"""
A/B Testing API Endpoints - Track resume performance with callback/outcome tracking.

Provides endpoints to create A/B tests, track outcomes (callback/no callback),
and analyze which resume versions perform better.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from app.core.database import get_db, ABTest, User
from app.models.schemas import (
    ABTestCreate,
    ABTestResponse,
    ABTestUpdateOutcome,
    ABTestStats,
)
from app.api.auth import get_current_user

router = APIRouter()


def determine_winner(score_a: float, score_b: float) -> str:
    """Determine which resume won based on scores."""
    if score_a > score_b:
        return "a"
    elif score_b > score_a:
        return "b"
    return "none"


@router.post("/create", response_model=ABTestResponse)
async def create_ab_test(
    test: ABTestCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Create a new A/B test comparing two resume versions.
    """
    if not test.resume_a or not test.resume_a.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Resume A text is required",
        )

    if not test.resume_b or not test.resume_b.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Resume B text is required",
        )

    winner = determine_winner(test.score_a, test.score_b)

    db_test = ABTest(
        user_id=current_user.id,
        job_description=test.job_description,
        resume_a=test.resume_a,
        resume_b=test.resume_b,
        score_a=test.score_a,
        score_b=test.score_b,
        winner=winner,
        platform=test.platform,
        notes=test.notes,
    )

    db.add(db_test)
    db.commit()
    db.refresh(db_test)

    return ABTestResponse(
        id=db_test.id,
        user_id=db_test.user_id,
        job_description=db_test.job_description,
        resume_a=db_test.resume_a,
        resume_b=db_test.resume_b,
        score_a=db_test.score_a,
        score_b=db_test.score_b,
        winner=db_test.winner,
        platform=db_test.platform,
        outcome=db_test.outcome,
        outcome_notes=db_test.outcome_notes,
        created_at=db_test.created_at.isoformat() if db_test.created_at else "",
        outcome_recorded_at=db_test.outcome_recorded_at.isoformat()
        if db_test.outcome_recorded_at
        else None,
    )


@router.get("/list", response_model=List[ABTestResponse])
async def list_ab_tests(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    List all A/B tests for the current user.
    """
    tests = (
        db.query(ABTest)
        .filter(ABTest.user_id == current_user.id)
        .order_by(ABTest.created_at.desc())
        .all()
    )

    return [
        ABTestResponse(
            id=test.id,
            user_id=test.user_id,
            job_description=test.job_description,
            resume_a=test.resume_a,
            resume_b=test.resume_b,
            score_a=test.score_a,
            score_b=test.score_b,
            winner=test.winner,
            platform=test.platform,
            outcome=test.outcome,
            outcome_notes=test.outcome_notes,
            created_at=test.created_at.isoformat() if test.created_at else "",
            outcome_recorded_at=test.outcome_recorded_at.isoformat()
            if test.outcome_recorded_at
            else None,
        )
        for test in tests
    ]


@router.get("/{test_id}", response_model=ABTestResponse)
async def get_ab_test(
    test_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Get a specific A/B test by ID.
    """
    test = (
        db.query(ABTest)
        .filter(ABTest.id == test_id, ABTest.user_id == current_user.id)
        .first()
    )

    if not test:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="A/B test not found",
        )

    return ABTestResponse(
        id=test.id,
        user_id=test.user_id,
        job_description=test.job_description,
        resume_a=test.resume_a,
        resume_b=test.resume_b,
        score_a=test.score_a,
        score_b=test.score_b,
        winner=test.winner,
        platform=test.platform,
        outcome=test.outcome,
        outcome_notes=test.outcome_notes,
        created_at=test.created_at.isoformat() if test.created_at else "",
        outcome_recorded_at=test.outcome_recorded_at.isoformat()
        if test.outcome_recorded_at
        else None,
    )


