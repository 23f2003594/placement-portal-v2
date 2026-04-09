from flask import render_template, Blueprint, session, jsonify, request
from database import get_connection
company_bp = Blueprint('company', __name__)
@company_bp.route("/stats/<int:user_id>",methods=["GET"])
def get_company_stats(user_id):
    conn = get_connection()
    company = conn.execute("select * from companies where user_id=?", (user_id,)).fetchone()
    if not company:
        return jsonify({"error":"Company profile not found. Please contact admin."}),404
    company_id = company['id']
    approval_status = company['approval_status']
    total_drives = conn.execute("select count(*) from placement_drive where company_id=?", (company_id,)).fetchone()[0] 
    total_apps = conn.execute("select count(*) from applications where drive_id in (select id from placement_drive where company_id=?)", (company_id,)).fetchone()[0]
    hired = conn.execute("select count(*) from applications where status='placed' and drive_id in (select id from placement_drive where company_id=?)", (company_id,)).fetchone()[0]
    conn.close()
    return jsonify({"company_name":company['name'],"approval_status":approval_status,"stats":{"total_drives":total_drives, "total_apps":total_apps, "hired":hired}})
@company_bp.route("/drives/create/<int:user_id>", methods=["POST"])
def create_drive(user_id):
    data = request.get_json()
    conn = get_connection()
    company = conn.execute("select * from companies where user_id=?", (user_id,)).fetchone()
    if not company:
        conn.close()
        return jsonify({"message":"Profile not found"}),404
    if(company["approval_status"]!="approved"):
        conn.close()
        return jsonify({"message":"Account not approved to post drives."}),403
    try:
        conn.execute("insert into placement_drive(company_id,title,description,salary,skills_required,eligibility_branch,eligibility_cgpa,eligibility_year,application_deadline, status) values (?,?,?,?,?,?,?,?,?,'pending')", (company['id'],data.get("title"),data.get("description"), data.get("salary"),data.get("skills_required"),data.get("eligibility_branch"),data.get("eligibility_cgpa"),data.get("eligibility_year"),data.get("application_deadline")))
        conn.commit()
        return jsonify({"success":True,"message":"Drive created and awaiting admin approval"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
    finally:
        conn.close()
@company_bp.route("/drives/list/<int:user_id>",methods=['GET'])
def list_drives(user_id):
    conn = get_connection()
    company = conn.execute("select * from companies where user_id=?", (user_id,)).fetchone()
    company_id = company["id"]
    if not company:
        return jsonify({"error":"Profile not found"}),404
    drives = conn.execute("select p.id,p.title,p.status,p.salary,(select count(*) from applications a where a.drive_id = p.id) as total_applications,(select count(*) from applications a where a.drive_id = p.id and a.status in('shortlisted','placed','selected')) as shortlisted_count from placement_drive p where p.company_id=?", (company_id,)).fetchall()
    conn.close()
    return jsonify([dict(d) for d in drives])
@company_bp.route("/drives/<int:drive_id>/applications",methods=['GET'])
def get_applications(drive_id):
    conn = get_connection()
    applications = conn.execute("select a.id as app_id, a.student_id ,s.name, s.roll_no,s.cgpa, a.status, a.interview_date ,a.feedback,u.email from applications a join students s on a.student_id = s.id join users u on s.user_id = u.id where a.drive_id=?", (drive_id,)).fetchall()
    conn.close()
    return jsonify([dict(a) for a in applications])
@company_bp.route("/applications/<int:app_id>/shortlist",methods=["POST"])
def shortlist(app_id):
    conn = get_connection()
    conn.execute("update applications set status='shortlisted' where id=?", (app_id,))
    conn.commit()
    conn.close()
    return jsonify({"success": True, "message": "Student shortlisted"})
@company_bp.route("/applications/<int:app_id>/reject",methods=["POST"])
def reject(app_id):
    conn = get_connection()
    conn.execute("update applications set status='rejected' where id=?", (app_id,))
    conn.commit()
    conn.close()
    return jsonify({"success": True, "message": "Application rejected"})
@company_bp.route("/applications/<int:app_id>/select",methods=["GET","POST"])
def select(app_id):
    conn = get_connection()
    if request.method=="POST":
        data = request.get_json()
        offer_link = data.get("offer_link")
        try:
            conn.execute("update applications set status='selected',feedback=? where id=? ", (offer_link,app_id))
            conn.commit()
            return jsonify({"success": True, "message": "Candidate selected! waiting for confirmation"})
        except Exception as e:
            return jsonify({"success": False, "message": str(e)}), 500
        finally:
            conn.close()
@company_bp.route("/applications/<int:app_id>/schedule", methods=["GET","POST"])
def schedule_interview(app_id):
    conn = get_connection()
    if request.method == "POST":
        data = request.get_json()
        interview_date = data.get("interview_date")
        feedback = data.get("feedback")
        conn.execute("update applications set interview_date=?, feedback=?,status='interview' where id=?", (interview_date, feedback, app_id))
        conn.commit()
        conn.close()
        return jsonify({"success": True, "message": "Interview scheduled"})
@company_bp.route("/drives/<int:drive_id>/selected", methods=["GET"])
def view_selected_students(drive_id):
    conn = get_connection()
    selected = conn.execute("select s.name, s.roll_no, u.email, s.branch, s.cgpa, p.offer_letter_link from placement p join students s ON p.student_id = s.id join users u on s.user_id = u.id where p.application_id IN (SELECT id FROM applications WHERE drive_id = ?)", (drive_id,)).fetchall()
    conn.close()
    return jsonify([dict(s) for s in selected])
@company_bp.route("/students/<int:student_id>", methods=["GET"])
def get_student_profile(student_id):
    conn = get_connection()
    student = conn.execute("select s.*,u.email from students s join users u on s.user_id = u.id where s.id=?", (student_id,)).fetchone()
    conn.close()
    if not student:
        return jsonify({"error": "Student not found"}), 404
    return jsonify(dict(student))
@company_bp.route("/student/<int:student_id>")
def view_student_profile(student_id):
    conn = get_connection()
    student = conn.execute("select s.*,u.email from students s join users u on s.user_id = u.id where s.id=?", (student_id,)).fetchone()
    conn.close()
    return render_template("company_student_profile.html",student=student)
