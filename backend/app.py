from flask import Flask, session, redirect, url_for,render_template
from flask_cors import CORS
from auth import auth_bp
from admin import admin_bp
from company import company_bp
from student import student_bp
from database import init_db
from config import DB_PATH
app = Flask(__name__)
CORS(app)
init_db()
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(admin_bp, url_prefix="/admin")
app.register_blueprint(company_bp, url_prefix="/company")
app.register_blueprint(student_bp,url_prefix="/student")
@app.route("/")
def home():
    return "placement portal backend is running"
@app.route("/admin")
def admin_entry():
    if session.get("role") != "admin":
        return redirect(url_for("auth.login"))
    return render_template("admin_dashboard")
@app.route("/company/dashboard")
def company_dashboard():
    if session.get("role") != "company":
        return redirect(url_for("auth.login"))
    return render_template("company_dashboard.html")
@app.route("/student/dashboard")
def student_dashboard():
    if session.get("role") != "student":
        return redirect(url_for("auth.login"))
    return render_template("student_dashboard.html")
if __name__ == "__main__":
    app.run(host='localhost',port=5000,debug=True)