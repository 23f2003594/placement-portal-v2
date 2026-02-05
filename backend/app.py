from flask import Flask, session, redirect, url_for,render_template
from auth import auth_bp
from admin import admin_bp
from database import init_db
from config import DB_PATH

app = Flask(__name__)
app.secret_key = "shakthi_key_2026"

init_db()

app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(admin_bp, url_prefix="/admin")

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
    return "company dashboard"

@app.route("/student/dashboard")
def student_dashboard():
    if session.get("role") != "student":
        return redirect(url_for("auth.login"))
    return "student dashboard"

if __name__ == "__main__":
    app.run(debug=True)
