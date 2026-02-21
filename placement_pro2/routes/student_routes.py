from flask import Blueprint, render_template, request, redirect, url_for, send_file
from models.models import db, User, Drive, Application, Resume, JobReferral, MentorshipSlot
from flask_login import login_required, current_user
from datetime import datetime
from utils.pdf_utils import generate_resume_pdf

student_bp = Blueprint('student', __name__, url_prefix='/student')

@student_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'student':
        return redirect(url_for('index'))
    
    applications = Application.query.filter_by(student_id=current_user.id).all()
    return render_template('student/dashboard.html', applications=applications)

@student_bp.route('/build-resume', methods=['GET', 'POST'])
@login_required
def build_resume():
    if current_user.role != 'student':
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        data = {
            'full_name': request.form.get('full_name'),
            'email': request.form.get('email'),
            'phone': request.form.get('phone'),
            'skills': request.form.get('skills'),
            'projects': request.form.get('projects'),
            'cgpa': request.form.get('cgpa'),
            'branch': request.form.get('branch'),
            'institution': request.form.get('institution')
        }
        
        # Update user
        current_user.full_name = data['full_name']
        current_user.email = data['email']
        current_user.phone = data['phone']
        current_user.skills = data['skills']
        current_user.cgpa = float(data['cgpa']) if data['cgpa'] else None
        current_user.branch = data['branch']
        current_user.institution = data['institution']
        
        # Save resume
        resume = Resume(
            student_id=current_user.id,
            skills=data['skills'],
            projects=data['projects'],
            education=f"{data['branch']} from {data['institution']}, CGPA: {data['cgpa']}"
        )
        db.session.add(resume)
        db.session.commit()
        
        # Generate PDF
        filename = generate_resume_pdf(current_user, data)
        
        return send_file(filename, as_attachment=True, download_name=f"{data['full_name']}_resume.pdf")
    
    return render_template('student/build_resume.html')

@student_bp.route('/live-feed')
@login_required
def live_feed():
    if current_user.role != 'student':
        return redirect(url_for('index'))
    
    # Get eligible drives
    drives = Drive.query.filter(
        Drive.min_cgpa <= (current_user.cgpa or 0),
        Drive.max_backlogs >= (current_user.backlogs or 0)
    ).all()
    
    # Filter by branch
    eligible = []
    for drive in drives:
        if current_user.branch and current_user.branch in drive.branches.split(','):
            eligible.append(drive)
    
    return render_template('student/live_feed.html', drives=eligible)

@student_bp.route('/apply-drive/<int:drive_id>')
@login_required
def apply_drive(drive_id):
    if current_user.role != 'student':
        return redirect(url_for('index'))
    
    # Check if already applied
    existing = Application.query.filter_by(
        student_id=current_user.id,
        drive_id=drive_id
    ).first()
    
    if not existing:
        app = Application(
            student_id=current_user.id,
            drive_id=drive_id
        )
        db.session.add(app)
        db.session.commit()
    
    return redirect(url_for('student.live_feed'))

@student_bp.route('/application-tracker')
@login_required
def application_tracker():
    if current_user.role != 'student':
        return redirect(url_for('index'))
    
    applications = Application.query.filter_by(student_id=current_user.id).all()
    return render_template('student/application_tracker.html', applications=applications)

@student_bp.route('/job-referrals')
@login_required
def job_referrals():
    if current_user.role != 'student':
        return redirect(url_for('index'))
    
    referrals = JobReferral.query.all()
    return render_template('student/job_referrals.html', referrals=referrals)

@student_bp.route('/mentorship-slots')
@login_required
def mentorship_slots():
    if current_user.role != 'student':
        return redirect(url_for('index'))
    
    slots = MentorshipSlot.query.filter_by(is_booked=False).all()
    return render_template('student/mentorship_slots.html', slots=slots)

@student_bp.route('/book-slot/<int:slot_id>')
@login_required
def book_slot(slot_id):
    if current_user.role != 'student':
        return redirect(url_for('index'))
    
    slot = MentorshipSlot.query.get(slot_id)
    if slot and not slot.is_booked:
        slot.is_booked = True
        slot.booked_by = current_user.id
        db.session.commit()
    
    return redirect(url_for('student.mentorship_slots'))
