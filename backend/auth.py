import sqlite3
from flask import Blueprint , request , session , redirect , url_for , flash , render_template
from werkzeug.security import check_password_hash , generate_password_hash
from database import get_connection

auth_bp = Blueprint('auth',__name__)

@auth_bp.route('/register/student',methods=["GET","POST"])
def register_student():
    if request.method == "POST":
        email = request.form['email']
        pwd = generate_password_hash(request.form['password'])
        name = request.form['name']
        roll_no = request.form['roll_no']
        branch = request.form['branch']
        year = request.form['year']
        cgpa = request.form['cgpa']
        education = request.form['education']
        skills = request.form['skills']
        resume_link = request.form['resume_link']

        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute("insert into users (email,password,role) values (?,?,?)",(email,pwd,"student"))
            user_id = cur.lastrowid
            cur.execute("insert into students (user_id,name,branch,year,cgpa,education,skills,resume_link,roll_no) values (?,?,?,?,?,?,?,?,?)",(user_id,name,branch,year,cgpa,education,skills,resume_link,roll_no))
            conn.commit()
            flash("Registration successful.","success")
            return redirect(url_for('auth.login'))
        except sqlite3.IntegrityError:
            flash("Email already registered.","danger")
        finally:
            conn.close()
    return render_template("student_register.html")

@auth_bp.route("/register/company",methods=["GET","POST"])
def register_company():
    if request.method == "POST":
        email = request.form['email']
        pwd = generate_password_hash(request.form['password'])
        name = request.form['name']
        industry = request.form['industry']
        location = request.form['location']
        hr_contact = request.form['hr_contact']
        website = request.form['website']

        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute("insert into users (email,password,role) values (?,?,?)",(email,pwd,"company"))
            user_id = cur.lastrowid
            cur.execute("insert into companies (user_id,name,industry,location,hr_contact,website) values (?,?,?,?,?,?)",(user_id,name,industry,location,hr_contact,website))
            conn.commit()
            flash("Registration successful. Admin approval pending.","success")
            return redirect(url_for('auth.login'))
        except sqlite3.IntegrityError:
            flash("Email already registered.","danger")
        finally:
            conn.close()
    return render_template("company_register.html") 

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        # 1️⃣ get user
        conn = get_connection()
        user = conn.execute("select * from users where email=?",(email,)).fetchone()
        conn.close()

        if not user or user["is_active"] != 1 or not check_password_hash(user["password"], password):
            flash("Invalid credentials or inactive account.", "danger")
            return redirect(url_for("auth.login"))

        if user["role"] == "company":
            conn = get_connection()
            company = conn.execute("select approval_status from companies where user_id=?",(user["id"],)).fetchone()
            conn.close()

            if not company or company["approval_status"] != "approved":
                flash("Company not approved by admin yet.", "warning")
                return redirect(url_for("auth.login"))
            
        if user["role"]=="student":
            conn = get_connection()
            student = conn.execute("select is_blacklisted from students where user_id=?",(user["id"],)).fetchone()
            conn.close()
            if student and student["is_blacklisted"]==1:
                flash("Your account has been blacklisted. Contact admin.","danger")
                return redirect(url_for("auth.login"))

        session["user_id"] = user["id"]
        session["role"] = user["role"]

        if user["role"] == "admin":
            return redirect(url_for("admin.dashboard"))
        elif user["role"] == "company":
            return redirect(url_for("company_dashboard"))
        else:
            return redirect(url_for("student_dashboard"))

    return render_template("login.html")


@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully.","success")
    return redirect(url_for('auth.login'))

