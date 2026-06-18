# Placement Portal System v2

A comprehensive, three-tier full-stack placement management system designed to streamline campus recruitment. This system features a secure **Node.js Middleware** for authentication and API routing, bridging the gap between a **Vue.js** frontend and a **Flask** backend.

---

## System Architecture

The project follows a secure Three-Tier Architecture:
1. **Frontend**: Vue.js 3 (Vite) - Interactive UI for Students, Companies, and Admins.
2. **Middleware**: Node.js/Express - Handles JWT issuance, Role-based verification, and API proxying.
3. **Backend**: Flask/Python - Manages business logic and SQLite database transactions.

---

##  Tech Stack

| Layer | Technology |
| :--- | :--- |
| **Frontend** | Vue.js 3, Vite, Axios, Bootstrap 5, Bootstrap Icons |
| **Middleware** | Node.js, Express, JSONWebToken (JWT), Axios |
| **Backend** | Python 3.x, Flask, SQLite3 |
| **Security** | JWT (Role-based: Admin, Student, Company), Password Hashing (Werkzeug) |

---

## Features

###  Student
- **Profile Management**: Update CGPA, branch, skills, and resume links.
- **Drive Discovery**: Search and browse approved placement drives.
- **Applications**: Apply to drives and track real-time status updates (Shortlisted, Interview, etc.).
- **Offer Management**: View feedback, accept/reject offers, and access offer letters.

###  Company
- **Registration**: Self-register and wait for Admin verification.
- **Drive Lifecycle**: Create recruitment drives (subject to admin approval).
- **Candidate Management**: Shortlist, Schedule Interviews, and Select candidates.
- **Offer Letters**: Finalize placements and provide Google Drive offer links.

###  Admin
- **System Oversight**: Approve/Reject companies and recruitment drives.
- **User Management**: Activate/Deactivate companies and blacklist/whitelist students.
- **Placements Master List**: View all finalized placements across the institution.
- **Analytics**: Dashboard with system statistics and placement counts.

---

##  Project Structure

```text
placement-portal-v2/
├── backend/                # Flask Backend (Business Logic)
│   ├── app.py              # Main Entry & Blueprint Registration
│   ├── database.py         # Schema Definition & DB Initialization
│   ├── auth.py             # User Authentication Logic
│   ├── admin.py            # Admin-specific Endpoints
│   ├── student.py          # Student-specific Endpoints
│   ├── company.py          # Company-specific Endpoints
│   └── placement_portal.db # SQLite Database File
├── middleware/             # Node.js Express Middleware (Security)
│   ├── index.js            # JWT Verification & Proxy Logic
│   ├── package.json        # Node Dependencies
│   └── node_modules/       
├── frontend-v2/            # Vue.js Frontend (UI)
│   ├── src/
│   │   ├── components/     # Vue Views (Login, Dashboard, Profile, etc.)
│   │   ├── services/api.js # Central Axios Configuration
│   │   └── router/index.js # Vue Router with Auth Guards
│   ├── package.json
│   └── vite.config.js
└── README.md

```
---
## Installation and Setup 

### Backend

 - cd backend
 - pip install -r requirements.txt
 - python app.py
 - Runs on http://localhost:5000

### Frontend

 - cd frontend-v2
 - npm install
 - npm run dev
 - Runs on http://localhost:5173

### Middleware (Express)

 - cd middleware
 - npm install
 - node index.js
 - Runs on http://localhost:3000

 ---

 ## Security and DataFlow

 - Authentication: Users log in through the Middleware. The Flask backend verifies credentials, and the Node middleware issues a JWT containing the user id and role.

 - Authorization: Routes are protected by middleware functions (verifyAdmin, verifyStudent, verifyCompany) that check the JWT role before forwarding requests to Flask.

 - Database Integrity: SQLite is configured with PRAGMA foreign_keys = ON to ensure cascading deletes and data consistency across related tables.

---

## Important Notes

 - Storage: Resumes and Offer Letters are stored as external Google Drive links.

 - Workflow: Drives must be approved by an Admin before they become visible to students.

 - Constraint: Once a student accepts an offer and is marked as Placed, they are restricted from applying to further drives.

## Author
Shakthi Kumaran Gnanavel
VIT Chennai 

## License
This project is for academic and educational purposes.






