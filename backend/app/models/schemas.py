from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from datetime import datetime


class ParseRequest(BaseModel):
    pass  # File upload handled by FastAPI


class ParseResponse(BaseModel):
    text: str
    sections: Dict[str, str]


class AnalyzeRequest(BaseModel):
    resume_text: str
    job_description: str


class SubScores(BaseModel):
    keywords: float = Field(..., ge=0, le=40)
    role_match: float = Field(..., ge=0, le=30)
    experience_relevance: float = Field(..., ge=0, le=20)
    quality: float = Field(..., ge=0, le=10)


class SkillMatch(BaseModel):
    skill: str
    type: str  # "exact" or "semantic"
    score: Optional[float] = None


class AnalyzeResponse(BaseModel):
    ats_score: float = Field(..., ge=0, le=100)
    subscores: SubScores
    skill_matches: List[SkillMatch]
    missing_skills: List[str]
    recommendations: List[str]


class RewriteRequest(BaseModel):
    bullet: str
    target_keywords: List[str]


class RewriteResponse(BaseModel):
    variants: List[str]  # ["ATS-optimized version", "Human-friendly version"]


# Cover Letter Models
class CoverLetterRequest(BaseModel):
    resume_text: str
    job_description: str
    company_name: str
    position: str


class CoverLetterResponse(BaseModel):
    cover_letter: str
    message: str


class ExportRequest(BaseModel):
    resume_text: str
    applied_changes: List[Dict[str, str]]  # [{"original": "...", "replacement": "..."}]


class ExportResponse(BaseModel):
    success: bool
    message: str


# User Authentication Models
class UserCreate(BaseModel):
    email: str
    username: str
    password: str
    full_name: Optional[str] = None


