import pdfminer.high_level
import docx
import re
from typing import Dict, Tuple, List
import io


def extract_text_and_sections(
    content: bytes, filename: str
) -> Tuple[str, Dict[str, str]]:
    """Extract text and sections from a resume file."""

    if filename.lower().endswith(".pdf"):
        text = extract_pdf_text(content)
    elif filename.lower().endswith(".docx"):
        text = extract_docx_text(content)
    else:
        raise ValueError("Unsupported file format. Please upload PDF or DOCX.")

    sections = split_sections(text)
    return text, sections


def extract_pdf_text(content: bytes) -> str:
    """Extract text from PDF content."""
    try:
        with io.BytesIO(content) as f:
            text = pdfminer.high_level.extract_text(f)
        return text.strip()
    except Exception as e:
        raise ValueError(f"Error extracting PDF text: {str(e)}")


def extract_docx_text(content: bytes) -> str:
    """Extract text from DOCX content."""
    try:
        with io.BytesIO(content) as f:
            doc = docx.Document(f)
            text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        return text.strip()
    except Exception as e:
        raise ValueError(f"Error extracting DOCX text: {str(e)}")


def split_sections(text: str) -> Dict[str, str]:
    """Split resume text into sections based on common heading keywords."""

    section_keywords = {
        "experience": [
            "experience",
            "work experience",
            "employment history",
            "professional experience",
        ],
        "education": ["education", "academic background", "qualifications"],
        "skills": ["skills", "technical skills", "competencies", "expertise"],
        "summary": ["summary", "professional summary", "profile", "objective"],
        "projects": ["projects", "personal projects", "portfolio"],
        "certifications": ["certifications", "certificates", "licenses"],
        "awards": ["awards", "achievements", "honors"],
        "publications": ["publications", "papers", "research"],
    }

    sections = {}
    lines = text.split("\n")
    current_section = "other"
    current_content = []

    for line in lines:
        line_lower = line.lower().strip()

        # Check if line is a section header
        found_section = False
        for section_name, keywords in section_keywords.items():
            for keyword in keywords:
                if line_lower.startswith(keyword) or line_lower == keyword:
                    if current_section != "other" and current_content:
                        sections[current_section] = "\n".join(current_content)

                    current_section = section_name
                    current_content = []
                    found_section = True
                    break
            if found_section:
                break

        if not found_section:
            current_content.append(line)

    # Add the last section
    if current_section != "other" and current_content:
        sections[current_section] = "\n".join(current_content)

    # If no sections were found, put everything in 'other'
    if not sections:
        sections["other"] = text

    return sections
