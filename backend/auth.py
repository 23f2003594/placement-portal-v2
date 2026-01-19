import sqlite3
from flask import Blueprint , request , session , redirect , url_for , flash
from werkzeug.security import check_password_hash , generate_password_hash
from database import get_connection

auth_bp = Blueprint('auth',__name__)

@auth_bp.route('/register/student',methods=["GET","POST"])
def register_student():
    if request.method == "POST":
        email = request.form['email']
        pwd = generate_password_hash(request.form['password'])
        name = request.form['name']
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
            cur.execute("insert into students (user_id,name,branch,year,cgpa,education,skills,resume_link) values (?,?,?,?,?,?,?,?)",(user_id,name,branch,year,cgpa,education,skills,resume_link))
            conn.commit()
            flash("Registration successful.","success")
            return redirect(url_for('auth.login'))
        except sqlite3.IntegrityError:
            flash("Email already registered.","danger")
        finally:
            conn.close()
    return "Student Registration Page"

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
    return "Company Registration Page"

@auth_bp.route("/login",methods=["GET","POST"])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']

        conn = get_connection()
        cur = conn.cursor()
        cur.execute("select * from users where email=?",(email,))
        user = cur.fetchone()
        conn.close()

        if user and check_password_hash(user['password'],password):
            session['user_id'] = user['id']
            session['role'] = user['role']
            flash("Login successful.","success")
            if user['role'] == 'admin':
                return redirect(url_for('admin_dashboard'))
            elif user['role'] == 'company':
                return redirect(url_for('company_dashboard'))
            elif user['role'] == 'student':
                return redirect(url_for('student_dashboard'))
        else:
            flash("Invalid credentials.","danger")
    return "Login Page"

@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully.","success")
    return redirect(url_for('auth.login'))

