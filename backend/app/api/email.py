"""
Email API - Send emails with templates.

Provides endpoints to send welcome emails, cover letters, alerts.
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
from app.services.email_service import (
    send_welcome_email,
    send_cover_letter_email,
    send_callback_alert,
    send_job_alert,
    is_email_configured,
    get_smtp_config,
)
from app.api.auth import get_current_user
from app.core.database import User

router = APIRouter()


class WelcomeEmailRequest(BaseModel):
    email: str
    name: str


class CoverLetterEmailRequest(BaseModel):
    email: str
    name: str
    company: str
    cover_letter: str


class CallbackAlertRequest(BaseModel):
    email: str
    name: str
    total_tests: int
    callback_rate: float
    winner: str
    platform: str
    best_score: float


class JobAlertRequest(BaseModel):
    email: str
    name: str
    company: str
    position: str
    location: str
    salary: str
    status: str
    applied_date: str
    job_url: str


@router.get("/status")
async def get_email_status():
    """
    Check email configuration status.
    """
    configured = is_email_configured()
    config = get_smtp_config()

    return {
        "configured": configured,
        "host": config.get("host", "") if configured else "Not configured",
        "username": config.get("username", "")[:4] + "****"
        if configured and config.get("username")
        else "",
    }


@router.post("/welcome")
async def send_welcome(request: WelcomeEmailRequest):
    """
    Send welcome email to a user.
    """
    if not is_email_configured():
        raise HTTPException(
            status_code=503,
            detail="Email service not configured",
        )

    success = send_welcome_email(request.email, request.name)

    if not success:
        raise HTTPException(
            status_code=500,
            detail="Failed to send email",
        )

    return {"message": "Welcome email sent successfully"}


@router.post("/cover-letter")
async def send_cover_letter(request: CoverLetterEmailRequest):
    """
    Send generated cover letter via email.
    """
    if not is_email_configured():
        raise HTTPException(
            status_code=503,
            detail="Email service not configured",
        )

    success = send_cover_letter_email(
        request.email,
        request.name,
        request.company,
        request.cover_letter,
    )

    if not success:
        raise HTTPException(
            status_code=500,
            detail="Failed to send email",
        )

    return {"message": "Cover letter email sent successfully"}


@router.post("/callback-alert")
async def send_callback(request: CallbackAlertRequest):
    """
    Send callback alert email.
    """
    if not is_email_configured():
        raise HTTPException(
            status_code=503,
            detail="Email service not configured",
        )

    success = send_callback_alert(
        request.email,
        request.name,
        request.total_tests,
        request.callback_rate,
        request.winner,
        request.platform,
        request.best_score,
    )

    if not success:
        raise HTTPException(
            status_code=500,
            detail="Failed to send email",
        )

    return {"message": "Callback alert sent successfully"}


@router.post("/job-alert")
async def send_job_update(request: JobAlertRequest):
    """
    Send job application status update.
    """
    if not is_email_configured():
        raise HTTPException(
            status_code=503,
            detail="Email service not configured",
        )

    success = send_job_alert(
        request.email,
        request.name,
        request.company,
        request.position,
        request.location,
        request.salary,
        request.status,
        request.applied_date,
        request.job_url,
    )

    if not success:
        raise HTTPException(
            status_code=500,
            detail="Failed to send email",
        )

    return {"message": "Job alert sent successfully"}
