from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, HttpUrl


class CandidateProfile(BaseModel):
    name: str
    location: str = ""
    graduation_year: Optional[int] = None
    degree: str = ""
    target_roles: List[str] = []
    target_domains: List[str] = []
    skills: List[str] = []
    resume_text: str = ""


class JobCandidate(BaseModel):
    company: str
    title: str
    description: str
    url: Optional[str] = None
    location: str = ""
    source: str = "manual"
    deadline: Optional[str] = None


class JobMatchRequest(BaseModel):
    candidate: CandidateProfile
    job: JobCandidate


class JobMatchResponse(BaseModel):
    score: float = Field(..., ge=0, le=100)
    eligible: bool
    role_type: str
    matched_skills: List[str] = []
    missing_skills: List[str] = []
    relevant_projects: List[str] = []
    recommended_resume: str = "finance_ds"
    reasons: List[str] = []


class ApplicationDraftRequest(BaseModel):
    candidate: CandidateProfile
    job: JobCandidate
    match: JobMatchResponse


class ApplicationDraftResponse(BaseModel):
    resume_variant: str
    cover_letter: str
    answers: dict = {}
    warnings: List[str] = []
    requires_review: bool = True
