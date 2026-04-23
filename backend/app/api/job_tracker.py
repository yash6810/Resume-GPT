from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta

from app.core.database import get_db, JobApplication, User
from app.api.auth import get_current_user
from app.models.schemas import (
    JobApplicationCreate,
    JobApplicationUpdate,
    JobApplicationResponse,
    JobTrackerStats,
)

router = APIRouter()


@router.post("/job-tracker", response_model=JobApplicationResponse)
async def create_job_application(
    job: JobApplicationCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Create a new job application entry."""
    db_job = JobApplication(
        user_id=current_user.id,
        company_name=job.company_name,
        position_title=job.position_title,
        job_description=job.job_description,
        job_url=job.job_url,
        location=job.location,
        salary_range=job.salary_range,
        status=job.status,
        ats_score=job.ats_score,
        resume_used=job.resume_used,
        notes=job.notes,
        applied_date=job.applied_date or datetime.utcnow(),
        follow_up_date=job.follow_up_date,
        interview_date=job.interview_date,
    )
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job


@router.get("/job-tracker", response_model=List[JobApplicationResponse])
async def list_job_applications(
    status: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """List all job applications for the current user."""
    query = db.query(JobApplication).filter(JobApplication.user_id == current_user.id)

    if status:
        query = query.filter(JobApplication.status == status)

    jobs = query.order_by(JobApplication.applied_date.desc()).all()
    return jobs


@router.get("/job-tracker/{job_id}", response_model=JobApplicationResponse)
async def get_job_application(
    job_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get a specific job application."""
    job = (
        db.query(JobApplication)
        .filter(JobApplication.id == job_id, JobApplication.user_id == current_user.id)
        .first()
    )

    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job application not found",
        )

    return job


@router.put("/job-tracker/{job_id}", response_model=JobApplicationResponse)
async def update_job_application(
    job_id: int,
    job_update: JobApplicationUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update a job application."""
    job = (
        db.query(JobApplication)
        .filter(JobApplication.id == job_id, JobApplication.user_id == current_user.id)
        .first()
    )

    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job application not found",
        )

    update_data = job_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(job, field, value)

    job.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(job)

    return job


@router.delete("/job-tracker/{job_id}")
async def delete_job_application(
    job_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Delete a job application."""
    job = (
        db.query(JobApplication)
        .filter(JobApplication.id == job_id, JobApplication.user_id == current_user.id)
        .first()
    )

    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job application not found",
        )

    db.delete(job)
    db.commit()

    return {"message": "Job application deleted successfully"}


@router.get("/job-tracker/stats/summary", response_model=JobTrackerStats)
async def get_job_tracker_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get job tracker statistics."""
    jobs = (
        db.query(JobApplication).filter(JobApplication.user_id == current_user.id).all()
    )

    total = len(jobs)

    # Count by status
    by_status = {}
    for job in jobs:
        by_status[job.status] = by_status.get(job.status, 0) + 1

    # Average ATS score
    scores = [j.ats_score for j in jobs if j.ats_score is not None]
    avg_score = sum(scores) / len(scores) if scores else None

    # Upcoming interviews (next 7 days)
    now = datetime.utcnow()
    week_later = now + timedelta(days=7)
    upcoming_interviews = sum(
        1 for j in jobs if j.interview_date and now <= j.interview_date <= week_later
    )

    # Upcoming follow-ups (next 7 days)
    upcoming_followups = sum(
        1 for j in jobs if j.follow_up_date and now <= j.follow_up_date <= week_later
    )

    return JobTrackerStats(
        total_applications=total,
        by_status=by_status,
        avg_ats_score=avg_score,
        upcoming_interviews=upcoming_interviews,
        upcoming_followups=upcoming_followups,
    )
