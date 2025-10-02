from typing import Optional
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.pdfgen import canvas
from datetime import datetime
import tempfile
import os


class PDFService:
    """Service for generating PDF resumes in Canadian format"""

    @staticmethod
    def generate_canadian_cv_pdf(cv_data: dict) -> BytesIO:
        """Generate a Canadian-format CV PDF"""

        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=0.75*inch,
            leftMargin=0.75*inch,
            topMargin=0.75*inch,
            bottomMargin=0.75*inch
        )

        # Container for the 'Flowable' objects
        elements = []

        # Define styles
        styles = getSampleStyleSheet()

        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=20,
            textColor=colors.HexColor('#1a1a1a'),
            spaceAfter=6,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )

        contact_style = ParagraphStyle(
            'Contact',
            parent=styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#4a4a4a'),
            alignment=TA_CENTER,
            spaceAfter=12
        )

        section_title_style = ParagraphStyle(
            'SectionTitle',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#2c5aa0'),
            spaceAfter=10,
            spaceBefore=12,
            fontName='Helvetica-Bold',
            borderWidth=1,
            borderColor=colors.HexColor('#2c5aa0'),
            borderPadding=5,
            borderRadius=2
        )

        body_style = ParagraphStyle(
            'CustomBody',
            parent=styles['Normal'],
            fontSize=10,
            leading=14,
            textColor=colors.HexColor('#1a1a1a')
        )

        # Header - Name
        name = cv_data.get('full_name', 'Your Name')
        elements.append(Paragraph(name.upper(), title_style))

        # Contact Information
        contact_info = []
        if cv_data.get('email'):
            contact_info.append(cv_data['email'])
        if cv_data.get('phone'):
            contact_info.append(cv_data['phone'])
        if cv_data.get('location'):
            contact_info.append(cv_data['location'])

        contact_text = ' | '.join(contact_info)
        elements.append(Paragraph(contact_text, contact_style))
        elements.append(Spacer(1, 0.2*inch))

        # Professional Summary
        if cv_data.get('summary'):
            elements.append(Paragraph('PROFESSIONAL SUMMARY', section_title_style))
            elements.append(Paragraph(cv_data['summary'], body_style))
            elements.append(Spacer(1, 0.15*inch))

        # Core Skills
        if cv_data.get('skills'):
            elements.append(Paragraph('CORE COMPETENCIES', section_title_style))
            skills = cv_data['skills']
            if isinstance(skills, list):
                skills_text = ' • '.join(skills)
            else:
                skills_text = str(skills)
            elements.append(Paragraph(skills_text, body_style))
            elements.append(Spacer(1, 0.15*inch))

        # Work Experience
        if cv_data.get('experience'):
            elements.append(Paragraph('PROFESSIONAL EXPERIENCE', section_title_style))

            for exp in cv_data['experience']:
                # Company and Position
                position = exp.get('position', '')
                company = exp.get('company', '')
                job_title = f"<b>{position}</b> — {company}"
                elements.append(Paragraph(job_title, body_style))

                # Dates and Location
                start = exp.get('start_date', '')
                end = exp.get('end_date', 'Present')
                location = exp.get('location', '')
                date_loc = f"<i>{start} - {end}"
                if location:
                    date_loc += f" | {location}"
                date_loc += "</i>"
                elements.append(Paragraph(date_loc, body_style))
                elements.append(Spacer(1, 0.05*inch))

                # Responsibilities
                responsibilities = exp.get('responsibilities', [])
                for resp in responsibilities:
                    elements.append(Paragraph(f"• {resp}", body_style))

                # Achievements
                achievements = exp.get('achievements', [])
                if achievements:
                    for ach in achievements:
                        elements.append(Paragraph(f"✓ {ach}", body_style))

                elements.append(Spacer(1, 0.15*inch))

        # Education
        if cv_data.get('education'):
            elements.append(Paragraph('EDUCATION', section_title_style))

            for edu in cv_data['education']:
                degree = edu.get('degree', '')
                field = edu.get('field_of_study', '')
                institution = edu.get('institution', '')

                edu_title = f"<b>{degree} - {field}</b>"
                elements.append(Paragraph(edu_title, body_style))

                edu_info = institution
                grad_date = edu.get('graduation_date', '')
                if grad_date:
                    edu_info += f" | {grad_date}"

                elements.append(Paragraph(f"<i>{edu_info}</i>", body_style))

                if edu.get('honors'):
                    honors_text = ', '.join(edu['honors'])
                    elements.append(Paragraph(f"Honors: {honors_text}", body_style))

                elements.append(Spacer(1, 0.1*inch))

        # Certifications
        if cv_data.get('certifications'):
            elements.append(Paragraph('CERTIFICATIONS', section_title_style))

            for cert in cv_data['certifications']:
                cert_name = cert.get('name', '')
                org = cert.get('issuing_organization', '')
                date = cert.get('issue_date', '')

                cert_text = f"<b>{cert_name}</b> — {org}"
                if date:
                    cert_text += f" ({date})"

                elements.append(Paragraph(cert_text, body_style))

            elements.append(Spacer(1, 0.1*inch))

        # Languages
        if cv_data.get('languages'):
            elements.append(Paragraph('LANGUAGES', section_title_style))

            lang_list = []
            for lang in cv_data['languages']:
                lang_name = lang.get('language', '')
                proficiency = lang.get('proficiency', '')
                lang_list.append(f"{lang_name} ({proficiency})")

            lang_text = ' | '.join(lang_list)
            elements.append(Paragraph(lang_text, body_style))
            elements.append(Spacer(1, 0.1*inch))

        # Build PDF
        doc.build(elements)

        # Get the value of the BytesIO buffer and return it
        buffer.seek(0)
        return buffer

    @staticmethod
    def save_pdf_to_file(buffer: BytesIO, filename: str) -> str:
        """Save PDF buffer to a file"""
        with open(filename, 'wb') as f:
            f.write(buffer.getvalue())
        return filename

    @staticmethod
    def generate_temp_pdf(cv_data: dict) -> str:
        """Generate a temporary PDF file"""
        buffer = PDFService.generate_canadian_cv_pdf(cv_data)

        # Create temp file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
        temp_file.write(buffer.getvalue())
        temp_file.close()

        return temp_file.name


pdf_service = PDFService()
