from flask import Flask, render_template
from config.config import Config
from models.models import db
from flask_login import LoginManager
from routes.auth_routes import auth_bp
from routes.tpo_routes import tpo_bp
from routes.student_routes import student_bp
from routes.alumni_routes import alumni_bp
from routes.analyst_routes import analyst_bp
from routes.chatbot_routes import chatbot_bp
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

# Import User model for login manager
from models.models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Home page route
@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')

# Context processor for templates
@app.context_processor
def utility_processor():
    return {'now': datetime.now}

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(tpo_bp)
app.register_blueprint(student_bp)
app.register_blueprint(alumni_bp)
app.register_blueprint(analyst_bp)
app.register_blueprint(chatbot_bp)

# Create tables
with app.app_context():
    db.create_all()
    print("✅ Database tables created!")

if __name__ == '__main__':
    print("\n" + "="*50)
    print("🚀 Placement Pro Website Starting...")
    print("="*50)
    print("\n📱 Open your browser and go to: http://localhost:5000")
    print("\n💡 Test Accounts:")
    print("   - Student: username: student123, password: 123456")
    print("   - TPO: username: tpo123, password: 123456")
    print("   - Alumni: username: alumni123, password: 123456")
    print("\n🔑 Login Rules:")
    print("   - Username: letters and numbers only")
    print("   - Password: numbers only")
    print("\n" + "="*50)
    
    app.run(debug=True, host='0.0.0.0', port=5000)