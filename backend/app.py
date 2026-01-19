from flask import Flask,session , redirect , url_for
from auth import auth_bp
from database import init_db
from config import DB_PATH
import os

app = Flask(__name__)

app.secret_key = "shakthi_key_2026"

app.register_blueprint(auth_bp, url_for_prefix='/auth')

@app.route("/")
def home():
    return "Placement portal is running DB at {}".format(DB_PATH)

@app.route("/admin/dashboard")
def admin_dashboard():
    if session.get('role') != 'admin':
        return redirect(url_for('auth.login'))
    return "Admin dashboard"

@app.route("/company/dashboard")
def company_dashboard():
    if session.get('role') != 'company':
        return redirect(url_for('auth.login'))
    return "Company dashboard"

@app.route("/student/dashboard")
def student_dashboard():
    if session.get('role') != 'student':
        return redirect(url_for('auth.login'))
    return "Student dashboard"


if __name__ == "__main__":
    if not os.path.exists(DB_PATH):
        init_db()
    else:
        print("Database already exists at {}".format(DB_PATH))
    app.run(debug=True)
