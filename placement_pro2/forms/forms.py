from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, FloatField, IntegerField, DateField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, NumberRange, Regexp

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Regexp('^[a-zA-Z0-9]+$', message="Only letters and numbers")])
    password = PasswordField('Password', validators=[DataRequired(), Regexp('^[0-9]+$', message="Only numbers")])
    role = SelectField('Role', choices=[('tpo', 'TPO'), ('student', 'Student'), ('alumni', 'Alumni'), ('analyst', 'Analyst')])

class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Regexp('^[a-zA-Z0-9]+$')])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Regexp('^[0-9]+$')])
    phone = StringField('Phone')
    role = SelectField('Role', choices=[('student', 'Student'), ('alumni', 'Alumni'), ('tpo', 'TPO'), ('analyst', 'Analyst')])

class DriveForm(FlaskForm):
    drive_name = StringField('Drive Name', validators=[DataRequired()])
    company = StringField('Company', validators=[DataRequired()])
    min_cgpa = FloatField('Minimum CGPA', validators=[DataRequired(), NumberRange(min=0, max=10)])
    backlogs_allowed = IntegerField('Backlogs Allowed', validators=[DataRequired(), NumberRange(min=0)])
    branches = StringField('Branches (comma separated)', validators=[DataRequired()])
    drive_date = DateField('Drive Date', validators=[DataRequired()])