from flask import Blueprint , session , redirect , url_for, jsonify , render_template ,request
from database import get_connection

admin_bp = Blueprint('admin',__name__)

def admin_required():
    return session.get('role')=='admin'

@admin_bp.route("/dashboard")
def dashboard():
    if not admin_required():
        return redirect(url_for('auth.login'))
    conn = get_connection()
    cur = conn.cursor()
    stats = {"total_students":cur.execute("select count(*) from students").fetchone()[0],"total_companies":cur.execute("select count(*) from companies").fetchone()[0],"total_drives":cur.execute("select count(*) from placement_drive").fetchone()[0],"total_applications":cur.execute("select count(*) from applications").fetchone()[0]}
    conn.close()
    return render_template("admin_dashboard.html",stats=stats)

@admin_bp.route("/companies")
def manage_companies():
    if not admin_required():
        return redirect(url_for('auth.login'))
    conn = get_connection()
    companies = conn.execute("select c.id , c.name , u.email , c.approval_status , u.id as user_id ,u.is_active from companies c join users u on c.user_id = u.id").fetchall()
    conn.close()
    return render_template("admin_companies.html",companies=companies)

@admin_bp.route("/companies/pending")
def pending_companies():
    if not admin_required():
        return redirect(url_for('auth.login'))
    conn = get_connection()
    companies = conn.execute("select * from companies where approval_status='pending'").fetchall()
    conn.close()
    return jsonify([dict(c) for c in companies])

@admin_bp.route("/companies/<int:company_id>/approve")
def approve_company(company_id):
    if not admin_required():
        return redirect(url_for('auth.login'))
    conn = get_connection()
    conn.execute("update companies set approval_status='approved' where id=?",(company_id,))
    conn.commit()
    conn.close()

    return redirect(url_for('admin.manage_companies'))

@admin_bp.route("/companies/<int:company_id>/reject")
def reject_company(company_id):
    if not admin_required():
        return redirect(url_for('auth.login'))
    conn = get_connection()
    conn.execute("update companies set approval_status='rejected' where id=?",(company_id,))
    conn.commit()
    conn.close()

    return redirect(url_for('admin.manage_companies'))

