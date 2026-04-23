import os
import logging
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from app.api import (
    parse,
    analyze,
    rewrite,
    export,
    builder,
    auth,
    history,
    cover_letter,
    ner,
    job_tracker,
    interview_prep,
    salary_insights,
    linkedin_import,
    ats_simulator,
    ab_test,
    email,
)
from app.core.skills_loader import load_skills
from app.core.database import init_db

# Load skills on startup
load_skills()

# Initialize database
init_db()

app = FastAPI(
    title="ResumeGPT - AI Resume Analyzer & ATS Booster",
    description="Upload a resume + job description → get an ATS match score, missing-skill list, actionable rewrite suggestions, and an exportable ATS-optimized resume.",
    version="2.0.0",
)


# ============================================================
# GLOBAL ERROR HANDLERS
# ============================================================


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle validation errors (invalid request body)."""
    errors = [
        {"field": ".".join(err["loc"]), "message": err["msg"]} for err in exc.errors()
    ]
    logger.warning(f"Validation error: {errors}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": "Validation Error",
            "message": "Invalid request data",
            "details": errors,
        },
    )


@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    """Handle value errors."""
    logger.warning(f"Value error: {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "error": "Value Error",
            "message": str(exc),
        },
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Handle all unhandled exceptions."""
    logger.error(f"Unhandled exception: {type(exc).__name__}: {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal Server Error",
            "message": "Something went wrong. Please try again later.",
            "details": str(exc) if os.getenv("DEBUG") == "True" else None,
        },
    )


# Add CORS middleware
cors_origins = (
    os.getenv("CORS_ORIGINS", "").split(",") if os.getenv("CORS_ORIGINS") else ["*"]
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(parse.router, tags=["Parse"])
app.include_router(analyze.router, tags=["Analyze"])
app.include_router(rewrite.router, tags=["Rewrite"])
app.include_router(export.router, tags=["Export"])
app.include_router(builder.router, tags=["Builder"])
app.include_router(auth.router, tags=["Authentication"])
app.include_router(history.router, tags=["Resume History"])
app.include_router(cover_letter.router, tags=["Cover Letter"])
app.include_router(ner.router, tags=["NER"])
app.include_router(job_tracker.router, tags=["Job Tracker"])
app.include_router(interview_prep.router, tags=["Interview Prep"])
app.include_router(salary_insights.router, tags=["Salary Insights"])
app.include_router(linkedin_import.router, tags=["LinkedIn Import"])
app.include_router(
    ats_simulator.router, prefix="/ats-simulator", tags=["ATS Simulator"]
)
app.include_router(ab_test.router, prefix="/ab-test", tags=["A/B Testing"])
app.include_router(email.router, prefix="/email", tags=["Email"])


@app.get("/")
async def root():
    return {
        "message": "Welcome to ResumeGPT API",
        "version": "2.0.0",
        "endpoints": {
            "parse": "/parse - Upload and parse resume (PDF/DOCX)",
            "analyze": "/analyze - Analyze resume against job description",
            "rewrite": "/rewrite - Rewrite bullet points with target keywords",
            "export": "/export - Export optimized resume as DOCX",
            "builder_templates": "/builder/templates - List available resume templates",
            "builder_industry_templates": "/builder/industry-templates - List industry-specific templates",
            "builder_export": "/builder/export - Build and export resume as DOCX",
            "builder_text": "/builder/text - Build resume and return as text",
            "cover_letter_generate": "/cover-letter/generate - Generate cover letter",
            "cover_letter_export": "/cover-letter/export - Export cover letter as DOCX",
            "auth_register": "/auth/register - Register new user",
            "auth_login": "/auth/login - Login user",
            "auth_me": "/auth/me - Get current user profile",
            "history_save": "/history/save - Save resume analysis to history",
            "history_list": "/history/list - List resume history",
            "history_stats": "/history/stats/summary - Get history statistics",
            "job_tracker_list": "/job-tracker - List job applications",
            "job_tracker_create": "/job-tracker - Create job application",
            "job_tracker_stats": "/job-tracker/stats/summary - Get job tracker statistics",
            "interview_prep": "/interview-prep - Generate interview questions",
            "salary_insights": "/salary-insights - Estimate salary range",
            "linkedin_import": "/linkedin-import - Parse LinkedIn profile",
            "ats_simulator_platforms": "/ats-simulator/platforms - List supported ATS platforms",
            "ats_simulator_analyze": "/ats-simulator/analyze - Multi-platform analysis",
            "ats_simulator_linkedin": "/ats-simulator/linkedin - LinkedIn ATS simulation",
            "ats_simulator_indeed": "/ats-simulator/indeed - Indeed ATS simulation",
            "ats_simulator_greenhouse": "/ats-simulator/greenhouse - Greenhouse ATS simulation",
            "ab_test_create": "/ab-test/create - Create A/B test",
            "ab_test_list": "/ab-test/list - List A/B tests",
            "ab_test_outcome": "/ab-test/{id}/outcome - Record outcome",
            "ab_test_stats": "/ab-test/stats/overview - Get A/B test statistics",
        },
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "ResumeGPT"}
