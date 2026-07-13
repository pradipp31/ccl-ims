from flask import Flask, render_template, request, redirect, session, url_for
from datetime import date
from database import (init_db, seed_db, get_student, get_officer, get_all_students,
                       get_all_posts, get_post_by_id, save_student, save_application,
                       get_applications_by_student, get_all_applications, update_application_status)

app = Flask(__name__)
app.secret_key = 'ccl-ims-secret-key-2026'

# ── HOME ──
@app.route('/')
def home():
    if 'student_email' in session:
        return redirect('/dashboard')
    return redirect('/login')

# ── LOGIN (Student + Officer dono) ──
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        student = get_student(email)
        officer = get_officer(email)

        if student and student['password'] == password:
            session['student_email'] = student['email']
            session['student_name'] = student['name']
            session['student_id'] = student['id']
            return redirect('/dashboard')
        elif officer and officer['password'] == password:
            session['officer_email'] = officer['email']
            session['officer_name'] = officer['name']
            return redirect('/officer/dashboard')
        else:
            error = "Invalid email or password!"

    return render_template('login.html', error=error)

# ── REGISTER ──
@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        confirm = request.form['confirm_password']
        college = request.form['college']
        branch = request.form['branch']
        year = request.form['year']

        if password != confirm:
            error = "Passwords do not match!"
        else:
            success = save_student(name, email, password, college, branch, year)
            if success:
                return redirect('/login')
            else:
                error = "Email already registered!"

    return render_template('register.html', error=error)

# ── STUDENT DASHBOARD ──
@app.route('/dashboard')
def dashboard():
    if 'student_email' not in session:
        return redirect('/login')
    return render_template('student_dashboard.html', name=session['student_name'])

# ── AVAILABLE POSTS ──
@app.route('/posts')
def posts():
    if 'student_email' not in session:
        return redirect('/login')
    all_posts = get_all_posts()
    return render_template('posts.html', posts=all_posts)

# ── APPLY FORM ──
@app.route('/apply/<int:post_id>', methods=['GET', 'POST'])
def apply(post_id):
    if 'student_email' not in session:
        return redirect('/login')

    post = get_post_by_id(post_id)

    if request.method == 'POST':
        today = date.today().isoformat()
        success = save_application(session['student_id'], post_id, today)
        if success:
            return render_template('apply.html', post=post, submitted=True)
        else:
            return render_template('apply.html', post=post, error="Aap already apply kar chuke ho!")

    return render_template('apply.html', post=post, submitted=False)

# ── MY APPLICATIONS ──
@app.route('/my-applications')
def my_applications():
    if 'student_email' not in session:
        return redirect('/login')
    apps = get_applications_by_student(session['student_id'])
    return render_template('my_application.html', applications=apps)

# ── OFFICER DASHBOARD ──
@app.route('/officer/dashboard')
def officer_dashboard():
    if 'officer_email' not in session:
        return redirect('/login')
    status_filter = request.args.get('status')
    apps = get_all_applications(status_filter)
    return render_template('officer_dashboard.html', applications=apps, name=session['officer_name'], current_filter=status_filter)

# ── UPDATE STATUS (Officer action) ──
@app.route('/update-status/<int:app_id>', methods=['POST'])
def update_status(app_id):
    if 'officer_email' not in session:
        return redirect('/login')
    new_status = request.form['status']
    update_application_status(app_id, new_status)
    return redirect('/officer/dashboard')

# ── LOGOUT ──
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

# ── MAIN ──
if __name__ == '__main__':
    init_db()
    seed_db()
    app.run(debug=True)