@admin_bp.route("/companies/<int:user_id>/toggle-active")
def toggle_company_active(user_id):
    if not admin_required():
        return redirect(url_for('auth.login'))
    conn = get_connection()
    conn.execute("update users set is_active = 1-is_active where id=?",(user_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('admin.manage_companies'))

@admin_bp.route("/drives")
def manage_drives():
    if not admin_required():
        return redirect(url_for('auth.login'))
    conn = get_connection()
    drives = conn.execute("select p.id , p.title  ,p.description, p.salary, p.skills_required , p.eligibility_branch,p.eligibility_cgpa, p.eligibility_year ,p.status ,p.application_deadline, c.name as company_name from placement_drive p join companies c on p.company_id = c.id order by p.created_at desc").fetchall()
    conn.close()
    return render_template("admin_drives.html",drives=drives)


@admin_bp.route("/drives/pending")
def pending_drives():
    if not admin_required():
        return redirect(url_for('auth.login'))
    conn = get_connection()
    drives = conn.execute("select * from placement_drive where status='pending'").fetchall()
    conn.close()
    return jsonify([dict(d) for d in drives])

@admin_bp.route("/drives/<int:drive_id>/approve")
def approve_drive(drive_id):
    if not admin_required():
        return redirect(url_for('auth.login'))
    conn = get_connection()
    conn.execute("update placement_drive set status='approved' where id=?",(drive_id,))
    conn.commit()
    conn.close()

    return redirect(url_for('admin.manage_drives'))

@admin_bp.route("/drives/<int:drive_id>/close")
def close_drive(drive_id):
    if not admin_required():
        return redirect(url_for('auth.login'))
    conn = get_connection()
    conn.execute("update placement_drive set status='closed' where id=?",(drive_id,))
    conn.commit()
    conn.close()

    return redirect(url_for('admin.manage_drives'))

@admin_bp.route("/students")
def manage_students():
    if not admin_required():
        return redirect(url_for('auth.login'))
    conn=get_connection()
    students = conn.execute("select  s.id , s.roll_no , s.name , u.email , u.is_active ,u.id as user_id , s.is_blacklisted from students s join users u on s.user_id = u.id").fetchall()
    conn.close()
    return render_template("admin_students.html",students=students)

@admin_bp.route("/applications")
def view_applications():
    if not admin_required():
        return redirect(url_for('auth.login'))
    conn=get_connection()
    apps = conn.execute("select c.name as company_name ,p.title as job_title ,p.id as drive_id  from placement_drive p  join companies c on p.company_id =c.id order by p.id desc").fetchall()
    conn.close()
    return render_template("admin_applications_drives.html",applications=apps)

@admin_bp.route("/applications/<int:drive_id>",methods=["GET","POST"])
def view_drive_applications(drive_id):
    if not admin_required():
        return redirect(url_for('auth.login'))

    conn = get_connection()

    drive = conn.execute("select p.title, c.name as company_name from placement_drive p join companies c on p.company_id = c.id where p.id=?", (drive_id,)).fetchone()
    applications = conn.execute("select s.name as student_name,s.roll_no, a.status from applications a join students s on a.student_id = s.id where a.drive_id=?", (drive_id,)).fetchall()
    conn.close()
    return render_template("admin_drives_applications.html",drive=drive,applications=applications)

@admin_bp.route("/students/<int:user_id>/toggle-active")
def toggle_student_active(user_id):
    if not admin_required():
        return redirect(url_for('auth.login'))
    conn=get_connection()
    conn.execute("update users set is_active=1-is_active where id=?",(user_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('admin.manage_students'))

@admin_bp.route("/students/<int:student_id>/toggle-blacklist")
def toggle_student_blacklist(student_id):
    if not admin_required():
        return redirect(url_for('auth.login'))
    conn=get_connection()
    conn.execute("update students set is_blacklisted=1-is_blacklisted where id=?",(student_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('admin.manage_students'))


@admin_bp.route("/companies/<int:company_id>/blacklist")
def blacklist_company(company_id):
    if not admin_required():
        return redirect(url_for('auth.login'))
    conn=get_connection()
    conn.execute("update users set is_active=0 where id=?",(company_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('admin.manage_companies'))

@admin_bp.route("/companies/<int:company_id>/unblacklist")
def unblacklist_company(company_id):
    if not admin_required():
        return redirect(url_for('auth.login'))
    conn=get_connection()
    conn.execute("update users set is_active=1 where id=?",(company_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('admin.manage_companies'))

@admin_bp.route("/search/students")
def search_students():
    if not admin_required():
        return redirect(url_for('auth.login'))
    query = request.args.get("q","")
    conn = get_connection()
    students = conn.execute("select s.id ,s.roll_no, s.name , u.email , u.is_active ,u.id as user_id , s.is_blacklisted from students s join users u on s.user_id = u.id where s.name like ? or u.email like ? or s.roll_no like ?",(f"%{query}%",f"%{query}%",f"%{query}%")).fetchall()
    conn.close()
    return render_template("admin_students.html",students=students,query=query,is_search=True)

@admin_bp.route("/search/companies")
def search_companies():
    if not admin_required():
        return redirect(url_for('auth.login'))
    query = request.args.get("q","")
    conn = get_connection()
    companies = conn.execute("select c.id , c.name ,c.industry , u.email , c.approval_status , u.id as user_id ,u.is_active from companies c join users u on c.user_id = u.id where c.name like ? or c.industry like ?",(f"%{query}%",f"%{query}%")).fetchall()
    conn.close()
    return render_template("admin_companies.html",companies=companies,query=query,is_search=True)

@admin_bp.route("/students/<int:student_id>")
def view_student(student_id):
    if not admin_required():
        return redirect(url_for("auth.login"))

    conn = get_connection()

    student = conn.execute("select s.*, u.email from students s join users u on s.user_id=u.id where s.id=?", (student_id,)).fetchone()
    conn.close()
    return render_template("admin_student_profile.html", student=student)


