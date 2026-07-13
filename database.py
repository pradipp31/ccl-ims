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
            ("Suresh Verma", "officer1@ccl.com", "officer123", "HR"),
            ("Anita Rao", "officer2@ccl.com", "officer123", "Mining"),
        ]
        c.executemany("INSERT INTO officers (name, email, password, department) VALUES (?,?,?,?)", officers)

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
