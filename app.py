import os
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from database import (
    init_db, get_user, add_user, get_applications, add_application,
    update_application_status, get_notifications, mark_notification_as_read,
    get_unread_count_student, get_unread_count_hr_admin, mark_all_notifications_as_read,
    get_approved_hr_applications, get_selected_applications, add_internship_details,
    get_internship_details
)
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this'

# Context processor for unread counts
@app.context_processor
def inject_unread_counts():
    unread_student = 0
    unread_hr = 0
    
    if 'user_id' in session:
        if session.get('user_type') == 'student':
            unread_student = get_unread_count_student(session['user_id'])
        elif session.get('user_type') == 'hr_admin':
            unread_hr = get_unread_count_hr_admin(session['user_id'])
    
    return dict(unread_student=unread_student, unread_hr=unread_hr)

# Initialize database
init_db()

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = get_user(email, password)
        
        if user:
            session['user_id'] = user[0]
            session['user_type'] = user[3]
            session['user_name'] = user[1]
            
            if user[3] == 'student':
                return redirect(url_for('student_dashboard'))
            elif user[3] == 'hr_admin':
                return redirect(url_for('hr_dashboard'))
            elif user[3] == 'department_officer':
                return redirect(url_for('department_dashboard'))
        else:
            return render_template('login.html', error='Invalid credentials')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        user_type = request.form['user_type']
        
        add_user(name, email, password, user_type)
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/student/dashboard')
def student_dashboard():
    if 'user_id' not in session or session['user_type'] != 'student':
        return redirect(url_for('login'))
    
    applications = get_applications(session['user_id'])
    return render_template('student_dashboard.html', applications=applications)

@app.route('/student/apply', methods=['GET', 'POST'])
def student_apply():
    if 'user_id' not in session or session['user_type'] != 'student':
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        cgpa = request.form['cgpa']
        skills = request.form['skills']
        experience = request.form['experience']
        
        add_application(session['user_id'], cgpa, skills, experience)
        return redirect(url_for('student_dashboard'))
    
    return render_template('my_application.html')

@app.route('/student/notifications')
def student_notifications():
    if 'user_id' not in session or session['user_type'] != 'student':
        return redirect(url_for('login'))
    
    mark_all_notifications_as_read(session['user_id'], 'student')
    notifications = get_notifications(session['user_id'], 'student')
    return render_template('notifications.html', notifications=notifications)

@app.route('/hr/dashboard')
def hr_dashboard():
    if 'user_id' not in session or session['user_type'] != 'hr_admin':
        return redirect(url_for('login'))
    
    pending_applications = get_applications(None)
    pending_applications = [app for app in pending_applications if app[5] == 'Pending']
    
    approved_applications = get_approved_hr_applications()
    
    return render_template('hr_dashboard.html', 
                         pending_applications=pending_applications,
                         approved_applications=approved_applications)

@app.route('/hr/approve/<int:app_id>', methods=['POST'])
def hr_approve(app_id):
    if 'user_id' not in session or session['user_type'] != 'hr_admin':
        return redirect(url_for('login'))
    
    update_application_status(app_id, 'Approved')
    return redirect(url_for('hr_dashboard'))

@app.route('/hr/reject/<int:app_id>', methods=['POST'])
def hr_reject(app_id):
    if 'user_id' not in session or session['user_type'] != 'hr_admin':
        return redirect(url_for('login'))
    
    update_application_status(app_id, 'Rejected')
    return redirect(url_for('hr_dashboard'))

@app.route('/hr/notifications')
def hr_notifications():
    if 'user_id' not in session or session['user_type'] != 'hr_admin':
        return redirect(url_for('login'))
    
    mark_all_notifications_as_read(session['user_id'], 'hr_admin')
    notifications = get_notifications(session['user_id'], 'hr_admin')
    return render_template('hr_notifications.html', notifications=notifications)

@app.route('/hr/add-internship-details', methods=['GET', 'POST'])
def hr_add_internship_details():
    if 'user_id' not in session or session['user_type'] != 'hr_admin':
        return redirect(url_for('login'))
    
    selected_applications = get_selected_applications()
    
    if request.method == 'POST':
        app_id = request.form['app_id']
        start_date = request.form['start_date']
        stipend = request.form['stipend']
        reporting_time = request.form['reporting_time']
        
        add_internship_details(app_id, start_date, stipend, reporting_time)
        return redirect(url_for('hr_dashboard'))
    
    return render_template('hr_manager_internship_details.html', 
                         selected_applications=selected_applications)

@app.route('/department/dashboard')
def department_dashboard():
    if 'user_id' not in session or session['user_type'] != 'department_officer':
        return redirect(url_for('login'))
    
    approved_applications = get_approved_hr_applications()
    return render_template('department_dashboard.html', 
                         approved_applications=approved_applications)

@app.route('/department/select/<int:app_id>', methods=['POST'])
def department_select(app_id):
    if 'user_id' not in session or session['user_type'] != 'department_officer':
        return redirect(url_for('login'))
    
    update_application_status(app_id, 'Selected')
    return redirect(url_for('department_dashboard'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)



