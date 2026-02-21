from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
from models.models import db, Drive, User
from flask_login import login_required, current_user
from datetime import datetime
from utils.email_utils import send_email_notification

tpo_bp = Blueprint('tpo', __name__, url_prefix='/tpo')

def get_eligible_students(min_cgpa, max_backlogs, branches):
    """Get list of eligible students"""
    students = User.query.filter_by(role='student').all()
    eligible = []
    branch_list = [b.strip() for b in branches.split(',')]
    for student in students:
        if (student.cgpa and student.cgpa >= min_cgpa and 
            student.backlogs <= max_backlogs and 
            student.branch in branch_list):
            eligible.append(student)
    return eligible

@tpo_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'tpo':
        return redirect(url_for('index'))
    
    drives = Drive.query.filter_by(created_by=current_user.id).all()
    return render_template('tpo/dashboard.html', drives=drives)

@tpo_bp.route('/criteria-engine', methods=['GET', 'POST'])
@login_required
def criteria_engine():
    if current_user.role != 'tpo':
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        drive_name = request.form.get('drive_name')
        company = request.form.get('company')
        min_cgpa = float(request.form.get('min_cgpa'))
        backlogs = int(request.form.get('backlogs_allowed'))
        branches = request.form.get('branches')
        drive_date = datetime.strptime(request.form.get('drive_date'), '%Y-%m-%d')
        
        # Create drive
        drive = Drive(
            name=drive_name,
            company=company,
            min_cgpa=min_cgpa,
            max_backlogs=backlogs,
            branches=branches,
            drive_date=drive_date,
            created_by=current_user.id
        )
        db.session.add(drive)
        db.session.commit()
        
        # Get eligible students
        eligible = get_eligible_students(min_cgpa, backlogs, branches)
        
        # Store in session
        session['current_drive_id'] = drive.id
        session['eligible_students'] = [s.id for s in eligible]
        
        return render_template('tpo/eligibility_result.html', 
                             eligible_count=len(eligible), 
                             drive_id=drive.id)
    
    return render_template('tpo/criteria_engine.html')

@tpo_bp.route('/notify-eligible')
@login_required
def notify_eligible():
    if current_user.role != 'tpo':
        return jsonify({'error': 'Access denied'})
    
    drive_id = session.get('current_drive_id')
    student_ids = session.get('eligible_students', [])
    
    if not drive_id or not student_ids:
        return jsonify({'message': 'No eligible students found'})
    
    drive = Drive.query.get(drive_id)
    students = User.query.filter(User.id.in_(student_ids)).all()
    
    for student in students:
        send_email_notification(
            student.email,
            f"Eligible for {drive.name} Drive",
            f"You are eligible for {drive.name} drive at {drive.company} on {drive.drive_date.strftime('%Y-%m-%d')}"
        )
    
    return jsonify({'message': f'Notified {len(students)} students'})

@tpo_bp.route('/calendar')
@login_required
def calendar():
    return render_template('tpo/calendar.html')