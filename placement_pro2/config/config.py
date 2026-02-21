import os

class Config:
    SECRET_KEY = 'your-secret-key-here-change-in-production'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(os.path.dirname(os.path.dirname(__file__)), 'instance', 'placement.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False