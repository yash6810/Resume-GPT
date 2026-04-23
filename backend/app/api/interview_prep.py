from fastapi import APIRouter, HTTPException
import os

from app.models.schemas import (
    InterviewPrepRequest,
    InterviewPrepResponse,
    InterviewQuestion,
)
from app.services.interview_prep import generate_interview_questions

router = APIRouter()


@router.post("/interview-prep", response_model=InterviewPrepResponse)
async def generate_interview_prep(data: InterviewPrepRequest):
    """Generate interview questions based on resume and job description."""
    try:
        # Check which LLM provider is available
        provider = "rule-based"
        if os.getenv("GROQ_API_KEY"):
            provider = "groq"
        elif os.getenv("GEMINI_API_KEY"):
            provider = "gemini"
        elif os.getenv("OPENAI_API_KEY"):
            provider = "openai"

        # Generate questions
        questions = generate_interview_questions(
            resume_text=data.resume_text,
            job_description=data.job_description,
            question_types=data.question_types,
        )

        # Convert to response format
        technical = [
            InterviewQuestion(question=q["question"], tips=q["tips"])
            for q in questions.get("technical", [])
        ]
        behavioral = [
            InterviewQuestion(question=q["question"], tips=q["tips"])
            for q in questions.get("behavioral", [])
        ]
        situational = [
            InterviewQuestion(question=q["question"], tips=q["tips"])
            for q in questions.get("situational", [])
        ]
        company = [
            InterviewQuestion(question=q["question"], tips=q["tips"])
            for q in questions.get("company", [])
        ]

        return InterviewPrepResponse(
            technical=technical,
            behavioral=behavioral,
            situational=situational,
            company=company,
            provider=provider,
        )

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error generating interview questions: {str(e)}"
        )
