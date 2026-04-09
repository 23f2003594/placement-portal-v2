import sqlite3
from flask import Blueprint , request , session , redirect , url_for , flash,jsonify
from werkzeug.security import check_password_hash , generate_password_hash
from database import get_connection
auth_bp = Blueprint('auth',__name__)
@auth_bp.route('/register/student',methods=["GET","POST"])
def register_student():
    data = request.get_json()
    email = data.get('email')
    pwd = generate_password_hash(data.get('password'))
    name = data.get('name')
    roll_no = data.get('roll_no')
    branch = data.get('branch')
    year = data.get('year')
    cgpa = data.get('cgpa')
    education = data.get('education')
    skills = data.get('skills')
    resume_link = data.get('resume_link')
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("insert into users (email,password,role) values (?,?,?)",(email,pwd,"student"))
        user_id = cur.lastrowid
        cur.execute("insert into students (user_id,name,branch,year,cgpa,education,skills,resume_link,roll_no) values (?,?,?,?,?,?,?,?,?)",(user_id,name,branch,year,cgpa,education,skills,resume_link,roll_no))
        conn.commit()
        return jsonify({"success": True, "message": "Registration successful"}), 201
    except sqlite3.IntegrityError:
        return jsonify({"success": False, "message": "Email already registered"}), 400
    finally:
        conn.close()
@auth_bp.route("/register/company",methods=["GET","POST"])
def register_company():
    data = request.get_json()
    email = data.get('email')
    pwd = generate_password_hash(data.get('password'))
    name = data.get('name')
    industry = data.get('industry')
    location = data.get('location')
    hr_contact = data.get('hr_contact')
    website = data.get('website')
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("insert into users (email,password,role) values (?,?,?)",(email,pwd,"company"))
        user_id = cur.lastrowid
        cur.execute("insert into companies (user_id,name,industry,location,hr_contact,website) values (?,?,?,?,?,?)",(user_id,name,industry,location,hr_contact,website))
        conn.commit()
        return jsonify({"success":True,"message":"Registration successful. Admin approval pending."})
    except sqlite3.IntegrityError:
        return jsonify({"success":"False","message":"Email already registered."})
    finally:
        conn.close()
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "message": "No data received"}), 400
    email = data.get("email")
    password = data.get("password")
    conn = get_connection()
    user = conn.execute("select * from users where email=?",(email,)).fetchone()
    conn.close()
    if not user or user["is_active"] != 1 or not check_password_hash(user["password"], password):
        return jsonify({"success":False,"message":"Invalid credentials or inactive account"}),401
    if user["role"] == "company":
        conn = get_connection()
        company = conn.execute("select approval_status from companies where user_id=?",(user["id"],)).fetchone()
        conn.close()
        if not company :
            return jsonify({"success": False, "message": "Company record not found"}), 403
        if company["approval_status"] == "pending":
            return jsonify({"success": False, "message": "Company not approved by admin yet"}), 403
        if company["approval_status"] == "rejected" :
            return jsonify({"success": False, "message": "Your registration has been rejected"}), 403  
    if user["role"]=="student":
        conn = get_connection()
        student = conn.execute("select is_blacklisted from students where user_id=?",(user["id"],)).fetchone()
        conn.close()
        if student and student["is_blacklisted"]==1:
            return jsonify({"success": False, "message": "Account blacklisted"}), 403
    return jsonify({"success":True,"user":{"id":user["id"],"role":user["role"],"email":user["email"]}})
@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully.","success")
    return redirect(url_for('auth.login'))
