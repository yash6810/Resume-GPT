from fpdf import FPDF
from typing import List, Dict, Any
import io


class ResumePDF(FPDF):
    """Custom PDF class for resume generation."""

    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=15)

    def header(self):
        pass

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f"Page {self.page_no()}", 0, 0, "C")


def create_resume_pdf(
    contact: Dict[str, Any],
    summary: str = None,
    skills: List[str] = None,
    experience: List[Dict[str, Any]] = None,
    education: List[Dict[str, Any]] = None,
    certifications: List[str] = None,
) -> bytes:
    """Create a PDF resume from the provided data."""
    pdf = ResumePDF()
    pdf.add_page()

    # Contact Information
    pdf.set_font("Helvetica", "B", 20)
    pdf.set_text_color(44, 62, 80)
    pdf.cell(0, 12, contact.get("name", "Resume"), ln=True, align="C")

    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(100, 100, 100)

    contact_parts = []
    if contact.get("email"):
        contact_parts.append(contact["email"])
    if contact.get("phone"):
        contact_parts.append(contact["phone"])
    if contact.get("location"):
        contact_parts.append(contact["location"])
    if contact.get("linkedin"):
        contact_parts.append(contact["linkedin"])
    if contact.get("website"):
        contact_parts.append(contact["website"])

    if contact_parts:
        pdf.cell(0, 6, " | ".join(contact_parts), ln=True, align="C")

    pdf.ln(5)
    pdf.set_draw_color(102, 126, 234)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(8)

    # Summary
    if summary:
        pdf.set_font("Helvetica", "B", 12)
        pdf.set_text_color(44, 62, 80)
        pdf.cell(0, 8, "PROFESSIONAL SUMMARY", ln=True)

        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(51, 51, 51)
        pdf.multi_cell(0, 5, summary)
        pdf.ln(5)

    # Skills
    if skills:
        pdf.set_font("Helvetica", "B", 12)
        pdf.set_text_color(44, 62, 80)
        pdf.cell(0, 8, "SKILLS", ln=True)

        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(51, 51, 51)
        pdf.multi_cell(0, 5, " • ".join(skills))
        pdf.ln(5)

    # Experience
    if experience:
        pdf.set_font("Helvetica", "B", 12)
        pdf.set_text_color(44, 62, 80)
        pdf.cell(0, 8, "EXPERIENCE", ln=True)

        for exp in experience:
            pdf.set_font("Helvetica", "B", 11)
            pdf.set_text_color(44, 62, 80)
            pdf.cell(0, 6, exp.get("title", ""), ln=True)

            pdf.set_font("Helvetica", "", 10)
            pdf.set_text_color(52, 152, 219)
            company_location = f"{exp.get('company', '')} | {exp.get('location', '')}"
            pdf.cell(0, 5, company_location, ln=True)

            pdf.set_font("Helvetica", "I", 10)
            pdf.set_text_color(100, 100, 100)
            pdf.cell(
                0,
                5,
                f"{exp.get('start_date', '')} - {exp.get('end_date', '')}",
                ln=True,
            )

            if exp.get("bullets"):
                pdf.set_font("Helvetica", "", 10)
                pdf.set_text_color(51, 51, 51)
                for bullet in exp["bullets"]:
                    pdf.cell(5)
                    pdf.cell(5, 5, chr(8226))  # Bullet character
                    pdf.multi_cell(0, 5, bullet)

            pdf.ln(3)

    # Education
    if education:
        pdf.set_font("Helvetica", "B", 12)
        pdf.set_text_color(44, 62, 80)
        pdf.cell(0, 8, "EDUCATION", ln=True)

        for edu in education:
            pdf.set_font("Helvetica", "B", 11)
            pdf.set_text_color(44, 62, 80)
            pdf.cell(0, 6, edu.get("degree", ""), ln=True)

            pdf.set_font("Helvetica", "", 10)
            pdf.set_text_color(52, 152, 219)
            school_location = f"{edu.get('school', '')} | {edu.get('location', '')}"
            pdf.cell(0, 5, school_location, ln=True)

            pdf.set_font("Helvetica", "I", 10)
            pdf.set_text_color(100, 100, 100)
            date_text = f"Graduated: {edu.get('graduation_date', '')}"
            if edu.get("gpa"):
                date_text += f" | GPA: {edu['gpa']}"
            pdf.cell(0, 5, date_text, ln=True)

            pdf.ln(2)

    # Certifications
    if certifications:
        pdf.set_font("Helvetica", "B", 12)
        pdf.set_text_color(44, 62, 80)
        pdf.cell(0, 8, "CERTIFICATIONS", ln=True)

        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(51, 51, 51)
        for cert in certifications:
            pdf.cell(5)
            pdf.cell(5, 5, chr(8226))
            pdf.cell(0, 5, cert, ln=True)

    # Return PDF as bytes
    return pdf.output()


def create_cover_letter_pdf(
    cover_letter_text: str, applicant_name: str = "Applicant"
) -> bytes:
    """Create a PDF cover letter."""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=20)

    # Set margins
    pdf.set_left_margin(25)
    pdf.set_right_margin(25)

    # Title
    pdf.set_font("Helvetica", "B", 14)
    pdf.set_text_color(44, 62, 80)
    pdf.cell(0, 10, "Cover Letter", ln=True, align="C")
    pdf.ln(10)

    # Content
    pdf.set_font("Helvetica", "", 11)
    pdf.set_text_color(51, 51, 51)

    paragraphs = cover_letter_text.strip().split("\n\n")
    for para in paragraphs:
        if para.strip():
            pdf.multi_cell(0, 6, para.strip())
            pdf.ln(4)

    return pdf.output()
