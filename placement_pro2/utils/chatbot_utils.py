import re

def get_chatbot_response(message):
    """Simple chatbot responses"""
    message = message.lower().strip()
    
    if re.search(r'hello|hi|hey', message):
        return "Hello! I'm PlacementBot. How can I help you today?"
    
    if re.search(r'drive|company|placement', message):
        return "Placement drives are announced by the TPO. Check your dashboard for upcoming drives!"
    
    if re.search(r'eligib|criteria|cutoff|cgpa|backlog', message):
        return "Eligibility criteria varies by company. Usually need 7.0+ CGPA and no backlogs."
    
    if re.search(r'resume|build|cv', message):
        return "Use Resume Wizard in Student Dashboard to build your resume!"
    
    if re.search(r'interview|schedule', message):
        return "Interview schedules are in your Application Tracker."
    
    if re.search(r'alumni|referral', message):
        return "Check Alumni section for job referrals from seniors!"
    
    if re.search(r'contact|tpo|office', message):
        return "Contact Placement Office: placement@xyzcollege.edu or +91-1234567890"
    
    if re.search(r'login|signup', message):
        return "Use Login/Signup buttons on top right corner!"
    
    return "I can help with: drives, eligibility, resume, interviews, alumni, contact info. What do you need?"