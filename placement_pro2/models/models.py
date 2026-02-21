from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # tpo, student, alumni, analyst
    phone = db.Column(db.String(15))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Student specific fields
    full_name = db.Column(db.String(100))
    branch = db.Column(db.String(50))
    cgpa = db.Column(db.Float)
    backlogs = db.Column(db.Integer, default=0)
    skills = db.Column(db.Text)
    institution = db.Column(db.String(200))
    graduation_year = db.Column(db.Integer)

class Drive(db.Model):
    __tablename__ = 'drives'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    company = db.Column(db.String(100), nullable=False)
    min_cgpa = db.Column(db.Float, nullable=False)
    max_backlogs = db.Column(db.Integer, nullable=False, default=0)
    branches = db.Column(db.String(200), nullable=False)
    drive_date = db.Column(db.DateTime, nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Application(db.Model):
    __tablename__ = 'applications'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    drive_id = db.Column(db.Integer, db.ForeignKey('drives.id'), nullable=False)
    status = db.Column(db.String(50), default='Applied')
    applied_date = db.Column(db.DateTime, default=datetime.utcnow)
    interview_date = db.Column(db.DateTime)

class Resume(db.Model):
    __tablename__ = 'resumes'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    skills = db.Column(db.Text)
    projects = db.Column(db.Text)
    education = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class JobReferral(db.Model):
    __tablename__ = 'job_referrals'
    
    id = db.Column(db.Integer, primary_key=True)
    alumni_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    company = db.Column(db.String(100), nullable=False)
    position = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    apply_link = db.Column(db.String(200))
    posted_date = db.Column(db.DateTime, default=datetime.utcnow)

class MentorshipSlot(db.Model):
    __tablename__ = 'mentorship_slots'
    
    id = db.Column(db.Integer, primary_key=True)
    alumni_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    topic = db.Column(db.String(200))
    booked_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    is_booked = db.Column(db.Boolean, default=False)