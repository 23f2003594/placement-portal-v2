from flask import Blueprint,session,redirect,url_for,jsonify,request
from database import get_connection

admin_bp=Blueprint('admin',__name__)

def admin_required():
    return session.get('role')=='admin'

@admin_bp.route("/dashboard",methods=["GET"])
def dashboard():
    conn=get_connection()
    cur=conn.cursor()
    stats={"total_students":cur.execute("select count(*) from students").fetchone()[0],"total_companies":cur.execute("select count(*) from companies").fetchone()[0],"total_drives":cur.execute("select count(*) from placement_drive").fetchone()[0],"total_applications":cur.execute("select count(*) from applications").fetchone()[0]}
    conn.close()
    return jsonify(stats)

@admin_bp.route("/companies",methods=['GET'])
def manage_companies():
    query=request.args.get("q","")
    conn=get_connection()
    if query:
        companies=conn.execute("select c.id,c.name,c.industry,u.email,c.approval_status,u.id as user_id,u.is_active from companies c join users u on c.user_id=u.id where c.name like ? or c.industry like ?",(f"%{query}%",f"%{query}%")).fetchall()
        conn.close()
    else:
        companies=conn.execute("select c.id,c.name,c.industry,u.email,c.approval_status,u.id as user_id,u.is_active from companies c join users u on c.user_id=u.id").fetchall()
    conn.close()
    return jsonify([dict(c) for c in companies])

@admin_bp.route("/companies/pending",methods=['GET'])
def pending_companies():
    conn = get_connection()
    companies = conn.execute("select * from companies where approval_status='pending'").fetchall()
    conn.close()
    return jsonify([dict(c) for c in companies])

@admin_bp.route("/companies/<int:company_id>/approve",methods=['POST'])
def approve_company(company_id):
    conn = get_connection()
    conn.execute("update companies set approval_status='approved' where id=?",(company_id,))
    conn.commit()
    conn.close()
    return jsonify({"success":True,"message":"Company approved"})

@admin_bp.route("/companies/<int:company_id>/reject",methods=['POST'])
def reject_company(company_id):
    conn = get_connection()
    conn.execute("update companies set approval_status='rejected' where id=?",(company_id,))
    conn.commit()
    conn.close()
    return jsonify({"success":True,"message":"Company rejected"})

@admin_bp.route("/companies/<int:user_id>/toggle-active",methods=['POST'])
def toggle_company_active(user_id):
    conn = get_connection()
    conn.execute("update users set is_active = 1-is_active where id=?",(user_id,))
    conn.commit()
    conn.close()
    return jsonify({"success":True})
@admin_bp.route("/drives",methods=['GET'])
def manage_drives():
    conn = get_connection()
    drives = conn.execute("select p.id , p.title  ,p.description, p.salary, p.skills_required , p.eligibility_branch,p.eligibility_cgpa, p.eligibility_year ,p.status ,p.application_deadline, c.name as company_name from placement_drive p join companies c on p.company_id = c.id order by p.created_at desc").fetchall()
    conn.close()
    return jsonify([dict(d) for d in drives])

@admin_bp.route("/drives/pending")
def pending_drives():
    if not admin_required():
        return redirect(url_for('auth.login'))
    conn = get_connection()
    drives = conn.execute("select * from placement_drive where status='pending'").fetchall()
    conn.close()
    return jsonify([dict(d) for d in drives])

@admin_bp.route("/drives/<int:drive_id>/approve",methods=['POST'])
def approve_drive(drive_id):
    conn=get_connection()
    conn.execute("update placement_drive set status='approved' where id=?",(drive_id,))
    conn.commit()
    conn.close()
    return jsonify({"success":True,"message":"Drive approved and is now visible to students"})

@admin_bp.route("/drives/<int:drive_id>/close",methods=['POST'])
def close_drive(drive_id):
    conn=get_connection()
    conn.execute("update placement_drive set status='closed' where id=?",(drive_id,))
    conn.commit()
    conn.close()
    return jsonify({"success":True,"message":"Drive closed for applications"})

@admin_bp.route("/students", methods=["GET"])
def manage_students():
    query = request.args.get("q", "")
    conn = get_connection()
    if query:
        students = conn.execute("select s.id, s.roll_no, s.name, u.email, u.is_active, u.id as user_id, s.is_blacklisted from students s join users u on s.user_id = u.id where s.name like ? or u.email like ? or s.roll_no like ?",(f"%{query}%", f"%{query}%", f"%{query}%")).fetchall()
    else:
        students = conn.execute("select s.id, s.roll_no, s.name, u.email, u.is_active, u.id as user_id, s.is_blacklisted from students s join users u on s.user_id = u.id").fetchall()
    conn.close()
    return jsonify([dict(s) for s in students])

@admin_bp.route("/drives/<int:drive_id>/applications",methods=["GET"])
def view_drive_applications(drive_id):
    conn = get_connection()
    drive = conn.execute("select p.title, c.name as company_name from placement_drive p join companies c on p.company_id = c.id where p.id=?", (drive_id,)).fetchone()
    applications = conn.execute("select s.name as student_name,s.roll_no, a.status,a.id as app_id,s.cgpa,s.id as student_id,a.applied_date from applications a join students s on a.student_id = s.id where a.drive_id=? order by s.cgpa desc", (drive_id,)).fetchall()
    conn.close()
    return jsonify({"drive_title": drive["title"] if drive else "Unknown Drive","applicants": [dict(a) for a in applications]})

@admin_bp.route("/students/<int:student_id>/toggle-blacklist",methods=['POST'])
def toggle_student_blacklist(student_id):
    conn=get_connection()
    conn.execute("update students set is_blacklisted=1-is_blacklisted where id=?",(student_id,))
    conn.commit()
    conn.close()
    return jsonify({"success":True,"message":"Blacklist status updated"})

@admin_bp.route("/students/<int:student_id>",methods=['GET'])
def view_student_profile(student_id):
    conn = get_connection()
    student = conn.execute("select s.*, u.email from students s join users u on s.user_id = u.id where s.id = ?", (student_id,)).fetchone()
    conn.close()
    if student:
        return jsonify(dict(student))
    return jsonify({"message":"Student not found"}),404

@admin_bp.route("/placements", methods=["GET"])
def get_all_placements():
    conn = get_connection()
    query = "select p.id, s.name as student_name, c.name as company_name, p.position, p.salary, p.offer_letter_link from placement p join students s on p.student_id = s.id join companies c on p.company_id = c.id order by p.id desc"
    records = conn.execute(query).fetchall()
    conn.close()
    return jsonify([dict(row) for row in records])

