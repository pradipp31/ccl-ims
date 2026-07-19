import os
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from database import (
    init_db, seed_db, get_student, get_student_by_id, get_all_students, save_student,
    get_officer, get_all_posts, get_post_by_id, save_application, get_applications_by_student,
    get_pending_hr_applications, get_approved_hr_applications, hr_approve_application,
    hr_reject_application, get_applications_by_department, update_final_status,
    save_internship_details, get_internship_details, get_selected_applications_without_details,
    create_notification, get_notifications_for_student, get_notifications_for_hr_admin,
    get_unread_count_student, get_unread_count_hr_admin, mark_notification_as_read,
    mark_all_notifications_as_read
)
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'your-secret-key-ccl-ims'

# Context processor for unread counts
@app.context_processor
def inject_unread_counts():
    unread_student = 0
    unread_hr = 0
    
    if 'user_id' in session:
        if session.get('user_type') == 'student':
            unread_student = get_unread_count_student(session['user_id'])
        elif session.get('user_type') == 'hr_admin':
            unread_hr = get_unread_count_hr_admin()
    
    return dict(unread_student=unread_student, unread_hr=unread_hr)

# Initialize database
init_db()
seed_db()

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # Try student login
        student = get_student(email)
        if student and student['password'] == password:
            session['user_id'] = student['id']
            session['user_type'] = 'student'
            session['user_name'] = student['name']
            return redirect(url_for('student_dashboard'))
        
        # Try officer login
        officer = get_officer(email)
        if officer and officer['password'] == password:
            session['user_id'] = officer['id']
            session['user_type'] = officer['role']
            session['user_name'] = officer['name']
            session['department'] = officer['department']
            
            if officer['role'] == 'admin_hr':
                return redirect(url_for('hr_dashboard'))
            else:
                return redirect(url_for('department_dashboard'))
        
        return render_template('login.html', error='Invalid credentials')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        college = request.form.get('college', '')
        branch = request.form.get('branch', '')
        year = request.form.get('year', '')
        
        if save_student(name, email, password, college, branch, year):
            return redirect(url_for('login'))
        else:
            return render_template('register.html', error='Email already exists')
    
    return render_template('register.html')

# ==================== STUDENT ROUTES ====================

@app.route('/student/dashboard')
def student_dashboard():
    if 'user_id' not in session or session['user_type'] != 'student':
        return redirect(url_for('login'))
    
    applications = get_applications_by_student(session['user_id'])
    posts = get_all_posts()
    
    return render_template('student_dashboard.html', 
                         applications=applications, 
                         posts=posts)

@app.route('/student/apply/<int:post_id>', methods=['POST'])
def student_apply(post_id):
    if 'user_id' not in session or session['user_type'] != 'student':
        return redirect(url_for('login'))
    
    student_id = session['user_id']
    applied_date = datetime.now().strftime('%Y-%m-%d')
    
    # Handle file uploads
    photo = request.files.get('photo')
    resume = request.files.get('resume')
    aadhar = request.files.get('aadhar')
    noc = request.files.get('noc')
    id_card = request.files.get('id_card')
    
    photo_path = photo.filename if photo else ''
    resume_path = resume.filename if resume else ''
    aadhar_path = aadhar.filename if aadhar else ''
    noc_path = noc.filename if noc else ''
    id_card_path = id_card.filename if id_card else ''
    
    if save_application(student_id, post_id, applied_date, photo_path, resume_path, 
                       aadhar_path, noc_path, id_card_path):
        create_notification('student', student_id, 'Application Submitted',
                          'Your application has been submitted successfully',
                          'application_submitted', post_id)
        return redirect(url_for('student_dashboard'))
    else:
        return redirect(url_for('student_dashboard'))

@app.route('/student/notifications')
def student_notifications():
    if 'user_id' not in session or session['user_type'] != 'student':
        return redirect(url_for('login'))
    
    mark_all_notifications_as_read('student', session['user_id'])
    notifications = get_notifications_for_student(session['user_id'])
    
    return render_template('student_notifications.html', notifications=notifications)

