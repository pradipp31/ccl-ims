import sqlite3
import os

DATABASE = 'ccl_ims.db'

def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            user_type TEXT NOT NULL
        )
    ''')
    
    # Applications table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            cgpa REAL,
            skills TEXT,
            experience TEXT,
            status TEXT DEFAULT 'Pending',
            hr_approval_status TEXT DEFAULT 'Pending',
            FOREIGN KEY (student_id) REFERENCES users(id)
        )
    ''')
    
    # Notifications table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS notifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            user_type TEXT NOT NULL,
            message TEXT,
            is_read INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    
    # Internship details table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS internship_details (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            application_id INTEGER NOT NULL,
            start_date TEXT,
            stipend REAL,
            reporting_time TEXT,
            FOREIGN KEY (application_id) REFERENCES applications(id)
        )
    ''')
    
    conn.commit()
    conn.close()

# ==================== USER FUNCTIONS ====================

def get_user(email, password):
    """Get user by email and password"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE email = ? AND password = ?', (email, password))
    user = cursor.fetchone()
    conn.close()
    return user

def add_user(name, email, password, user_type):
    """Add new user"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO users (name, email, password, user_type) VALUES (?, ?, ?, ?)',
                       (name, email, password, user_type))
        conn.commit()
    except sqlite3.IntegrityError:
        pass  # Email already exists
    finally:
        conn.close()

# ==================== APPLICATION FUNCTIONS ====================

def get_applications(student_id=None):
    """Get applications - if student_id is None, get all"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    if student_id:
        cursor.execute('SELECT * FROM applications WHERE student_id = ?', (student_id,))
    else:
        cursor.execute('SELECT * FROM applications')
    applications = cursor.fetchall()
    conn.close()
    return applications

def add_application(student_id, cgpa, skills, experience):
    """Add new application"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO applications (student_id, cgpa, skills, experience) VALUES (?, ?, ?, ?)',
                   (student_id, cgpa, skills, experience))
    conn.commit()
    conn.close()

def update_application_status(app_id, status):
    """Update application status"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('UPDATE applications SET status = ? WHERE id = ?', (status, app_id))
    conn.commit()
    conn.close()

def get_approved_hr_applications():
    """Get applications approved by HR"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM applications WHERE hr_approval_status = ?', ('Approved',))
    applications = cursor.fetchall()
    conn.close()
    return applications

def get_selected_applications():
    """Get applications selected by department"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM applications WHERE status = ?', ('Selected',))
    applications = cursor.fetchall()
    conn.close()
    return applications

# ==================== NOTIFICATION FUNCTIONS ====================

def get_notifications(user_id, user_type):
    """Get all notifications for a user"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM notifications 
                      WHERE user_id = ? AND user_type = ? 
                      ORDER BY created_at DESC''',
                   (user_id, user_type))
    notifications = cursor.fetchall()
    conn.close()
    return notifications

def mark_notification_as_read(notification_id):
    """Mark single notification as read"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('UPDATE notifications SET is_read = 1 WHERE id = ?', (notification_id,))
    conn.commit()
    conn.close()

def mark_all_notifications_as_read(user_id, user_type):
    """Mark all notifications as read for a user"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('UPDATE notifications SET is_read = 1 WHERE user_id = ? AND user_type = ?',
                   (user_id, user_type))
    conn.commit()
    conn.close()

def get_unread_count_student(student_id):
    """Get unread notification count for student"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''SELECT COUNT(*) FROM notifications 
                      WHERE user_id = ? AND user_type = ? AND is_read = 0''',
                   (student_id, 'student'))
    count = cursor.fetchone()[0]
    conn.close()
    return count

def get_unread_count_hr_admin(hr_id):
    """Get unread notification count for HR admin"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''SELECT COUNT(*) FROM notifications 
                      WHERE user_id = ? AND user_type = ? AND is_read = 0''',
                   (hr_id, 'hr_admin'))
    count = cursor.fetchone()[0]
    conn.close()
    return count

# ==================== INTERNSHIP DETAILS FUNCTIONS ====================

def add_internship_details(app_id, start_date, stipend, reporting_time):
    """Add internship details for an application"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO internship_details 
                      (application_id, start_date, stipend, reporting_time) 
                      VALUES (?, ?, ?, ?)''',
                   (app_id, start_date, stipend, reporting_time))
    conn.commit()
    conn.close()

def get_internship_details(app_id):
    """Get internship details for an application"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM internship_details WHERE application_id = ?', (app_id,))
    details = cursor.fetchone()
    conn.close()
    return details






