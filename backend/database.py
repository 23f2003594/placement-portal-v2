import sqlite3
from datetime import datetime
from config import DB_PATH
from werkzeug.security import generate_password_hash

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.row_factory = sqlite3.Row
    return conn

def create_tables():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("create table if not exists users (id integer primary key autoincrement , email text unique not null ,password text not null , role text not null check (role in ('admin','company','student')),is_active integer default 1, created_at text default current_timestamp )")

    cur.execute("create table if not exists companies (id integer primary key autoincrement , user_id integer not null unique , name text not null , industry text , location text , hr_contact text , website text , approval_status text default 'pending' check (approval_status in ('pending','approved','rejected')),created_at text default current_timestamp ,foreign key(user_id) references users(id) on delete cascade )")

    cur.execute("create table if not exists students ( id integer primary key autoincrement , user_id integer not null unique , name text not null , branch text , year integer , cgpa real , education text , skills text , resume_link text , created_at text default current_timestamp ,foreign key(user_id) references users(id) on delete cascade )")

    cur.execute("create table if not exists placement_drive(id integer primary key autoincrement , company_id integer not null , title text not null , description text , salary integer , skills_required text , eligibility_branch text , eligibility_cgpa real , eligibility_year integer , application_deadline text , status text default 'pending' check (status in ('pending','approved','closed')) ,created_at text default current_timestamp , foreign key(company_id) references companies(id) on delete cascade )")

    cur.execute("create table if not exists applications ( id integer primary key autoincrement , drive_id integer not null , student_id integer not null , status text default 'applied' check (status in ('applied','shortlisted','rejected','selected')) , applied_date text default current_timestamp , foreign key(drive_id) references placement_drive(id) on delete cascade, foreign key(student_id) references students(id) on delete cascade , unique(drive_id,student_id) )")

    cur.execute("create table if not exists placement ( id integer primary key autoincrement , application_id integer not null unique , student_id integer not null , company_id integer not null , position text , salary integer , joining_date text , created_at text default current_timestamp , foreign key(student_id) references students(id) on delete cascade, foreign key(company_id) references companies(id) on delete cascade )")

    conn.commit()
    conn.close()
    print("Tables created successfully.")

def create_admin():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("select id from users where role='admin'")
    admin = cur.fetchone()
    if admin is None:
        hashed_pwd = generate_password_hash("admin2026")
        cur.execute("insert into users (email,password,role,is_active) values (?,?,?,?)",("admin@institute.edu",hashed_pwd,"admin",1))
        conn.commit()
        print("Admin user created successfully.")
    else:
        print("Admin user already exists.")
    conn.close()

def init_db():
    print("Initializing database...")
    create_tables()
    create_admin()
    print("database initialized successfully.")
