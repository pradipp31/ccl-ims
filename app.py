import os
from flask import Flask, render_template, request, redirect, session, url_for
from datetime import date
from werkzeug.utils import secure_filename
from database import (init_db, seed_db, get_student, get_student_by_id, get_officer, get_all_students,
                       get_all_posts, get_post_by_id, save_student, save_application,
                       get_applications_by_student, get_pending_hr_applications, get_approved_hr_applications,
                       hr_approve_application, hr_reject_application,
                       get_applications_by_department, update_final_status,
                       save_internship_details, get_internship_details,
                       get_selected_applications_without_details,
                       create_notification, get_notifications_for_student,
                       get_notifications_for_hr_admin, mark_notification_as_read,
                       get_unread_count_student, get_unread_count_hr_admin,
                       mark_all_notifications_as_read)

app = Flask(__name__)
app.secret_key = 'ccl-ims-secret-key-2026-production'

UPLOAD_FOLDER = os.path.join('static', 'uploads')
ALLOWED_EXTENSIONS = {'pdf', 'jpg', 'jpeg', 'png'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_uploaded_file(file, student_id, doc_name):
    if file and allowed_file(file.filename):
        filename = secure_filename(f"{student_id}_{doc_name}_{file.filename}")
        path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(path)
        return f"uploads/{filename}"
    return None

@app.context_processor
def inject_unread_counts():
    unread_student = 0
    unread_hr = 0
    if 'student_email' in session:
        unread_student = get_unread_count_student(session['student_id'])
    if session.get('officer_role') == 'admin_hr':
        unread_hr = get_unread_count_hr_admin()
    return dict(unread_student=unread_student, unread_hr=unread_hr)

@app.route('/')
def home():
    if 'student_email' in session:
        return redirect('/dashboard')
    if 'officer_email' in session:
        if session.get('officer_role') == 'admin_hr':
            return redirect('/hr/dashboard')
        return redirect('/department/dashboard')
    return render_template('select_login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        email = request.form['email'].strip()
        password = request.form['password'].strip()
        student = get_student(email)
        if student and student['password'] == password:
            session['student_email'] = student['email']
            session['student_name'] = student['name']
            session['student_id'] = student['id']
            return redirect('/dashboard')
        else:
            error = "Invalid email or password!"
    return render_template('login.html', error=error)

@app.route('/officer-login', methods=['GET', 'POST'])
def officer_login():
    error = None
    if request.method == 'POST':
        email = request.form['email'].strip()
        password = request.form['password'].strip()
        officer = get_officer(email)
        if officer and officer['password'] == password:
            session['officer_email'] = officer['email']
            session['officer_name'] = officer['name']
            session['officer_role'] = officer['role']
            session['officer_department'] = officer['department']
            if officer['role'] == 'admin_hr':
                return redirect('/hr/dashboard')
            else:
                return redirect('/department/dashboard')
        else:
            error = "Invalid officer email or password!"
    return render_template('officer_login.html', error=error)

@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email'].strip()
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

@app.route('/dashboard')
def dashboard():
    if 'student_email' not in session:
        return redirect('/login')
    return render_template('student_dashboard.html', name=session['student_name'])

@app.route('/posts')
def posts():
    if 'student_email' not in session:
        return redirect('/login')
    return render_template('posts.html', posts=get_all_posts())

@app.route('/apply/<int:post_id>', methods=['GET', 'POST'])
def apply(post_id):
    if 'student_email' not in session:
        return redirect('/login')

    post = get_post_by_id(post_id)

    if request.method == 'POST':
        student_id = session['student_id']
        photo = save_uploaded_file(request.files.get('photo'), student_id, 'photo')
        resume = save_uploaded_file(request.files.get('resume'), student_id, 'resume')
        aadhar = save_uploaded_file(request.files.get('aadhar'), student_id, 'aadhar')
        noc = save_uploaded_file(request.files.get('noc'), student_id, 'noc')
        id_card = save_uploaded_file(request.files.get('id_card'), student_id, 'idcard')

        if not all([photo, resume, aadhar, noc, id_card]):
            return render_template('apply.html', post=post, submitted=False,
                                    error="All documents must be uploaded (PDF/JPG/PNG format only)!")

        today = date.today().isoformat()
        success = save_application(student_id, post_id, today, photo, resume, aadhar, noc, id_card)
        if success:
            return render_template('apply.html', post=post, submitted=True)
        else:
            return render_template('apply.html', post=post, submitted=False,
                                    error="You have already applied for this post!")

    return render_template('apply.html', post=post, submitted=False)

@app.route('/my-applications')
def my_applications():
    if 'student_email' not in session:
        return redirect('/login')
    apps = get_applications_by_student(session['student_id'])
    return render_template('my_application.html', applications=apps)

@app.route('/hr/dashboard')
def hr_dashboard():
    if session.get('officer_role') != 'admin_hr':
        return redirect('/officer-login')
    pending_apps = get_pending_hr_applications()
    approved_apps = get_approved_hr_applications()
    return render_template('hr_dashboard.html', pending_applications=pending_apps, approved_applications=approved_apps, name=session['officer_name'])

@app.route('/hr/approve/<int:app_id>', methods=['POST'])
def hr_approve(app_id):
    if session.get('officer_role') != 'admin_hr':
        return redirect('/officer-login')
    
    department = request.form['department']
    hr_approve_application(app_id, department)
    
    from database import get_db
    conn = get_db()
    app_data = conn.execute("SELECT student_id FROM applications WHERE id = ?", (app_id,)).fetchone()
    conn.close()
    
    if app_data:
        student = get_student_by_id(app_data['student_id'])
        create_notification('student', app_data['student_id'],
            'Application Approved by HR',
            f'Your application has been approved by HR and forwarded to {department} department.',
            'hr_approved', app_id)
        create_notification('hr_admin', 0,
            'Application Approved',
            f'You approved {student["name"]} - assigned to {department}',
            'hr_approved', app_id)
    
    return redirect('/hr/dashboard')

@app.route('/hr/reject/<int:app_id>', methods=['POST'])
def hr_reject(app_id):
    if session.get('officer_role') != 'admin_hr':
        return redirect('/officer-login')
    
    hr_reject_application(app_id)
    
    from database import get_db
    conn = get_db()
    app_data = conn.execute("SELECT student_id FROM applications WHERE id = ?", (app_id,)).fetchone()
    conn.close()
    
    if app_data:
        create_notification('student', app_data['student_id'],
            'Application Rejected',
            'Your application has been rejected by HR.',
            'hr_rejected', app_id)
    
    return redirect('/hr/dashboard')

@app.route('/department/dashboard')
def department_dashboard():
    if session.get('officer_role') != 'department':
        return redirect('/officer-login')
    status_filter = request.args.get('status')
    dept = session['officer_department']
    apps = get_applications_by_department(dept, status_filter)
    return render_template('department_dashboard.html', applications=apps, name=session['officer_name'],
                            department=dept, current_filter=status_filter)

@app.route('/department/update-status/<int:app_id>', methods=['POST'])
def department_update_status(app_id):
    if session.get('officer_role') != 'department':
        return redirect('/officer-login')
    
    new_status = request.form['status']
    update_final_status(app_id, new_status)
    
    from database import get_db
    conn = get_db()
    app_data = conn.execute("SELECT student_id FROM applications WHERE id = ?", (app_id,)).fetchone()
    conn.close()
    
    if app_data:
        student = get_student_by_id(app_data['student_id'])
        dept = session['officer_department']
        
        if new_status == 'Selected':
            create_notification('student', app_data['student_id'],
                'Congratulations! Application Selected',
                f'Your application has been selected by {dept} department.',
                'selected', app_id)
            create_notification('hr_admin', 0,
                'Application Selected',
                f'{student["name"]} selected by {dept}. Add internship details.',
                'selected', app_id)
        else:
            create_notification('student', app_data['student_id'],
                'Application Rejected',
                f'Your application has been rejected by {dept} department.',
                'rejected', app_id)
    
    return redirect('/department/dashboard')

@app.route('/hr/add-internship-details')
def hr_manager_internship_details():
    if session.get('officer_role') != 'admin_hr':
        return redirect('/officer-login')
    apps = get_selected_applications_without_details()
    return render_template('hr_manager_internship_details.html', applications=apps,
                            name=session['officer_name'])

@app.route('/hr/save-details/<int:app_id>', methods=['POST'])
def hr_manager_save_details(app_id):
    if session.get('officer_role') != 'admin_hr':
        return redirect('/officer-login')

    duration_months = request.form['duration_months']
    start_date = request.form['start_date']
    end_date = request.form['end_date']
    reporting_time_start = request.form['reporting_time_start']
    reporting_time_end = request.form['reporting_time_end']
    department = request.form['department']
    reporting_location = request.form['reporting_location']
    stipend_amount = request.form.get('stipend_amount', 0)
    additional_notes = request.form.get('additional_notes', '')

    save_internship_details(app_id, duration_months, start_date, end_date,
                            reporting_time_start, reporting_time_end, department,
                            reporting_location, stipend_amount, additional_notes)
    
    from database import get_db
    conn = get_db()
    app_data = conn.execute("SELECT student_id FROM applications WHERE id = ?", (app_id,)).fetchone()
    conn.close()
    
    if app_data:
        create_notification('student', app_data['student_id'],
            'Internship Details Finalized',
            f'Your internship starts {start_date} at {reporting_time_start}. Check offer letter.',
            'internship_details_added', app_id)
    
    return redirect('/hr/add-internship-details')

@app.route('/internship-offer/<int:app_id>')
def internship_offer(app_id):
    if 'student_email' not in session:
        return redirect('/login')

    apps = get_applications_by_student(session['student_id'])
    app_ids = [app['id'] for app in apps]
    if app_id not in app_ids:
        return redirect('/my-applications')

    details = get_internship_details(app_id)
    if not details:
        return redirect('/my-applications')

    return render_template('internship_offer.html', details=details)

@app.route('/notifications')
def notifications():
    if 'student_email' not in session:
        return redirect('/login')
    
    student_id = session['student_id']
    notifs = get_notifications_for_student(student_id)
    mark_all_notifications_as_read('student', student_id)
    
    return render_template('notifications.html', notifications=notifs)

@app.route('/hr/notifications')
def hr_notifications():
    if session.get('officer_role') != 'admin_hr':
        return redirect('/officer-login')
    
    notifs = get_notifications_for_hr_admin()
    mark_all_notifications_as_read('hr_admin')
    
    return render_template('hr_notifications.html', notifications=notifs, name=session['officer_name'])

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

@app.route('/officer-logout')
def officer_logout():
    session.clear()
    return redirect('/officer-login')

@app.route('/test-students')
def test_students():
    students = get_all_students()
    output = "<h2>Students in Database (" + str(len(students)) + " total):</h2><ul>"
    for s in students:
        output += f"<li>{s['name']} — EMAIL: [{s['email']}] — PASSWORD: [{s['password']}]</li>"
    output += "</ul>"
    return output

if __name__ == '__main__':
    init_db()
    seed_db()

    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)


