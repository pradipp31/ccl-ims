import sqlite3

DB_NAME = 'ccl_ims.db'

def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

# ── DATABASE INITIALIZE ──
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

    # officers ab role aur department dono rakhte hain
    # role = 'admin_hr' (documents approve karta hai) ya 'department' (final decision leta hai)
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

    # applications mein documents ke path aur do-stage status hai
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

    conn.commit()
    conn.close()

# ── SEED SAMPLE DATA ──
def seed_db():
    conn = get_db()
    c = conn.cursor()

    c.execute("SELECT COUNT(*) FROM students")
    if c.fetchone()[0] == 0:
        students = [
            ("Rahul Kumar", "rahul1@test.com", "pass123", "BIT Sindri", "CSE", "3rd"),
            ("Priya Sharma", "priya@test.com", "pass123", "NIT Jamshedpur", "ECE", "2nd"),
            ("Amit Singh", "amit@test.com", "pass123", "RIT Jamshedpur", "ME", "4th"),
            ("Sneha Gupta", "sneha@test.com", "pass123", "BIT Sindri", "CSE", "3rd"),
            ("Rohan Mehta", "rohan@test.com", "pass123", "NIT Jamshedpur", "Civil", "1st"),
            ("Anjali Verma", "anjali@test.com", "pass123", "RIT Jamshedpur", "ECE", "2nd"),
            ("Vikas Yadav", "vikas@test.com", "pass123", "BIT Sindri", "ME", "4th"),
            ("Pooja Kumari", "pooja@test.com", "pass123", "NIT Jamshedpur", "CSE", "3rd"),
            ("Saurabh Jha", "saurabh@test.com", "pass123", "RIT Jamshedpur", "Civil", "2nd"),
            ("Neha Rani", "neha@test.com", "pass123", "BIT Sindri", "ECE", "1st"),
            ("Ankit Raj", "ankit@test.com", "pass123", "NIT Jamshedpur", "ME", "4th"),
            ("Divya Kumari", "divya@test.com", "pass123", "RIT Jamshedpur", "CSE", "3rd"),
            ("Manish Tiwari", "manish@test.com", "pass123", "BIT Sindri", "Civil", "2nd"),
            ("Kavita Devi", "kavita@test.com", "pass123", "NIT Jamshedpur", "ECE", "1st"),
            ("Suresh Prasad", "suresh@test.com", "pass123", "RIT Jamshedpur", "ME", "3rd"),
            ("Ritu Kumari", "ritu@test.com", "pass123", "BIT Sindri", "CSE", "4th"),
            ("Deepak Kumar", "deepak@test.com", "pass123", "NIT Jamshedpur", "Civil", "2nd"),
            ("Shweta Singh", "shweta@test.com", "pass123", "RIT Jamshedpur", "ECE", "1st"),
            ("Gaurav Ojha", "gaurav@test.com", "pass123", "BIT Sindri", "ME", "3rd"),
            ("Nisha Kumari", "nisha@test.com", "pass123", "NIT Jamshedpur", "CSE", "2nd"),
            ("Abhishek Anand", "abhishek@test.com", "pass123", "RIT Jamshedpur", "Civil", "4th"),
            ("Komal Sinha", "komal@test.com", "pass123", "BIT Sindri", "ECE", "3rd"),
            ("Rakesh Mahato", "rakesh@test.com", "pass123", "NIT Jamshedpur", "ME", "1st"),
            ("Sunita Kumari", "sunita@test.com", "pass123", "RIT Jamshedpur", "CSE", "2nd"),
            ("Vivek Kumar", "vivek@test.com", "pass123", "BIT Sindri", "Civil", "4th"),
        ]
        c.executemany("INSERT INTO students (name, email, password, college, branch, year) VALUES (?,?,?,?,?,?)", students)

    c.execute("SELECT COUNT(*) FROM officers")
    if c.fetchone()[0] == 0:
        officers = [
            # HR Admin — documents approve karta hai, department assign karta hai
            ("HR Admin", "hradmin@ccl.com", "admin123", "admin_hr", None),
            # Teen department officers — final decision lete hain
            ("HR Officer", "hr@ccl.com", "hr123", "department", "HR"),
            ("PR Officer", "pr@ccl.com", "pr123", "department", "PR"),
            ("ERP Officer", "erp@ccl.com", "erp123", "department", "ERP"),
        ]
        c.executemany("INSERT INTO officers (name, email, password, role, department) VALUES (?,?,?,?,?)", officers)

    c.execute("SELECT COUNT(*) FROM internship_posts")
    if c.fetchone()[0] == 0:
        posts = [
            ("IT Intern", "IT Department", 5, "2026-08-15", 1),
            ("Mining Engineer Intern", "Mining", 3, "2026-08-20", 1),
            ("HR Intern", "Human Resources", 2, "2026-08-10", 1),
            ("Finance Intern", "Finance", 4, "2026-08-25", 1),
        ]
        c.executemany("INSERT INTO internship_posts (title, department, total_seats, last_date, is_active) VALUES (?,?,?,?,?)", posts)

    conn.commit()
    conn.close()

# ── STUDENT FUNCTIONS ──
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

# ── OFFICER FUNCTIONS ──
def get_officer(email):
    conn = get_db()
    officer = conn.execute("SELECT * FROM officers WHERE email = ?", (email,)).fetchone()
    conn.close()
    return officer

# ── POSTS FUNCTIONS ──
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

# ── APPLICATION FUNCTIONS (with documents) ──
def save_application(student_id, post_id, applied_date, photo, resume, aadhar, noc, id_card):
    conn = get_db()
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
    conn.close()
    return True

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

# ── HR ADMIN: saari fresh applications jo approval ke wait mein hain ──
def get_pending_hr_applications():
    conn = get_db()
    apps = conn.execute('''
        SELECT applications.*, students.name, students.college, students.branch,
               internship_posts.title
        FROM applications
        JOIN students ON applications.student_id = students.id
        JOIN internship_posts ON applications.post_id = internship_posts.id
        WHERE applications.hr_approval_status = 'Pending HR Approval'
    ''').fetchall()
    conn.close()
    return apps

# ── HR ADMIN: approve karke department assign karna ──
def hr_approve_application(app_id, department):
    conn = get_db()
    conn.execute('''UPDATE applications SET hr_approval_status = 'Approved',
                     assigned_department = ?, final_status = 'Pending' WHERE id = ?''',
                 (department, app_id))
    conn.commit()
    conn.close()

def hr_reject_application(app_id):
    conn = get_db()
    conn.execute("UPDATE applications SET hr_approval_status = 'Rejected', final_status = 'Rejected' WHERE id = ?",
                 (app_id,))
    conn.commit()
    conn.close()

# ── DEPARTMENT OFFICER: apne department ki approved applications dekhna ──
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
    conn.execute("UPDATE applications SET final_status = ? WHERE id = ?", (new_status, app_id))
    conn.commit()
    conn.close()

