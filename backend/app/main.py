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


from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# Mount static frontend directory
frontend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "frontend"))
if os.path.exists(frontend_dir):
    app.mount("/static", StaticFiles(directory=frontend_dir), name="static")

@app.get("/app", response_class=FileResponse)
@app.get("/index.html", response_class=FileResponse)
async def serve_frontend():
    index_path = os.path.join(frontend_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return JSONResponse(status_code=404, content={"detail": "Frontend index.html not found"})

@app.get("/")
async def root():
    index_path = os.path.join(frontend_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {
        "message": "Welcome to ResumeGPT API",
        "version": "2.0.0",
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "ResumeGPT"}
