from flask import Blueprint , session , redirect , url_for , render_template,request
from database import get_connection

student_bp = Blueprint("student",__name__)

def student_required():
    return session.get("role")=="student"

@student_bp.route("/drives")
def view_drives():
    if not student_required():
        return redirect(url_for("auth.login"))
    search = request.args.get("search","")
    conn = get_connection()
    query="select p.id,p.title,p.description,p.salary,p.skills_required,p.application_deadline,c.name as company_name from placement_drive p join companies c on p.company_id = c.id where p.status='approved' and c.approval_status='approved'"
    params=[]
    if search:
        query+="and (p.title like ? or c.name like ? or p.skills_required like ?)"
        search_term = f"%{search}%"
        params = [search_term , search_term , search_term]
    drives =  conn.execute(query,params).fetchall()
    conn.close()
    return render_template("student_drives.html",drives=drives)

@student_bp.route("/drives/<int:drive_id>/apply")
def apply_drives(drive_id):
    if not student_required():
        return redirect(url_for("auth.login"))
    user_id = session["user_id"]
    conn = get_connection()
    student = conn.execute("select id from students where user_id=?",(user_id,)).fetchone()
    student_id = student["id"]
    existing = conn.execute("select id from applications where drive_id=? and student_id=?",(drive_id,student_id)).fetchone()
    if existing:
        conn.close()
        return "Already applied"
    drive = conn.execute("select eligibility_branch,eligibility_cgpa,eligibility_year from placement_drive where id=?",(drive_id,)).fetchone()
    student_data = conn.execute("select branch,cgpa,year from students where id=?",(student_id,)).fetchone()
    if(student_data["cgpa"]<drive["eligibility_cgpa"]):
        conn.close()
        return "Not eligible"
    conn.execute("insert into applications(drive_id,student_id,status) values(?,?,'applied')",(drive_id,student_id))
    conn.commit()
    conn.close()
    return redirect(url_for("student.view_drives"))

@student_bp.route("/applications")
def application_history():
    if not student_required():
        return redirect(url_for("auth.login"))
    user_id = session["user_id"]
    conn = get_connection()
    student = conn.execute("select id from students where user_id=?",(user_id,)).fetchone()

    apps = conn.execute("select a.id as application_id ,p.title,c.name as company_name,a.status,a.applied_date,a.interview_date,a.feedback,pl.offer_letter_link from applications a join placement_drive p on a.drive_id=p.id join companies c on p.company_id=c.id left join placement pl on pl.application_id = a.id where a.student_id=?", (student["id"],)).fetchall()
    conn.close()
    return render_template("student_history.html", applications=apps)

@student_bp.route("/profile", methods=["GET", "POST"])
def profile():
    if not student_required():
        return redirect(url_for("auth.login"))

    user_id = session["user_id"]
    conn = get_connection()
    student = conn.execute("select * from students where user_id=?",(user_id,)).fetchone()
    if request.method == "POST":
        conn.execute("update students set education=?, skills=?, resume_link=?, cgpa=? where user_id=?", (request.form["education"],request.form["skills"],request.form["resume_link"],request.form["cgpa"],user_id))
        conn.commit()
        conn.close()
        return redirect(url_for("student.profile"))

    conn.close()
    return render_template("student_profile.html", student=student)

@student_bp.route("/accept/<int:application_id>",methods=["GET","POST"])
def accept_offer(application_id):
    if not student_required():
        return redirect(url_for("auth.login"))

    conn = get_connection()

    conn.execute("update applications set status='placed' where id=?", (application_id,))

    conn.commit()
    conn.close()

    return redirect(url_for("student.application_history"))



