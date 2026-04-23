"""
ATS Simulator API Endpoints - Platform-specific resume analysis.

Provides endpoints to simulate how different ATS systems parse and score resumes.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict

from app.services.ats_simulator import (
    analyze_platform_ats,
    get_platform_config,
    get_all_platforms,
    multi_platform_analysis,
    simulate_linkedin_parsing,
    simulate_indeed_parsing,
    simulate_greenhouse_parsing,
    simulate_glassdoor_parsing,
    simulate_monster_parsing,
    simulate_lever_parsing,
)

router = APIRouter()


class ATSAnalyzeRequest(BaseModel):
    resume_text: str
    job_description: str


class ATSPlatformAnalyzeRequest(BaseModel):
    resume_text: str
    job_description: str
    file_size_bytes: Optional[int] = 0
    file_extension: Optional[str] = "pdf"


class ATSMultiPlatformRequest(BaseModel):
    resume_text: str
    job_description: str


@router.get("/platforms")
async def list_platforms():
    """
    List all supported ATS platforms with their configurations.
    """
    platforms = get_all_platforms()

    return {
        "platforms": [
            {
                "key": key,
                "name": config.name,
                "keyword_weight": config.keyword_weight,
                "role_match_weight": config.role_match_weight,
                "formatting_weight": config.formatting_weight,
                "max_file_size_mb": config.max_file_size_mb,
                "accepted_formats": config.accepted_formats,
                "focus_areas": config.focus_areas,
            }
            for key, config in platforms.items()
        ]
    }


@router.get("/platforms/{platform}")
async def get_platform_info(platform: str):
    """
    Get detailed information about a specific platform.
    """
    config = get_platform_config(platform)
    if not config:
        raise HTTPException(
            status_code=404,
            detail=f"Platform '{platform}' not found. Available: linkedin, indeed, greenhouse",
        )

    return {
        "key": platform.lower(),
        "name": config.name,
        "keyword_weight": config.keyword_weight,
        "role_match_weight": config.role_match_weight,
        "formatting_weight": config.formatting_weight,
        "max_file_size_mb": config.max_file_size_mb,
        "accepted_formats": config.accepted_formats,
        "focus_areas": config.focus_areas,
        "bonus_keywords": config.bonus_keywords,
        "penalty_keywords": config.penalty_keywords,
    }


@router.post("/linkedin")
async def analyze_linkedin(request: ATSPlatformAnalyzeRequest):
    """
    Analyze resume for LinkedIn application tracking system.
    Returns LinkedIn-specific scoring and recommendations.
    """
    if not request.resume_text or not request.resume_text.strip():
        raise HTTPException(status_code=400, detail="Resume text is required")

    if not request.job_description or not request.job_description.strip():
        raise HTTPException(status_code=400, detail="Job description is required")

    try:
        result = analyze_platform_ats(
            request.resume_text, request.job_description, "linkedin"
        )

        parsing_simulation = simulate_linkedin_parsing(request.resume_text)
        result["parsing_simulation"] = parsing_simulation

        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing resume: {str(e)}")


@router.post("/indeed")
async def analyze_indeed(request: ATSPlatformAnalyzeRequest):
    """
    Analyze resume for Indeed application system.
    Returns Indeed-specific scoring and recommendations.
    """
    if not request.resume_text or not request.resume_text.strip():
        raise HTTPException(status_code=400, detail="Resume text is required")

    if not request.job_description or not request.job_description.strip():
        raise HTTPException(status_code=400, detail="Job description is required")

    try:
        result = analyze_platform_ats(
            request.resume_text, request.job_description, "indeed"
        )

        parsing_simulation = simulate_indeed_parsing(request.resume_text)
        result["parsing_simulation"] = parsing_simulation

        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing resume: {str(e)}")


@router.post("/greenhouse")
async def analyze_greenhouse(request: ATSPlatformAnalyzeRequest):
    """
    Analyze resume for Greenhouse ATS.
    Returns Greenhouse-specific scoring with DEI and culture fit analysis.
    """
    if not request.resume_text or not request.resume_text.strip():
        raise HTTPException(status_code=400, detail="Resume text is required")

    if not request.job_description or not request.job_description.strip():
        raise HTTPException(status_code=400, detail="Job description is required")

    try:
        result = analyze_platform_ats(
            request.resume_text, request.job_description, "greenhouse"
        )

        parsing_simulation = simulate_greenhouse_parsing(request.resume_text)
        result["parsing_simulation"] = parsing_simulation

        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing resume: {str(e)}")


@router.post("/glassdoor")
async def analyze_glassdoor(request: ATSPlatformAnalyzeRequest):
    """
    Analyze resume for Glassdoor applications.
    Returns Glassdoor-specific scoring with company reputation focus.
    """
    if not request.resume_text or not request.resume_text.strip():
        raise HTTPException(status_code=400, detail="Resume text is required")

    if not request.job_description or not request.job_description.strip():
        raise HTTPException(status_code=400, detail="Job description is required")

    try:
        result = analyze_platform_ats(
            request.resume_text, request.job_description, "glassdoor"
        )

        parsing_simulation = simulate_glassdoor_parsing(request.resume_text)
        result["parsing_simulation"] = parsing_simulation

        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing resume: {str(e)}")


@router.post("/monster")
async def analyze_monster(request: ATSPlatformAnalyzeRequest):
    """
    Analyze resume for Monster job applications.
    Returns Monster-specific scoring with standard ATS formatting focus.
    """
    if not request.resume_text or not request.resume_text.strip():
        raise HTTPException(status_code=400, detail="Resume text is required")

    if not request.job_description or not request.job_description.strip():
        raise HTTPException(status_code=400, detail="Job description is required")

    try:
        result = analyze_platform_ats(
            request.resume_text, request.job_description, "monster"
        )

        parsing_simulation = simulate_monster_parsing(request.resume_text)
        result["parsing_simulation"] = parsing_simulation

        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing resume: {str(e)}")


@router.post("/lever")
async def analyze_lever(request: ATSPlatformAnalyzeRequest):
    """
    Analyze resume for Lever applications.
    Returns Lever-specific scoring with culture fit and values focus.
    """
    if not request.resume_text or not request.resume_text.strip():
        raise HTTPException(status_code=400, detail="Resume text is required")

    if not request.job_description or not request.job_description.strip():
        raise HTTPException(status_code=400, detail="Job description is required")

    try:
        result = analyze_platform_ats(
            request.resume_text, request.job_description, "lever"
        )

        parsing_simulation = simulate_lever_parsing(request.resume_text)
        result["parsing_simulation"] = parsing_simulation

        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing resume: {str(e)}")


@router.post("/analyze")
async def analyze_multi_platform(request: ATSMultiPlatformRequest):
    """
    Analyze resume across all supported platforms.
    Returns comparison results showing which platform is best for this resume.
    """
    if not request.resume_text or not request.resume_text.strip():
        raise HTTPException(status_code=400, detail="Resume text is required")

    if not request.job_description or not request.job_description.strip():
        raise HTTPException(status_code=400, detail="Job description is required")

    try:
        result = multi_platform_analysis(request.resume_text, request.job_description)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing resume: {str(e)}")


@router.post("/parse-simulation/{platform}")
async def simulate_parsing(platform: str, resume_text: str):
    """
    Simulate how a specific platform would parse the resume.
    Returns extracted information and parsing details.
    """
    if not resume_text or not resume_text.strip():
        raise HTTPException(status_code=400, detail="Resume text is required")

    platform = platform.lower()

    if platform == "linkedin":
        return simulate_linkedin_parsing(resume_text)
    elif platform == "indeed":
        return simulate_indeed_parsing(resume_text)
    elif platform == "greenhouse":
        return simulate_greenhouse_parsing(resume_text)
    elif platform == "glassdoor":
        return simulate_glassdoor_parsing(resume_text)
    elif platform == "monster":
        return simulate_monster_parsing(resume_text)
    elif platform == "lever":
        return simulate_lever_parsing(resume_text)
    else:
        raise HTTPException(
            status_code=404,
            detail=f"Platform '{platform}' not supported. Available: linkedin, indeed, greenhouse, glassdoor, monster, lever",
        )
