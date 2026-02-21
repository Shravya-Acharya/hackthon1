from flask import Blueprint, render_template, request
from flask_login import login_required, current_user

analyst_bp = Blueprint('analyst', __name__, url_prefix='/analyst')

@analyst_bp.route('/skill-gap-analysis')
@login_required
def skill_gap_analysis():
    target_role = request.args.get('target_role', 'Data Analyst')
    
    skill_requirements = {
        'Data Analyst': ['Python', 'SQL', 'Excel', 'PowerBI', 'Tableau', 'Statistics'],
        'Software Developer': ['Python', 'Java', 'JavaScript', 'SQL', 'Data Structures', 'Algorithms'],
        'Web Developer': ['HTML', 'CSS', 'JavaScript', 'React', 'Node.js'],
        'Machine Learning': ['Python', 'TensorFlow', 'PyTorch', 'SQL', 'Statistics']
    }
    
    required = skill_requirements.get(target_role, [])
    
    if current_user.role == 'student' and current_user.skills:
        student_skills = [s.strip() for s in current_user.skills.split(',')]
        missing = [s for s in required if s not in student_skills]
    else:
        student_skills = []
        missing = required
    
    return render_template('analyst/skill_gap_analysis.html', 
                         target_role=target_role,
                         required=required,
                         student_skills=student_skills,
                         missing=missing)