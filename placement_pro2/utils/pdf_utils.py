from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

def generate_resume_pdf(user, resume_data):
    """Generate PDF resume"""
    filename = f"resume_{user.username}.pdf"
    
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=20,
        alignment=1
    )
    
    # Add content
    story.append(Paragraph("XYZ College of Engineering", title_style))
    story.append(Spacer(1, 0.2*inch))
    story.append(Paragraph(f"<b>{resume_data.get('full_name', user.username)}</b>", styles['Heading2']))
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph(f"Email: {resume_data.get('email', user.email)}", styles['Normal']))
    story.append(Paragraph(f"Phone: {resume_data.get('phone', user.phone)}", styles['Normal']))
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("<b>EDUCATION</b>", styles['Heading3']))
    story.append(Paragraph(f"{resume_data.get('branch', '')} - CGPA: {resume_data.get('cgpa', '')}", styles['Normal']))
    story.append(Paragraph(resume_data.get('institution', ''), styles['Normal']))
    story.append(Spacer(1, 0.1*inch))
    
    story.append(Paragraph("<b>SKILLS</b>", styles['Heading3']))
    story.append(Paragraph(resume_data.get('skills', ''), styles['Normal']))
    story.append(Spacer(1, 0.1*inch))
    
    story.append(Paragraph("<b>PROJECTS</b>", styles['Heading3']))
    story.append(Paragraph(resume_data.get('projects', ''), styles['Normal']))
    
    doc.build(story)
    return filename