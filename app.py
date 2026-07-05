from flask import Flask, render_template, request, redirect, session, url_for
from database import init_db, seed_db, get_student, get_officer, get_all_students, get_all_posts

app = Flask(__name__)
app.secret_key = 'ccl-ims-secret-key-2026'

# ── HOME ──
@app.route('/')
def home():
    if 'student_email' in session:
        return redirect('/dashboard')
    return redirect('/login')

# ── LOGIN ──
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        student = get_student(email)

        if student and student['password'] == password:
            session['student_email'] = student['email']
            session['student_name'] = student['name']
            return redirect('/dashboard')
        else:
            error = "Galat email ya password!"

    return render_template('login.html', error=error)

# ── DASHBOARD ──
@app.route('/dashboard')
def dashboard():
    if 'student_email' not in session:
        return redirect('/login')
    return render_template('student_dashboard.html', name=session['student_name'])

# ── LOGOUT ──
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

# ── ALL STUDENTS (TEST KARNE KE LIYE) ──
@app.route('/test-students')
def test_students():
    students = get_all_students()
    output = "<h2>25 Students Database Mein:</h2><ul>"
    for s in students:
        output += f"<li>{s['name']} — {s['email']} — {s['college']}</li>"
    output += "</ul>"
    return output

# ── MAIN — YAHAN SE WEBSITE START HOTI HAI ──
if __name__ == '__main__':
    init_db()
    seed_db()
    app.run(debug=True)