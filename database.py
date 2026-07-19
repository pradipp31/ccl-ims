import sqlite3
from datetime import datetime
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(BASE_DIR, "ccl_ims.db")

def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        college TEXT,
        branch TEXT,
        year TEXT
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS officers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT NOT NULL,
        department TEXT
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS internship_posts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        department TEXT,
        total_seats INTEGER,
        last_date TEXT,
        is_active INTEGER DEFAULT 1
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS applications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        post_id INTEGER,
        applied_date TEXT,
        photo_path TEXT,
        resume_path TEXT,
        aadhar_path TEXT,
        noc_path TEXT,
        id_card_path TEXT,
        hr_approval_status TEXT DEFAULT 'Pending HR Approval',
        assigned_department TEXT,
        final_status TEXT DEFAULT 'Pending',
        FOREIGN KEY (student_id) REFERENCES students(id),
        FOREIGN KEY (post_id) REFERENCES internship_posts(id)
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS internship_details (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        application_id INTEGER UNIQUE,
        duration_months INTEGER,
        start_date TEXT,
        end_date TEXT,
        reporting_time_start TEXT,
        reporting_time_end TEXT,
        department TEXT,
        reporting_location TEXT,
        stipend_amount INTEGER,
        additional_notes TEXT,
        FOREIGN KEY (application_id) REFERENCES applications(id)
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS notifications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        recipient_type TEXT,
        recipient_id INTEGER,
        title TEXT,
        message TEXT,
        notification_type TEXT,
        related_application_id INTEGER,
        is_read INTEGER DEFAULT 0,
        created_at TEXT,
        FOREIGN KEY (related_application_id) REFERENCES applications(id)
    )''')

    conn.commit()
    conn.close()

def seed_db():
    conn = get_db()
    c = conn.cursor()

    c.execute("SELECT COUNT(*) FROM students")
    if c.fetchone()[0] == 0:
        students = [
            ("Rahul Kumar", "rahul1@gmail.com", "pass123", "BIT Sindri", "CSE", "3rd"),
            ("Priya Sharma", "priya@gmail.com", "pass123", "NIT Jamshedpur", "ECE", "2nd"),
            ("Amit Singh", "amit@gmail.com", "pass123", "RIT Jamshedpur", "ME", "4th"),
            ("Sneha Gupta", "sneha@gmail.com", "pass123", "BIT Sindri", "CSE", "3rd"),
            ("Rohan Mehta", "rohan@gmail.com", "pass123", "NIT Jamshedpur", "Civil", "1st"),
            ("Anjali Verma", "anjali@gmail.com", "pass123", "RIT Jamshedpur", "ECE", "2nd"),
            ("Vikas Yadav", "vikas@gmail.com", "pass123", "BIT Sindri", "ME", "4th"),
            ("Pooja Kumari", "pooja@gmail.com", "pass123", "NIT Jamshedpur", "CSE", "3rd"),
            ("Saurabh Jha", "saurabh@gmail.com", "pass123", "RIT Jamshedpur", "Civil", "2nd"),
            ("Neha Rani", "neha@gmail.com", "pass123", "BIT Sindri", "ECE", "1st"),
            ("Ankit Raj", "ankit@gmail.com", "pass123", "NIT Jamshedpur", "ME", "4th"),
            ("Divya Kumari", "divya@gmail.com", "pass123", "RIT Jamshedpur", "CSE", "3rd"),
            ("Manish Tiwari", "manish@gmail.com", "pass123", "BIT Sindri", "Civil", "2nd"),
            ("Kavita Devi", "kavita@gmail.com", "pass123", "NIT Jamshedpur", "ECE", "1st"),
            ("Suresh Prasad", "suresh@gmail.com", "pass123", "RIT Jamshedpur", "ME", "3rd"),
            ("Ritu Kumari", "ritu@gmail.com", "pass123", "BIT Sindri", "CSE", "4th"),
            ("Deepak Kumar", "deepak@gmail.com", "pass123", "NIT Jamshedpur", "Civil", "2nd"),
            ("Shweta Singh", "shweta@gmail.com", "pass123", "RIT Jamshedpur", "ECE", "1st"),
            ("Gaurav Ojha", "gaurav@gmail.com", "pass123", "BIT Sindri", "ME", "3rd"),
            ("Nisha Kumari", "nisha@gmail.com", "pass123", "NIT Jamshedpur", "CSE", "2nd"),
            ("Abhishek Anand", "abhishek@gmail.com", "pass123", "RIT Jamshedpur", "Civil", "4th"),
            ("Komal Sinha", "komal@gmail.com", "pass123", "BIT Sindri", "ECE", "3rd"),
            ("Rakesh Mahato", "rakesh@gmail.com", "pass123", "NIT Jamshedpur", "ME", "1st"),
            ("Sunita Kumari", "sunita@gmail.com", "pass123", "RIT Jamshedpur", "CSE", "2nd"),
            ("Vivek Kumar", "vivek@gmail.com", "pass123", "BIT Sindri", "Civil", "4th"),
            ("Pradip Kumar", "pradip31@gmail.com", "pradip3107", "BIT Sindri", "CSE", "3rd"),
            ("Tanya Sinha", "tanya1@gmail.com", "tanya123", "NIT Jamshedpur", "ECE", "2nd"),
            ("Harshit Harsh", "harshit2@gmail.com", "harshit3029", "RIT Jamshedpur", "ME", "4th"),
        ]
        c.executemany("INSERT INTO students (name, email, password, college, branch, year) VALUES (?,?,?,?,?,?)", students)

    c.execute("SELECT COUNT(*) FROM officers")
    if c.fetchone()[0] == 0:
        officers = [
            ("HR Admin", "hradmin@gmail.com", "admin123", "admin_hr", None),
            ("HR Officer", "hrofficer@gmail.com", "hr123", "department", "HR"),
            ("PR Officer", "profficer@gmail.com", "pr123", "department", "PR"),
            ("ERP Officer", "erpofficer@gmail.com", "erp123", "department", "ERP"),
        ]
        c.executemany("INSERT INTO officers (name, email, password, role, department) VALUES (?,?,?,?,?)", officers)

    c.execute("SELECT COUNT(*) FROM internship_posts")
    if c.fetchone()[0] == 0:
        posts = [
            ("IT Intern", "ERP", 25, "2026-07-25", 1),
            ("Mining Engineer Intern", "ERP", 25, "2026-07-25", 1),
            ("HR Intern", "HR", 25, "2026-07-25", 1),
            ("Finance Intern", "ERP", 25, "2026-07-25", 1),
            ("Public Relations Intern", "PR", 25, "2026-07-25", 1),
        ]
        c.executemany("INSERT INTO internship_posts (title, department, total_seats, last_date, is_active) VALUES (?,?,?,?,?)", posts)

    conn.commit()
    conn.close()

def get_student(email):
    conn = get_db()
    student = conn.execute("SELECT * FROM students WHERE email = ?", (email,)).fetchone()
    conn.close()
    return student

def get_student_by_id(student_id):
    conn = get_db()
    student = conn.execute("SELECT * FROM students WHERE id = ?", (student_id,)).fetchone()
    conn.close()
    return student

def get_all_students():
    conn = get_db()
    students = conn.execute("SELECT * FROM students").fetchall()
    conn.close()
    return students

def save_student(name, email, password, college, branch, year):
    conn = get_db()
    try:
        conn.execute("INSERT INTO students (name, email, password, college, branch, year) VALUES (?,?,?,?,?,?)",
                     (name, email, password, college, branch, year))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def get_officer(email):
    conn = get_db()
    officer = conn.execute("SELECT * FROM officers WHERE email = ?", (email,)).fetchone()
    conn.close()
    return officer

def get_all_posts():
    conn = get_db()
    posts = conn.execute("SELECT * FROM internship_posts WHERE is_active = 1").fetchall()
    conn.close()
    return posts

def get_post_by_id(post_id):
    conn = get_db()
    post = conn.execute("SELECT * FROM internship_posts WHERE id = ?", (post_id,)).fetchone()
    conn.close()
    return post

def save_application(student_id, post_id, applied_date, photo, resume, aadhar, noc, id_card):
    conn = get_db()
    try:
        existing = conn.execute("SELECT * FROM applications WHERE student_id=? AND post_id=?",
                                 (student_id, post_id)).fetchone()
        if existing:
            conn.close()
            return False
        conn.execute('''INSERT INTO applications
            (student_id, post_id, applied_date, photo_path, resume_path, aadhar_path, noc_path, id_card_path,
             hr_approval_status, final_status)
            VALUES (?,?,?,?,?,?,?,?, 'Pending HR Approval', 'Pending')''',
            (student_id, post_id, applied_date, photo, resume, aadhar, noc, id_card))
        conn.commit()
        return True
    finally:
        conn.close()

def get_applications_by_student(student_id):
    conn = get_db()
    apps = conn.execute('''
        SELECT applications.*, internship_posts.title, internship_posts.department
        FROM applications
        JOIN internship_posts ON applications.post_id = internship_posts.id
        WHERE applications.student_id = ?
    ''', (student_id,)).fetchall()
    conn.close()
    return apps

def get_pending_hr_applications():
    conn = get_db()
    apps = conn.execute('''
        SELECT applications.*, students.name, students.college, students.branch,
               internship_posts.title, internship_posts.department
        FROM applications
        JOIN students ON applications.student_id = students.id
        JOIN internship_posts ON applications.post_id = internship_posts.id
        WHERE applications.hr_approval_status = 'Pending HR Approval'
    ''').fetchall()
    conn.close()
    return apps

def get_approved_hr_applications():
    conn = get_db()
    apps = conn.execute('''
        SELECT applications.*, students.name, students.college, students.branch,
               internship_posts.title, internship_posts.department
        FROM applications
        JOIN students ON applications.student_id = students.id
        JOIN internship_posts ON applications.post_id = internship_posts.id
        WHERE applications.hr_approval_status = 'Approved'
    ''').fetchall()
    conn.close()
    return apps

def hr_approve_application(app_id, department):
    conn = get_db()
    try:
        conn.execute('''UPDATE applications SET hr_approval_status = 'Approved',
                         assigned_department = ?, final_status = 'Pending' WHERE id = ?''',
                     (department, app_id))
        conn.commit()
    finally:
        conn.close()

def hr_reject_application(app_id):
    conn = get_db()
    try:
        conn.execute("UPDATE applications SET hr_approval_status = 'Rejected', final_status = 'Rejected' WHERE id = ?",
                     (app_id,))
        conn.commit()
    finally:
        conn.close()

def get_applications_by_department(department, status_filter=None):
    conn = get_db()
    query = '''
        SELECT applications.*, students.name, students.college, students.branch,
               internship_posts.title
        FROM applications
        JOIN students ON applications.student_id = students.id
        JOIN internship_posts ON applications.post_id = internship_posts.id
        WHERE applications.assigned_department = ? AND applications.hr_approval_status = 'Approved'
    '''
    params = [department]
    if status_filter:
        query += " AND applications.final_status = ?"
        params.append(status_filter)
    apps = conn.execute(query, params).fetchall()
    conn.close()
    return apps

def update_final_status(app_id, new_status):
    conn = get_db()
    try:
        conn.execute("UPDATE applications SET final_status = ? WHERE id = ?", (new_status, app_id))
        conn.commit()
    finally:
        conn.close()

def save_internship_details(application_id, duration_months, start_date, end_date,
                             reporting_time_start, reporting_time_end, department,
                             reporting_location, stipend_amount=0, additional_notes=""):
    conn = get_db()
    try:
        conn.execute('''INSERT INTO internship_details
            (application_id, duration_months, start_date, end_date, reporting_time_start,
             reporting_time_end, department, reporting_location, stipend_amount, additional_notes)
            VALUES (?,?,?,?,?,?,?,?,?,?)''',
            (application_id, duration_months, start_date, end_date, reporting_time_start,
             reporting_time_end, department, reporting_location, int(stipend_amount), additional_notes))
        conn.commit()
    finally:
        conn.close()

def get_internship_details(application_id):
    conn = get_db()
    details = conn.execute("SELECT * FROM internship_details WHERE application_id = ?",
                           (application_id,)).fetchone()
    conn.close()
    return details

def get_selected_applications_without_details():
    conn = get_db()
    apps = conn.execute('''
        SELECT applications.*, students.name, students.college,
               internship_posts.title, internship_posts.department
        FROM applications
        JOIN students ON applications.student_id = students.id
        JOIN internship_posts ON applications.post_id = internship_posts.id
        WHERE applications.final_status = 'Selected'
        AND applications.id NOT IN (SELECT application_id FROM internship_details)
    ''').fetchall()
    conn.close()
    return apps

def create_notification(recipient_type, recipient_id, title, message, notification_type, related_application_id=None):
    conn = get_db()
    try:
        created_at = datetime.now().isoformat()
        conn.execute('''INSERT INTO notifications
            (recipient_type, recipient_id, title, message, notification_type, related_application_id, created_at)
            VALUES (?,?,?,?,?,?,?)''',
            (recipient_type, recipient_id, title, message, notification_type, related_application_id, created_at))
        conn.commit()
    finally:
        conn.close()

def get_notifications_for_student(student_id):
    conn = get_db()
    try:
        notifications = conn.execute(
            "SELECT * FROM notifications WHERE recipient_type = 'student' AND recipient_id = ? ORDER BY created_at DESC",
            (student_id,)
        ).fetchall()
        return list(notifications) if notifications else []
    finally:
        conn.close()

def get_notifications_for_hr_admin():
    conn = get_db()
    try:
        notifications = conn.execute(
            "SELECT * FROM notifications WHERE recipient_type = 'hr_admin' ORDER BY created_at DESC"
        ).fetchall()
        return list(notifications) if notifications else []
    finally:
        conn.close()

def get_unread_count_student(student_id):
    conn = get_db()
    try:
        count = conn.execute(
            "SELECT COUNT(*) FROM notifications WHERE recipient_type = 'student' AND recipient_id = ? AND is_read = 0",
            (student_id,)
        ).fetchone()[0]
        return count
    finally:
        conn.close()

def get_unread_count_hr_admin():
    conn = get_db()
    try:
        count = conn.execute(
            "SELECT COUNT(*) FROM notifications WHERE recipient_type = 'hr_admin' AND is_read = 0"
        ).fetchone()[0]
        return count
    finally:
        conn.close()

def mark_notification_as_read(notification_id):
    conn = get_db()
    try:
        conn.execute("UPDATE notifications SET is_read = 1 WHERE id = ?", (notification_id,))
        conn.commit()
    finally:
        conn.close()

def mark_all_notifications_as_read(recipient_type, recipient_id=None):
    conn = get_db()
    try:
        if recipient_type == 'student':
            conn.execute("UPDATE notifications SET is_read = 1 WHERE recipient_type = 'student' AND recipient_id = ?", (recipient_id,))
        else:
            conn.execute("UPDATE notifications SET is_read = 1 WHERE recipient_type = 'hr_admin'")
        conn.commit()
    finally:
        conn.close()





