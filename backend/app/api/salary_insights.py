from fastapi import APIRouter, HTTPException

from app.models.schemas import (
    SalaryInsightsRequest,
    SalaryInsightsResponse,
)
from app.services.salary_insights import estimate_salary

router = APIRouter()


@router.post("/salary-insights", response_model=SalaryInsightsResponse)
async def get_salary_insights(data: SalaryInsightsRequest):
    """Estimate salary range based on job title, skills, location, and experience."""
    try:
        result = estimate_salary(
            skills=data.skills,
            job_title=data.job_title,
            location=data.location,
            years_experience=data.years_experience,
        )

        return SalaryInsightsResponse(
            min_salary=result.get("min_salary", 0),
            max_salary=result.get("max_salary", 0),
            median_salary=result.get("median_salary", 0),
            currency=result.get("currency", "USD"),
            factors=result.get("factors", []),
            tips=result.get("tips", []),
            market_trend=result.get("market_trend", "stable"),
            provider=result.get("provider", "rule-based"),
        )

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error estimating salary: {str(e)}"
        )
