from flask import render_template, Blueprint, session, redirect, url_for, request
from database import get_connection

company_bp = Blueprint('company', __name__)

def company_required():
    return session.get('role') == 'company'

@company_bp.route("/dashboard")
def dashboard():
    if not company_required():
        return redirect(url_for('auth.login'))
    user_id = session.get('user_id')
    conn = get_connection()
    company = conn.execute("select * from companies where user_id=?", (user_id,)).fetchone()
    if not company:
        return "Company profile not found. Please contact admin."
    company_id = company['id']
    total_drives = conn.execute("select count(*) from placement_drive where company_id=?", (company_id,)).fetchone()[0] 
    total_apps = conn.execute("select count(*) from applications where drive_id in (select id from placement_drive where company_id=?)", (company_id,)).fetchone()[0]
    shortlisted = conn.execute("select count(*) from applications where status='shortlisted' and drive_id in (select id from placement_drive where company_id=?)", (company_id,)).fetchone()[0]
    conn.close()
    return render_template("company_dashboard.html", total_drives=total_drives, total_apps=total_apps, shortlisted=shortlisted)

@company_bp.route("/drives/create", methods=["GET", "POST"])
def create_drive():
    if not company_required():
        return redirect(url_for('auth.login'))
    if request.method == "POST":
        user_id = session.get('user_id')
        conn = get_connection()
        company = conn.execute("select * from companies where user_id=?", (user_id,)).fetchone()
        if not company:
            return "Company profile not found. Please contact admin."
        company_id = company['id']
        title = request.form.get("title")
        description = request.form.get("description")
        salary = request.form.get("salary")
        skills_required = request.form.get("skills_required")
        eligibility_branch = request.form.get("eligibility_branch")
        eligibility_cgpa = request.form.get("eligibility_cgpa")
        eligibility_year = request.form.get("eligibility_year")
        application_deadline = request.form.get("application_deadline")
        conn.execute("insert into placement_drive (company_id, title, description, salary, skills_required, eligibility_branch, eligibility_cgpa, eligibility_year, application_deadline,status) values (?,?,?,?,?,?,?,?,?,'pending')", (company_id, title, description, salary, skills_required, eligibility_branch, eligibility_cgpa, eligibility_year, application_deadline))
        conn.commit()
        conn.close()
        return redirect(url_for('company.list_drives'))
    return render_template("company_create_drive.html")

@company_bp.route("/drives")
def list_drives():
    if not company_required():
        return redirect(url_for('auth.login'))
    user_id = session.get('user_id')
    conn = get_connection()
    company = conn.execute("select * from companies where user_id=?", (user_id,)).fetchone()
    company_id = company["id"]
    drives = conn.execute("select p.id,p.title,p.status,(select count(*) from applications a where a.drive_id = p.id) as total_applications,(select count(*) from applications a where a.drive_id = p.id and a.status='shortlisted') as shortlisted_count from placement_drive p where p.company_id=?", (company_id,)).fetchall()
    conn.close()
    return render_template("company_drives.html", drives=drives)

@company_bp.route("/drives/<int:drive_id>/applications")
def view_applications(drive_id):
    if not company_required():
        return redirect(url_for('auth.login'))
    conn = get_connection()
    applications = conn.execute("select a.id, s.name, s.roll_no, a.status, a.interview_date ,a.feedback,u.email from applications a join students s on a.student_id = s.id join users u on s.user_id = u.id where a.drive_id=?", (drive_id,)).fetchall()
    conn.close()
    return render_template("company_applications.html", applications=applications, drive_id = drive_id)

@company_bp.route("/application/<int:app_id>/shortlist")
def shortlist(app_id):
    if not company_required():
        return redirect(url_for('auth.login'))
    conn = get_connection()
    conn.execute("update applications set status='shortlisted' where id=?", (app_id,))
    conn.commit()
    conn.close()
    return redirect(request.referrer)

@company_bp.route("/application/<int:app_id>/reject")
def reject(app_id):
    if not company_required():
        return redirect(url_for('auth.login'))
    conn = get_connection()
    conn.execute("update applications set status='rejected' where id=?", (app_id,))
    conn.commit()
    conn.close()
    return redirect(request.referrer)

@company_bp.route("/application/<int:app_id>/select")
def select(app_id):
    if not company_required():
        return redirect(url_for('auth.login'))
    conn = get_connection()
    conn.execute("update applications set status='selected' where id=?", (app_id,))
    conn.commit()
    conn.close()
    return redirect(request.referrer)

@company_bp.route("/application/<int:app_id>/schedule", methods=["GET","POST"])
def schedule_interview(app_id):
    if not company_required():
        return redirect(url_for('auth.login'))
    if request.method == "POST":
        interview_date = request.form["interview_date"]
        feedback = request.form["feedback"]
        conn = get_connection()
        conn.execute("update applications set interview_date=?, feedback=? where id=?", (interview_date, feedback, app_id))
        conn.commit()
        conn.close()
        return redirect(url_for('company_dashboard'))
    return render_template("schedule_interview.html", app_id=app_id)
