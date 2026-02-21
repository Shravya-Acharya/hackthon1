from flask import Blueprint, render_template, request, redirect, url_for
from models.models import db, User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Login page"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        role = request.form.get('role')
        
        user = User.query.filter_by(username=username, role=role).first()
        
        if user and check_password_hash(user.password, password):
            login_user(user)
            if role == 'tpo':
                return redirect(url_for('tpo.dashboard'))
            elif role == 'student':
                return redirect(url_for('student.dashboard'))
            elif role == 'alumni':
                return redirect(url_for('alumni.dashboard'))
            elif role == 'analyst':
                return redirect(url_for('analyst.skill_gap_analysis'))
        
        return '''
        <script>
            alert('Invalid username or password');
            window.location.href = '/login';
        </script>
        '''
    
    return render_template('auth/login.html')

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    """Signup page"""
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role')
        phone = request.form.get('phone')
        
        # Validation
        if not username.isalnum():
            return '<script>alert("Username must contain only letters and numbers"); window.location.href="/signup";</script>'
        
        if not password.isdigit():
            return '<script>alert("Password must contain only numbers"); window.location.href="/signup";</script>'
        
        if User.query.filter_by(username=username).first():
            return '<script>alert("Username already exists"); window.location.href="/signup";</script>'
        
        if User.query.filter_by(email=email).first():
            return '<script>alert("Email already registered"); window.location.href="/signup";</script>'
        
        # Create user
        new_user = User(
            username=username,
            email=email,
            password=generate_password_hash(password),
            role=role,
            phone=phone
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        return '<script>alert("Account created! Please login."); window.location.href="/login";</script>'
    
    return render_template('auth/signup.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))