class UserLogin(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    full_name: Optional[str] = None
    created_at: datetime


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


# Industry Template schemas
class IndustryTemplate(BaseModel):
    id: str
    name: str
    description: str
    icon: str
    suggested_sections: List[str]
    keywords: List[str]
    summary_template: str
    bullet_templates: List[str]
    skills_categories: Dict[str, List[str]]
    recommended_certs: List[str]
    color_primary: str
    color_secondary: str


class IndustryTemplatesResponse(BaseModel):
    templates: Dict[str, IndustryTemplate]


class IndustrySuggestionRequest(BaseModel):
    industry_id: str
    role: str = ""
    years_experience: int = 0


# Resume History Models
class ResumeHistoryCreate(BaseModel):
    resume_name: str
    job_description: Optional[str] = None
    ats_score: Optional[float] = None
    matched_skills: List[str] = []
    missing_skills: List[str] = []
    recommendations: List[str] = []
    resume_text: Optional[str] = None
    analysis_data: Optional[Dict] = None


class ResumeHistoryResponse(BaseModel):
    id: int
    user_id: int
    resume_name: str
    job_description: Optional[str] = None
    ats_score: Optional[float] = None
    matched_skills: List[str] = []
    missing_skills: List[str] = []
    recommendations: List[str] = []
    resume_text: Optional[str] = None
    analysis_data: Optional[Dict] = None
    created_at: datetime
    updated_at: datetime


# Job Tracker Models
class JobApplicationCreate(BaseModel):
    company_name: str
    position_title: str
    job_description: Optional[str] = None
    job_url: Optional[str] = None
    location: Optional[str] = None
    salary_range: Optional[str] = None
    status: str = "applied"  # applied, screening, interview, offer, rejected, accepted
    ats_score: Optional[float] = None
    resume_used: Optional[str] = None
    notes: Optional[str] = None
    applied_date: Optional[datetime] = None
    follow_up_date: Optional[datetime] = None
    interview_date: Optional[datetime] = None


class JobApplicationUpdate(BaseModel):
    company_name: Optional[str] = None
    position_title: Optional[str] = None
    job_description: Optional[str] = None
    job_url: Optional[str] = None
    location: Optional[str] = None
    salary_range: Optional[str] = None
    status: Optional[str] = None
    ats_score: Optional[float] = None
    resume_used: Optional[str] = None
    notes: Optional[str] = None
    applied_date: Optional[datetime] = None
    follow_up_date: Optional[datetime] = None
    interview_date: Optional[datetime] = None


class JobApplicationResponse(BaseModel):
    id: int
    user_id: int
    company_name: str
    position_title: str
    job_description: Optional[str] = None
    job_url: Optional[str] = None
    location: Optional[str] = None
    salary_range: Optional[str] = None
    status: str
    ats_score: Optional[float] = None
    resume_used: Optional[str] = None
    notes: Optional[str] = None
    applied_date: datetime
    follow_up_date: Optional[datetime] = None
    interview_date: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class JobTrackerStats(BaseModel):
    total_applications: int
    by_status: Dict[str, int]
    avg_ats_score: Optional[float]
    upcoming_interviews: int
    upcoming_followups: int


# Interview Prep Models
class InterviewQuestion(BaseModel):
    question: str
    tips: str


class InterviewPrepRequest(BaseModel):
    resume_text: str
    job_description: str
    question_types: List[str] = ["technical", "behavioral", "situational", "company"]


class InterviewPrepResponse(BaseModel):
    technical: List[InterviewQuestion] = []
    behavioral: List[InterviewQuestion] = []
    situational: List[InterviewQuestion] = []
    company: List[InterviewQuestion] = []
    provider: str = "rule-based"


# Salary Insights Models
class SalaryInsightsRequest(BaseModel):
    job_title: str
    skills: List[str] = []
    location: str = "United States"
    years_experience: int = 0


class SalaryInsightsResponse(BaseModel):
    min_salary: int
    max_salary: int
    median_salary: int
    currency: str = "USD"
    factors: List[str] = []
    tips: List[str] = []
    market_trend: str = "stable"
    provider: str = "rule-based"


# LinkedIn Import Models
class LinkedInImportRequest(BaseModel):
    profile_text: str


class LinkedInContact(BaseModel):
    name: str = ""
    email: str = ""
    phone: str = ""
    location: str = ""
    linkedin: str = ""
    website: str = ""


class LinkedInExperience(BaseModel):
    title: str = ""
    company: str = ""
    location: str = ""
    start_date: str = ""
    end_date: str = ""
    bullets: List[str] = []


class LinkedInEducation(BaseModel):
    degree: str = ""
    school: str = ""
    location: str = ""
    graduation_date: str = ""
    gpa: Optional[str] = None


class LinkedInImportResponse(BaseModel):
    contact: LinkedInContact
    summary: str = ""
    skills: List[str] = []
    experience: List[LinkedInExperience] = []
    education: List[LinkedInEducation] = []
    certifications: List[str] = []
    formatted_text: str = ""


# ATS Simulator Models
class ATSPlatformRequest(BaseModel):
    resume_text: str
    job_description: str
    file_size_bytes: int = 0
    file_extension: str = "pdf"


class ATSPlatformResponse(BaseModel):
    platform: str
    platform_key: str
    total_score: float
    subscores: dict
    matched_skills: List[str]
    missing_skills: List[str]
    focus_areas: List[str]
    recommendations: List[str]
    parsing_simulation: dict = {}


class ATSPlatformInfo(BaseModel):
    key: str
    name: str
    keyword_weight: float
    role_match_weight: float
    formatting_weight: float
    max_file_size_mb: int
    accepted_formats: List[str]
    focus_areas: List[str]


class ATSMultiPlatformRequest(BaseModel):
    resume_text: str
    job_description: str


class ATSMultiPlatformResponse(BaseModel):
    platforms: dict
    best_platform: str
    best_score: float
    worst_platform: str
    worst_score: float
    recommendation: str


# A/B Testing Models
class ABTestCreate(BaseModel):
    job_description: str
    resume_a: str
    resume_b: str
    score_a: float
    score_b: float
    platform: str = "generic"
    notes: str = ""


class ABTestUpdateOutcome(BaseModel):
    outcome: str
    notes: str = ""
    outcome_callback_date: Optional[str] = None


class ABTestResponse(BaseModel):
    id: int
    user_id: int
    job_description: str
    resume_a: str
    resume_b: str
    score_a: float
    score_b: float
    winner: str
    platform: str
    outcome: str
    outcome_notes: str = ""
    created_at: str
    outcome_recorded_at: Optional[str] = None


class ABTestStats(BaseModel):
    total_tests: int
    callback_rate: float
    win_rate_a: float
    win_rate_b: float
    avg_score_a: float
    avg_score_b: float
    platform_stats: dict = {}
