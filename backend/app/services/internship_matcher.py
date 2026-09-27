from typing import List
from app.models.internship_schemas import CandidateProfile, JobCandidate, JobMatchResponse

ROLE_KEYWORDS = {
    "quant": ["quant", "algorithmic trading", "quantitative", "trading", "backtesting", "market risk"],
    "financial_ds": ["financial data", "finance", "risk analytics", "data science", "machine learning", "analytics"],
    "ai_ml": ["machine learning", "ai", "artificial intelligence", "llm", "genai", "nlp", "mlops"],
    "swe": ["software engineer", "backend", "api", "python", "software development", "full stack"],
}


def _norm(items: List[str]) -> set[str]:
    return {x.strip().lower() for x in items if x and x.strip()}


def infer_role_type(job: JobCandidate) -> str:
    text = f"{job.title} {job.description}".lower()
    scores = {role: sum(1 for k in keys if k in text) for role, keys in ROLE_KEYWORDS.items()}
    return max(scores, key=scores.get) if max(scores.values()) else "other"


def match_job(candidate: CandidateProfile, job: JobCandidate) -> JobMatchResponse:
    job_text = f"{job.title} {job.description}".lower()
    skills = _norm(candidate.skills)
    matched = sorted([s for s in skills if s in job_text])

    missing_common = [
        k for k in ["python", "sql", "statistics", "machine learning", "xgboost", "pytorch", "docker", "fastapi"]
        if k in job_text and k not in skills
    ]

    role = infer_role_type(job)
    role_bonus = 25 if ((role == "quant" and any("quant" in r.lower() for r in candidate.target_roles)) or
                        (role == "financial_ds" and any(x in r.lower() for r in candidate.target_roles for x in ["data", "risk", "finance", "analytics"])) or
                        (role == "ai_ml" and any(x in r.lower() for r in candidate.target_roles for x in ["ai", "ml", "machine learning"])) or
                        (role == "swe" and any("software" in r.lower() for r in candidate.target_roles))) else 10

    skill_score = min(45, len(matched) * 6)
    domain_score = 15 if any(d.lower() in job_text for d in candidate.target_domains) else 5
    # Conservative eligibility: surface possible disqualifiers instead of silently assuming eligibility.
    eligibility = True
    graduation = str(candidate.graduation_year or "")
    if "graduating in 2026" in job_text and graduation != "2026": eligibility = False
    if "graduating in 2025" in job_text and graduation != "2025": eligibility = False
    if "2027 batch" in job_text and graduation != "2027": eligibility = False
    location_score = 10 if not candidate.location or not job.location or candidate.location.lower() in job.location.lower() else 5
    score = min(100, skill_score + role_bonus + domain_score + location_score + 5)

    projects = []
    if role in {"quant", "financial_ds"}:
        projects.append("Sentilyze")
        projects.append("The Accuracy Paradox in AI Equity Markets")
    if role in {"ai_ml", "swe"}:
        projects.append("Vyapar")

    return JobMatchResponse(
        score=round(score if eligibility else min(score, 49), 1), eligible=eligibility, role_type=role,
        matched_skills=matched, missing_skills=missing_common,
        relevant_projects=projects, recommended_resume={"quant":"quant", "financial_ds":"finance_ds", "ai_ml":"ai_ml", "swe":"swe"}.get(role, "finance_ds"),
        reasons=[f"Role classified as {role}", f"Matched {len(matched)} profile skills", "Human review required before submission"] + ([] if eligibility else ["Eligibility check found a potential graduation-year mismatch"]),
    )
