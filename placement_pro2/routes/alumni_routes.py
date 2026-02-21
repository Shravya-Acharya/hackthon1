from flask import Blueprint, render_template, request, redirect, url_for
from models.models import db, JobReferral, MentorshipSlot, User
from flask_login import login_required, current_user
from datetime import datetime

alumni_bp = Blueprint('alumni', __name__, url_prefix='/alumni')

@alumni_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'alumni':
        return redirect(url_for('index'))
    
    referrals = JobReferral.query.filter_by(alumni_id=current_user.id).all()
    slots = MentorshipSlot.query.filter_by(alumni_id=current_user.id).all()
    
    return render_template('alumni/dashboard.html', referrals=referrals, slots=slots)

@alumni_bp.route('/post-referral', methods=['GET', 'POST'])
@login_required
def post_referral():
    if current_user.role != 'alumni':
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        referral = JobReferral(
            alumni_id=current_user.id,
            company=request.form.get('company'),
            position=request.form.get('position'),
            description=request.form.get('description'),
            apply_link=request.form.get('apply_link')
        )
        db.session.add(referral)
        db.session.commit()
        return redirect(url_for('alumni.dashboard'))
    
    return render_template('alumni/post_referral.html')

@alumni_bp.route('/create-mentorship', methods=['GET', 'POST'])
@login_required
def create_mentorship():
    if current_user.role != 'alumni':
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        slot = MentorshipSlot(
            alumni_id=current_user.id,
            date=datetime.strptime(request.form.get('date'), '%Y-%m-%d'),
            topic=request.form.get('topic')
        )
        db.session.add(slot)
        db.session.commit()
        return redirect(url_for('alumni.dashboard'))
    
    return render_template('alumni/create_mentorship.html')