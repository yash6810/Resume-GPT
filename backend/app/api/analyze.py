from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
from app.models.schemas import AnalyzeRequest, AnalyzeResponse
from app.services.scoring import analyze_resume

router = APIRouter()


class QuickScoreRequest(BaseModel):
    resume_text: str
    job_description: str


class QuickScoreResponse(BaseModel):
    ats_score: float
    matched_skills: List[str]
    missing_skills: List[str]
    recommendations: List[str]
    status: str


@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze_resume_endpoint(request: AnalyzeRequest):
    """
    Analyze resume against job description and return ATS score, missing skills, and recommendations.
    """
    # Validate input
    if not request.resume_text or not request.resume_text.strip():
        raise HTTPException(status_code=400, detail="Resume text is required")

    if not request.job_description or not request.job_description.strip():
        raise HTTPException(status_code=400, detail="Job description is required")

    try:
        result = analyze_resume(request.resume_text, request.job_description)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing resume: {str(e)}")


@router.post("/analyze/quick", response_model=QuickScoreResponse)
async def quick_score_endpoint(request: QuickScoreRequest):
    """
    Quick ATS score calculation (lightweight, for real-time updates).
    Returns score, matched/missing skills, and recommendations.
    """
    if not request.resume_text or not request.resume_text.strip():
        return QuickScoreResponse(
            ats_score=0,
            matched_skills=[],
            missing_skills=[],
            recommendations=[],
            status="no_resume",
        )

    if not request.job_description or not request.job_description.strip():
        return QuickScoreResponse(
            ats_score=0,
            matched_skills=[],
            missing_skills=[],
            recommendations=[],
            status="no_jd",
        )

    try:
        result = analyze_resume(request.resume_text, request.job_description)

        # Extract matched skill names
        matched_skills = [s.skill for s in result.skill_matches if s.type == "exact"]

        return QuickScoreResponse(
            ats_score=result.ats_score,
            matched_skills=matched_skills,
            missing_skills=result.missing_skills,
            recommendations=result.recommendations,
            status="ok",
        )
    except Exception as e:
        return QuickScoreResponse(
            ats_score=0,
            matched_skills=[],
            missing_skills=[],
            recommendations=[],
            status="error",
        )
