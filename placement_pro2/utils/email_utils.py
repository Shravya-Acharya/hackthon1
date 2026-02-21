def send_email_notification(to_email, subject, body):
    """Simple email function (prints to console for testing)"""
    print(f"\n📧 EMAIL SENT:")
    print(f"To: {to_email}")
    print(f"Subject: {subject}")
    print(f"Body: {body}\n")
    return True