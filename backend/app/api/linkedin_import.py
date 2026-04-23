from fastapi import APIRouter, HTTPException

from app.models.schemas import LinkedInImportRequest, LinkedInImportResponse
from app.services.linkedin_import import parse_linkedin_profile, format_linkedin_import

router = APIRouter()


@router.post("/linkedin-import", response_model=LinkedInImportResponse)
async def import_linkedin_profile(data: LinkedInImportRequest):
    """Parse LinkedIn profile text and extract structured data."""
    try:
        parsed = parse_linkedin_profile(data.profile_text)
        formatted = format_linkedin_import(parsed)

        return LinkedInImportResponse(
            contact=parsed["contact"],
            summary=parsed["summary"],
            skills=parsed["skills"],
            experience=parsed["experience"],
            education=parsed["education"],
            certifications=parsed["certifications"],
            formatted_text=formatted,
        )

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error parsing LinkedIn profile: {str(e)}"
        )
