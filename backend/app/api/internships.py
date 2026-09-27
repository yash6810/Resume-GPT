from fastapi import APIRouter
from app.models.internship_schemas import JobMatchRequest, JobMatchResponse
from app.services.internship_matcher import match_job

router = APIRouter(prefix="/internships", tags=["InternshipOS"])


@router.post("/match", response_model=JobMatchResponse)
async def match_internship(data: JobMatchRequest):
    return match_job(data.candidate, data.job)


@router.get("/health")
async def internship_health():
    return {"status": "healthy", "module": "internshipos"}
