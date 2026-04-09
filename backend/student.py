from flask import Blueprint ,request,jsonify
from database import get_connection
from datetime import datetime

student_bp = Blueprint("student",__name__)
@student_bp.route("/drives/<int:user_id>",methods=['GET'])
def view_drives(user_id):
    search=request.args.get("search","")
    conn=get_connection()
    student=conn.execute("select id,branch,cgpa from students where user_id=?",(user_id,)).fetchone()
    if not student:
        return jsonify({"message":"Student profile not found"}),404
    query="select p.id,p.title,p.description,p.salary,p.eligibility_cgpa,p.eligibility_branch,c.location,p.skills_required,p.application_deadline,c.name as company_name,exists(select 1 from applications a where a.drive_id = p.id and a.student_id =?) as already_applied,(p.eligibility_branch = 'All' or p.eligibility_branch like '%' || ? || '%') as is_branch_eligible from placement_drive p join companies c on p.company_id = c.id where p.status='approved' and c.approval_status='approved'"
    params=[student["id"],student["branch"]]
    if search:
        query+="and (p.title like ? or c.name like ? or p.skills_required like ? or c.location like ?)"
        search_term = f"%{search}%"
        params.extend([search_term , search_term , search_term , search_term])
    drives =  conn.execute(query,params).fetchall()
    conn.close()
    return jsonify([dict(d) for d in drives])

@student_bp.route("/apply",methods=['POST'])
def apply_drive():
    data = request.get_json()
    user_id = data.get("user_id")
    drive_id = data.get("drive_id")
    conn = get_connection()
    student = conn.execute("select id,branch,cgpa,year from students where user_id=?",(user_id,)).fetchone()
    existing = conn.execute("select id from applications where drive_id=? and student_id=?",(drive_id,student["id"])).fetchone()
    if existing:
        conn.close()
        return jsonify({"message":"Already applied"}),403
    drive = conn.execute("select * from placement_drive where id=?",(drive_id,)).fetchone()
    if drive['eligibility_branch'] != 'All' and student['branch'] not in drive['eligibility_branch']:
        return jsonify({"message": "You are not eligible for this drive"}), 403
    if(student["cgpa"]<drive["eligibility_cgpa"]):
        conn.close()
        return jsonify({"message":"Not eligible"}),403
    placed = conn.execute("select 1 FROM applications where student_id=? AND status='placed' ", (student["id"],)).fetchone()
    if placed:
        conn.close()
        return jsonify({"message": "You are already placed and cannot apply for more drives."}), 403
    conn.execute("insert into applications(drive_id,student_id,status,applied_date) values(?,?,'applied',?)",(drive_id,student["id"],datetime.now().strftime("%Y-%m-%d")))
    conn.commit()
    conn.close()
    return jsonify({"success":True,"message":"Applied successfully"})

@student_bp.route("/applications/<int:user_id>",methods=['GET'])
def application_history(user_id):
    conn = get_connection()
    student = conn.execute("select id from students where user_id=?",(user_id,)).fetchone()
    apps = conn.execute("select a.id as application_id, p.title, c.name as company_name, a.status, a.applied_date, a.interview_date, a.feedback, pl.offer_letter_link from applications a join placement_drive p on a.drive_id = p.id join companies c on p.company_id = c.id join students s on a.student_id = s.id left join placement pl on a.id = pl.application_id where s.id = ?", (student["id"],)).fetchall()
    conn.close()
    return jsonify([dict(a) for a in apps])
@student_bp.route("/profile/<int:user_id>", methods=["GET", "POST"])
def manage_profile(user_id):
    conn = get_connection()
    try:
        if request.method=="GET":
            student = conn.execute("select s.*,u.email from students s join users u on s.user_id=u.id where s.user_id=?",(user_id,)).fetchone()
            conn.close()
            if student:
                return jsonify(dict(student)),200
            return jsonify({"success":False,"message":"Student not found"}),404
        if request.method=="POST":
            data = request.get_json()
            conn.execute("update students set education=?,skills=?,resume_link=?,cgpa=? where user_id=?",(data.get("education"),data.get("skills"),data.get("resume_link"),data.get("cgpa"),user_id))
            conn.commit()
            return jsonify({"success": True, "message": "Profile updated successfully"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
    finally:
        conn.close()
@student_bp.route("/accept-offer",methods=["POST"])
def accept_offer():
    data=request.get_json()
    application_id = data.get("application_id")
    conn = get_connection()
    try:
        app = conn.execute("select a.student_id , a.drive_id ,a.feedback as offer_link from applications a where a.id=?",(application_id,)).fetchone()
        drive = conn.execute("select company_id,title,salary from placement_drive where id=?",(app["drive_id"],)).fetchone()
        conn.execute("update applications set status='placed' where id=?", (application_id,))
        conn.execute("insert into placement (application_id, student_id, company_id, position, salary, offer_letter_link) values (?, ?, ?, ?, ?, ?)", (application_id, app["student_id"], drive["company_id"], drive["title"], drive["salary"], app["offer_link"]))
        conn.commit()
        return jsonify({"success":True,"message":"Congratulations, Your placement is confirmed."})
    except Exception as e:
        return jsonify({"error": str(e)}),500
    finally:
        conn.close()
@student_bp.route("/reject-offer", methods=["POST"])
def reject_offer():
    data = request.get_json()
    application_id = data.get("application_id")
    conn = get_connection()
    try:
        conn.execute("UPDATE applications SET status='rejected' WHERE id=?", (application_id,))
        conn.commit()
        return jsonify({"success": True, "message": "Offer declined successfully."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()