@router.put("/{test_id}/outcome")
async def update_outcome(
    test_id: int,
    outcome_update: ABTestUpdateOutcome,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Update the outcome of an A/B test (callback/no callback).
    """
    test = (
        db.query(ABTest)
        .filter(ABTest.id == test_id, ABTest.user_id == current_user.id)
        .first()
    )

    if not test:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="A/B test not found",
        )

    if outcome_update.outcome not in ["callback", "no_callback", "pending"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid outcome. Must be: callback, no_callback, or pending",
        )

    test.outcome = outcome_update.outcome
    test.outcome_notes = outcome_update.notes or ""

    if outcome_update.outcome in ["callback", "no_callback"]:
        test.outcome_recorded_at = datetime.utcnow()

    db.commit()
    db.refresh(test)

    return {
        "message": "Outcome updated successfully",
        "test_id": test.id,
        "outcome": test.outcome,
        "outcome_recorded_at": test.outcome_recorded_at.isoformat()
        if test.outcome_recorded_at
        else None,
    }


@router.delete("/{test_id}")
async def delete_ab_test(
    test_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Delete an A/B test.
    """
    test = (
        db.query(ABTest)
        .filter(ABTest.id == test_id, ABTest.user_id == current_user.id)
        .first()
    )

    if not test:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="A/B test not found",
        )

    db.delete(test)
    db.commit()

    return {"message": "A/B test deleted successfully"}


@router.get("/{test_id}/stats")
async def get_test_stats(
    test_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Get statistics for a specific A/B test.
    """
    test = (
        db.query(ABTest)
        .filter(ABTest.id == test_id, ABTest.user_id == current_user.id)
        .first()
    )

    if not test:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="A/B test not found",
        )

    return {
        "test_id": test.id,
        "score_a": test.score_a,
        "score_b": test.score_b,
        "winner": test.winner,
        "outcome": test.outcome,
        "platform": test.platform,
        "score_diff": abs(test.score_a - test.score_b),
        "was_winner_callback": (test.winner == "a" and test.outcome == "callback")
        or (test.winner == "b" and test.outcome == "callback"),
    }


@router.get("/stats/overview", response_model=ABTestStats)
async def get_stats_overview(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Get aggregate statistics across all A/B tests for the user.
    """
    tests = db.query(ABTest).filter(ABTest.user_id == current_user.id).all()

    if not tests:
        return ABTestStats(
            total_tests=0,
            callback_rate=0.0,
            win_rate_a=0.0,
            win_rate_b=0.0,
            avg_score_a=0.0,
            avg_score_b=0.0,
            platform_stats={},
        )

    total = len(tests)
    callbacks = sum(1 for t in tests if t.outcome == "callback")
    no_callbacks = sum(1 for t in tests if t.outcome == "no_callback")

    wins_a = sum(1 for t in tests if t.winner == "a")
    wins_b = sum(1 for t in tests if t.winner == "b")

    callback_rate = (callbacks / total * 100) if total > 0 else 0.0

    win_rate_a = (wins_a / total * 100) if total > 0 else 0.0
    win_rate_b = (wins_b / total * 100) if total > 0 else 0.0

    avg_score_a = sum(t.score_a for t in tests) / total
    avg_score_b = sum(t.score_b for t in tests) / total

    platform_stats = {}
    for test in tests:
        platform = test.platform or "generic"
        if platform not in platform_stats:
            platform_stats[platform] = {"total": 0, "callbacks": 0}
        platform_stats[platform]["total"] += 1
        if test.outcome == "callback":
            platform_stats[platform]["callbacks"] += 1

    for platform in platform_stats:
        total_platform = platform_stats[platform]["total"]
        callbacks_platform = platform_stats[platform]["callbacks"]
        platform_stats[platform]["callback_rate"] = (
            callbacks_platform / total_platform * 100 if total_platform > 0 else 0
        )

    return ABTestStats(
        total_tests=total,
        callback_rate=round(callback_rate, 2),
        win_rate_a=round(win_rate_a, 2),
        win_rate_b=round(win_rate_b, 2),
        avg_score_a=round(avg_score_a, 2),
        avg_score_b=round(avg_score_b, 2),
        platform_stats=platform_stats,
    )
