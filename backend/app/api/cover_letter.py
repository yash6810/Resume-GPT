from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from app.models.schemas import CoverLetterRequest, CoverLetterResponse
from app.services.cover_letter import generate_cover_letter, create_cover_letter_docx
import io

router = APIRouter()


@router.post("/cover-letter/generate", response_model=CoverLetterResponse)
async def generate_cover_letter_endpoint(request: CoverLetterRequest):
    """
    Generate a cover letter based on resume text and job description.
    """
    if not request.resume_text or not request.resume_text.strip():
        raise HTTPException(status_code=400, detail="Resume text is required")

    if not request.job_description or not request.job_description.strip():
        raise HTTPException(status_code=400, detail="Job description is required")

    if not request.company_name or not request.company_name.strip():
        raise HTTPException(status_code=400, detail="Company name is required")

    if not request.position or not request.position.strip():
        raise HTTPException(status_code=400, detail="Position is required")

    try:
        cover_letter = generate_cover_letter(
            request.resume_text,
            request.job_description,
            request.company_name,
            request.position,
        )

        return CoverLetterResponse(
            cover_letter=cover_letter,
            message="Cover letter generated successfully",
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error generating cover letter: {str(e)}"
        )


@router.post("/cover-letter/export")
async def export_cover_letter_endpoint(request: CoverLetterRequest):
    """
    Generate and export a cover letter as DOCX.
    """
    if not request.resume_text or not request.resume_text.strip():
        raise HTTPException(status_code=400, detail="Resume text is required")

    if not request.job_description or not request.job_description.strip():
        raise HTTPException(status_code=400, detail="Job description is required")

    if not request.company_name or not request.company_name.strip():
        raise HTTPException(status_code=400, detail="Company name is required")

    if not request.position or not request.position.strip():
        raise HTTPException(status_code=400, detail="Position is required")

    try:
        cover_letter = generate_cover_letter(
            request.resume_text,
            request.job_description,
            request.company_name,
            request.position,
        )

        # Get applicant name from resume (simple extraction)
        first_line = request.resume_text.strip().split("\n")[0]
        applicant_name = first_line if len(first_line) < 50 else "Applicant"

        docx_bytes = create_cover_letter_docx(cover_letter, applicant_name)

        return StreamingResponse(
            io.BytesIO(docx_bytes),
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            headers={"Content-Disposition": "attachment; filename=cover_letter.docx"},
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error exporting cover letter: {str(e)}"
        )