# ==================== HR ADMIN ROUTES ====================

@app.route('/hr/dashboard')
def hr_dashboard():
    if 'user_id' not in session or session['user_type'] != 'admin_hr':
        return redirect(url_for('login'))
    
    pending_applications = get_pending_hr_applications()
    approved_applications = get_approved_hr_applications()
    
    return render_template('hr_dashboard.html',
                         pending_applications=pending_applications,
                         approved_applications=approved_applications)

@app.route('/hr/approve/<int:app_id>', methods=['POST'])
def hr_approve(app_id):
    if 'user_id' not in session or session['user_type'] != 'admin_hr':
        return redirect(url_for('login'))
    
    department = request.form.get('department', 'ERP')
    hr_approve_application(app_id, department)
    
    create_notification('hr_admin', session['user_id'],
                       'Application Approved',
                       'You have approved an application',
                       'application_approved', app_id)
    
    return redirect(url_for('hr_dashboard'))

@app.route('/hr/reject/<int:app_id>', methods=['POST'])
def hr_reject(app_id):
    if 'user_id' not in session or session['user_type'] != 'admin_hr':
        return redirect(url_for('login'))
    
    hr_reject_application(app_id)
    
    return redirect(url_for('hr_dashboard'))

@app.route('/hr/notifications')
def hr_notifications():
    if 'user_id' not in session or session['user_type'] != 'admin_hr':
        return redirect(url_for('login'))
    
    mark_all_notifications_as_read('hr_admin')
    notifications = get_notifications_for_hr_admin()
    
    return render_template('hr_notifications.html', notifications=notifications)

@app.route('/hr/add-internship-details', methods=['GET', 'POST'])
def hr_add_internship_details():
    if 'user_id' not in session or session['user_type'] != 'admin_hr':
        return redirect(url_for('login'))
    
    selected_applications = get_selected_applications_without_details()
    
    if request.method == 'POST':
        app_id = request.form['app_id']
        duration = request.form['duration_months']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        reporting_start = request.form['reporting_time_start']
        reporting_end = request.form['reporting_time_end']
        department = request.form['department']
        location = request.form['reporting_location']
        stipend = request.form.get('stipend_amount', 0)
        notes = request.form.get('additional_notes', '')
        
        save_internship_details(app_id, duration, start_date, end_date,
                              reporting_start, reporting_end, department,
                              location, stipend, notes)
        
        return redirect(url_for('hr_dashboard'))
    
    return render_template('hr_add_internship_details.html',
                         selected_applications=selected_applications)

# ==================== DEPARTMENT ROUTES ====================

@app.route('/department/dashboard')
def department_dashboard():
    if 'user_id' not in session or session['user_type'] not in ['department', 'admin_hr']:
        return redirect(url_for('login'))
    
    department = session.get('department', 'ERP')
    pending_applications = get_applications_by_department(department, 'Pending')
    selected_applications = get_applications_by_department(department, 'Selected')
    
    return render_template('department_dashboard.html',
                         pending_applications=pending_applications,
                         selected_applications=selected_applications,
                         department=department)

@app.route('/department/select/<int:app_id>', methods=['POST'])
def department_select(app_id):
    if 'user_id' not in session or session['user_type'] not in ['department', 'admin_hr']:
        return redirect(url_for('login'))
    
    update_final_status(app_id, 'Selected')
    
    create_notification('hr_admin', session['user_id'],
                       'Application Selected',
                       'An application has been selected by department',
                       'application_selected', app_id)
    
    return redirect(url_for('department_dashboard'))

@app.route('/department/reject/<int:app_id>', methods=['POST'])
def department_reject(app_id):
    if 'user_id' not in session or session['user_type'] not in ['department', 'admin_hr']:
        return redirect(url_for('login'))
    
    update_final_status(app_id, 'Rejected')
    
    return redirect(url_for('department_dashboard'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)



