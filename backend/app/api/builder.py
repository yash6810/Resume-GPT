from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from typing import List, Optional
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
import io

from app.services.templates import (
    build_resume_with_template,
    get_available_templates,
    get_all_industry_templates,
    get_industry_template,
    generate_industry_summary,
    get_industry_keywords,
    get_industry_skills,
    get_industry_bullet_templates,
)

router = APIRouter()


class ContactInfo(BaseModel):
    name: str
    email: str
    phone: str
    location: str
    linkedin: Optional[str] = None
    website: Optional[str] = None


class Experience(BaseModel):
    title: str
    company: str
    location: str
    start_date: str
    end_date: str
    bullets: List[str]


class Education(BaseModel):
    degree: str
    school: str
    location: str
    graduation_date: str
    gpa: Optional[str] = None


class ResumeBuilderRequest(BaseModel):
    contact: ContactInfo
    summary: Optional[str] = None
    skills: List[str] = []
    experience: List[Experience] = []
    education: List[Education] = []
    certifications: List[str] = []
    template: str = "modern"


@router.get("/builder/templates")
async def list_templates():
    """Return available resume templates."""
    return {"templates": get_available_templates()}


@router.get("/builder/industry-templates")
async def list_industry_templates():
    """Return available industry-specific templates."""
    templates = get_all_industry_templates()
    return {"templates": templates}


@router.get("/builder/industry-templates/{industry_id}")
async def get_industry_template_detail(industry_id: str):
    """Return details for a specific industry template."""
    template = get_industry_template(industry_id)
    if not template:
        raise HTTPException(
            status_code=404, detail=f"Industry template '{industry_id}' not found"
        )
    return {"template": template}


@router.get("/builder/industry-templates/{industry_id}/keywords")
async def get_industry_keywords_endpoint(industry_id: str):
    """Return recommended keywords for an industry."""
    keywords = get_industry_keywords(industry_id)
    if not keywords:
        raise HTTPException(
            status_code=404, detail=f"Industry template '{industry_id}' not found"
        )
    return {"industry_id": industry_id, "keywords": keywords}


@router.get("/builder/industry-templates/{industry_id}/skills")
async def get_industry_skills_endpoint(industry_id: str):
    """Return recommended skills categories for an industry."""
    skills = get_industry_skills(industry_id)
    if not skills:
        raise HTTPException(
            status_code=404, detail=f"Industry template '{industry_id}' not found"
        )
    return {"industry_id": industry_id, "skills_categories": skills}


@router.get("/builder/industry-templates/{industry_id}/bullets")
async def get_industry_bullets_endpoint(industry_id: str):
    """Return bullet point templates for an industry."""
    bullets = get_industry_bullet_templates(industry_id)
    if not bullets:
        raise HTTPException(
            status_code=404, detail=f"Industry template '{industry_id}' not found"
        )
    return {"industry_id": industry_id, "bullet_templates": bullets}


@router.post("/builder/industry-templates/{industry_id}/generate-summary")
async def generate_industry_summary_endpoint(
    industry_id: str, role: str = "", years_experience: int = 0, skills: List[str] = []
):
    """Generate an industry-specific summary."""
    summary = generate_industry_summary(industry_id, role, years_experience, skills)
    if not summary:
        raise HTTPException(
            status_code=404, detail=f"Industry template '{industry_id}' not found"
        )
    return {"industry_id": industry_id, "summary": summary}


@router.post("/builder/export")
async def build_resume(data: ResumeBuilderRequest):
    try:
        docx_bytes = build_resume_with_template(data)
        return StreamingResponse(
            io.BytesIO(docx_bytes),
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            headers={
                "Content-Disposition": f"attachment; filename=resume_{data.template}.docx"
            },
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error building resume: {str(e)}")


@router.post("/builder/text")
async def build_resume_text(data: ResumeBuilderRequest):
    """Return resume as plain text for preview."""
    try:
        lines = []
        lines.append(data.contact.name.upper())
        lines.append(
            " | ".join(
                filter(
                    None,
                    [
                        data.contact.email,
                        data.contact.phone,
                        data.contact.location,
                        data.contact.linkedin or "",
                        data.contact.website or "",
                    ],
                )
            )
        )
        lines.append("")

        if data.summary:
            lines.append("PROFESSIONAL SUMMARY")
            lines.append(data.summary)
            lines.append("")

        if data.skills:
            lines.append("SKILLS")
            lines.append(", ".join(data.skills))
            lines.append("")

        if data.experience:
            lines.append("EXPERIENCE")
            for exp in data.experience:
                lines.append(f"{exp.title}")
                lines.append(f"{exp.company} | {exp.location}")
                lines.append(f"{exp.start_date} - {exp.end_date}")
                for bullet in exp.bullets:
                    lines.append(f"- {bullet}")
                lines.append("")

        if data.education:
            lines.append("EDUCATION")
            for edu in data.education:
                lines.append(f"{edu.degree}")
                lines.append(f"{edu.school} | {edu.location}")
                lines.append(f"Graduated: {edu.graduation_date}")
                if edu.gpa:
                    lines[-1] += f" | GPA: {edu.gpa}"
                lines.append("")

        if data.certifications:
            lines.append("CERTIFICATIONS")
            for cert in data.certifications:
                lines.append(f"- {cert}")

        return {"text": "\n".join(lines), "template": data.template}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error generating preview: {str(e)}"
        )
