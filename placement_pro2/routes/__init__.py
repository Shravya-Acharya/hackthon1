# This file makes the routes directory a Python package
# Import all blueprints to make them available when importing from routes

from .auth_routes import auth_bp
from .tpo_routes import tpo_bp
from .student_routes import student_bp
from .alumni_routes import alumni_bp
from .analyst_routes import analyst_bp
from .chatbot_routes import chatbot_bp

__all__ = ['auth_bp', 'tpo_bp', 'student_bp', 'alumni_bp', 'analyst_bp', 'chatbot_bp']