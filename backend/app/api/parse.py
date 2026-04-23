from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.parser import extract_text_and_sections
from app.models.schemas import ParseResponse

router = APIRouter()


@router.post("/parse", response_model=ParseResponse)
async def parse_resume(resume: UploadFile = File(...)):
    """
    Parse uploaded resume file (PDF/DOCX) and extract text and sections.
    """
    # Validate file type
    if not resume.filename.lower().endswith((".pdf", ".docx")):
        raise HTTPException(
            status_code=400, detail="Only PDF and DOCX files are supported"
        )

    # Validate file size (5MB limit)
    content = await resume.read()
    if len(content) > 5 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File size exceeds 5MB limit")

    try:
        text, sections = extract_text_and_sections(content, resume.filename)
        return ParseResponse(text=text, sections=sections)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error parsing resume: {str(e)}")
