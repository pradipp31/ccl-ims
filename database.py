import sqlite3
from datetime import date

DB_NAME = 'ccl_ims.db'

def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    c = conn.cursor()

    # Students table
    c.execute('''CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        college TEXT,
        branch TEXT,
        year TEXT
    )''')

    # Officers table
    c.execute('''CREATE TABLE IF NOT EXISTS officers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        department TEXT
    )''')

    # Internship posts table
    c.execute('''CREATE TABLE IF NOT EXISTS internship_posts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        department TEXT,
        total_seats INTEGER,
        last_date TEXT,
        is_active INTEGER DEFAULT 1
    )''')

    # Applications table
    c.execute('''CREATE TABLE IF NOT EXISTS applications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        post_id INTEGER,
        applied_date TEXT,
        status TEXT DEFAULT 'Pending',
        FOREIGN KEY (student_id) REFERENCES students(id),
        FOREIGN KEY (post_id) REFERENCES internship_posts(id)
    )''')

    conn.commit()
    conn.close()

def seed_db():
    conn = get_db()
    c = conn.cursor()

    # Agar pehle se data hai toh dobara mat daalo
    existing = c.execute("SELECT COUNT(*) FROM students").fetchone()[0]
    if existing > 0:
        conn.close()
        return

    # 25 Sample Students
    students = [
        ('Rahul Kumar', 'rahul1@test.com', 'pass123', 'BIT Mesra', 'CSE', '3rd Year'),
        ('Priya Singh', 'priya2@test.com', 'pass123', 'NIT Jamshedpur', 'ECE', '2nd Year'),
        ('Aman Verma', 'aman3@test.com', 'pass123', 'BIT Sindri', 'ME', '4th Year'),
        ('Sneha Gupta', 'sneha4@test.com', 'pass123', 'RIT Jamshedpur', 'CSE', '3rd Year'),
        ('Vikas Yadav', 'vikas5@test.com', 'pass123', 'BIT Mesra', 'Civil', '2nd Year'),
        ('Anjali Sharma', 'anjali6@test.com', 'pass123', 'NIT Jamshedpur', 'CSE', '3rd Year'),
        ('Rohit Kumar', 'rohit7@test.com', 'pass123', 'BIT Sindri', 'ECE', '1st Year'),
        ('Pooja Devi', 'pooja8@test.com', 'pass123', 'RIT Jamshedpur', 'ME', '4th Year'),
        ('Suresh Prasad', 'suresh9@test.com', 'pass123', 'BIT Mesra', 'CSE', '2nd Year'),
        ('Kavita Kumari', 'kavita10@test.com', 'pass123', 'NIT Jamshedpur', 'Civil', '3rd Year'),
        ('Manoj Singh', 'manoj11@test.com', 'pass123', 'BIT Sindri', 'CSE', '4th Year'),
        ('Deepika Rani', 'deepika12@test.com', 'pass123', 'RIT Jamshedpur', 'ECE', '2nd Year'),
        ('Ajay Kumar', 'ajay13@test.com', 'pass123', 'BIT Mesra', 'ME', '3rd Year'),
        ('Neha Kumari', 'neha14@test.com', 'pass123', 'NIT Jamshedpur', 'CSE', '1st Year'),
        ('Sanjay Verma', 'sanjay15@test.com', 'pass123', 'BIT Sindri', 'Civil', '4th Year'),
        ('Ritu Singh', 'ritu16@test.com', 'pass123', 'RIT Jamshedpur', 'CSE', '2nd Year'),
        ('Vivek Kumar', 'vivek17@test.com', 'pass123', 'BIT Mesra', 'ECE', '3rd Year'),
        ('Shalini Devi', 'shalini18@test.com', 'pass123', 'NIT Jamshedpur', 'ME', '2nd Year'),
        ('Ravi Ranjan', 'ravi19@test.com', 'pass123', 'BIT Sindri', 'CSE', '4th Year'),
        ('Puja Kumari', 'puja20@test.com', 'pass123', 'RIT Jamshedpur', 'Civil', '1st Year'),
        ('Amit Kumar', 'amit21@test.com', 'pass123', 'BIT Mesra', 'CSE', '3rd Year'),
        ('Rekha Singh', 'rekha22@test.com', 'pass123', 'NIT Jamshedpur', 'ECE', '2nd Year'),
        ('Sunil Kumar', 'sunil23@test.com', 'pass123', 'BIT Sindri', 'ME', '4th Year'),
        ('Geeta Devi', 'geeta24@test.com', 'pass123', 'RIT Jamshedpur', 'CSE', '3rd Year'),
        ('Harsh Raj', 'harsh25@test.com', 'pass123', 'BIT Mesra', 'Civil', '2nd Year'),
    ]
    c.executemany(
        "INSERT INTO students (name, email, password, college, branch, year) VALUES (?,?,?,?,?,?)",
        students
    )

    # Sample Officers
    officers = [
        ('Admin Officer', 'admin@ccl.com', 'admin123', 'HR'),
        ('Rajesh Officer', 'rajesh@ccl.com', 'officer123', 'Mining'),
    ]
    c.executemany(
        "INSERT INTO officers (name, email, password, department) VALUES (?,?,?,?)",
        officers
    )

    # Sample Internship Posts
    posts = [
        ('IT Intern', 'IT Department', 5, '2026-08-15', 1),
        ('Mining Engineer Intern', 'Mining', 3, '2026-08-20', 1),
        ('Finance Intern', 'Finance', 2, '2026-08-10', 1),
        ('HR Intern', 'HR', 4, '2026-08-25', 1),
    ]
    c.executemany(
        "INSERT INTO internship_posts (title, department, total_seats, last_date, is_active) VALUES (?,?,?,?,?)",
        posts
    )

    conn.commit()
    conn.close()
    print("25 students, officers, and posts added successfully!")

# ── Query Functions ──

def get_student(email):
    conn = get_db()
    user = conn.execute(
        "SELECT * FROM students WHERE email=?", (email,)
    ).fetchone()
    conn.close()
    return user

def get_officer(email):
    conn = get_db()
    user = conn.execute(
        "SELECT * FROM officers WHERE email=?", (email,)
    ).fetchone()
    conn.close()
    return user

def get_all_students():
    conn = get_db()
    rows = conn.execute("SELECT * FROM students").fetchall()
    conn.close()
    return rows

def get_all_posts():
    conn = get_db()
    rows = conn.execute("SELECT * FROM internship_posts WHERE is_active=1").fetchall()
    conn.close()
    return rows

def save_student(name, email, password, college, branch, year):
    conn = get_db()
    conn.execute(
        "INSERT INTO students (name, email, password, college, branch, year) VALUES (?,?,?,?,?,?)",
        (name, email, password, college, branch, year)
    )
    conn.commit()
    conn.close()