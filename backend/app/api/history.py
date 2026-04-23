from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db, ResumeHistory, User
from app.models.schemas import ResumeHistoryCreate, ResumeHistoryResponse
from app.api.auth import get_current_user

router = APIRouter()


@router.post("/history/save", response_model=ResumeHistoryResponse)
def save_resume_history(
    history: ResumeHistoryCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Save resume analysis to history"""
    db_history = ResumeHistory(
        user_id=current_user.id,
        resume_name=history.resume_name,
        job_description=history.job_description,
        ats_score=history.ats_score,
        matched_skills=history.matched_skills,
        missing_skills=history.missing_skills,
        recommendations=history.recommendations,
        resume_text=history.resume_text,
        analysis_data=history.analysis_data,
    )
    db.add(db_history)
    db.commit()
    db.refresh(db_history)

    return db_history


@router.get("/history/list", response_model=List[ResumeHistoryResponse])
def list_resume_history(
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    """List all resume history for current user"""
    history = (
        db.query(ResumeHistory)
        .filter(ResumeHistory.user_id == current_user.id)
        .order_by(ResumeHistory.created_at.desc())
        .all()
    )

    return history


@router.get("/history/{history_id}", response_model=ResumeHistoryResponse)
def get_resume_history(
    history_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get a specific resume history entry"""
    history = (
        db.query(ResumeHistory)
        .filter(
            ResumeHistory.id == history_id, ResumeHistory.user_id == current_user.id
        )
        .first()
    )

    if not history:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Resume history not found"
        )

    return history


@router.delete("/history/{history_id}")
def delete_resume_history(
    history_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Delete a specific resume history entry"""
    history = (
        db.query(ResumeHistory)
        .filter(
            ResumeHistory.id == history_id, ResumeHistory.user_id == current_user.id
        )
        .first()
    )

    if not history:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Resume history not found"
        )

    db.delete(history)
    db.commit()

    return {"message": "Resume history deleted successfully"}


@router.get("/history/stats/summary")
def get_history_stats(
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    """Get summary statistics for resume history"""
    history = (
        db.query(ResumeHistory).filter(ResumeHistory.user_id == current_user.id).all()
    )

    if not history:
        return {
            "total_analyses": 0,
            "average_score": 0,
            "highest_score": 0,
            "lowest_score": 0,
        }

    scores = [h.ats_score for h in history if h.ats_score is not None]

    return {
        "total_analyses": len(history),
        "average_score": sum(scores) / len(scores) if scores else 0,
        "highest_score": max(scores) if scores else 0,
        "lowest_score": min(scores) if scores else 0,
    }
