"""
ATS Simulator Service - Platform-specific resume parsing and scoring simulation.

Simulates how different ATS systems (LinkedIn, Indeed, Greenhouse) parse and score resumes.
Each platform has different keyword weighting, formatting requirements, and parsing rules.

Supported platforms:
- LinkedIn: Skills-first, profile completeness focus
- Indeed: Simple text parsing, limited formatting
- Greenhouse: DEI keywords, culture fit focus
"""

import re
from typing import Dict, List, Optional, Set, Tuple
from dataclasses import dataclass
from app.core.skills_loader import get_all_skills, load_skills
from app.core.embeddings import get_embedding_model


@dataclass
class PlatformConfig:
    """Configuration for each ATS platform."""

    name: str
    keyword_weight: float
    role_match_weight: float
    formatting_weight: float
    max_file_size_mb: int
    accepted_formats: List[str]
    strict_parsing: bool
    focus_areas: List[str]
    bonus_keywords: List[str]
    penalty_keywords: List[str]


ATS_PLATFORMS = {
    "linkedin": PlatformConfig(
        name="LinkedIn",
        keyword_weight=50,
        role_match_weight=30,
        formatting_weight=20,
        max_file_size_mb=2,
        accepted_formats=["pdf", "docx"],
        strict_parsing=False,
        focus_areas=["skills", "profile_completeness", "certifications"],
        bonus_keywords=[
            "leadership",
            "managed",
            "achieved",
            "innovated",
            "transformed",
        ],
        penalty_keywords=["responsible for", "duties include", "helped with"],
    ),
    "indeed": PlatformConfig(
        name="Indeed",
        keyword_weight=40,
        role_match_weight=30,
        formatting_weight=30,
        max_file_size_mb=1,
        accepted_formats=["pdf", "docx", "txt"],
        strict_parsing=True,
        focus_areas=["basic_info", "experience", "skills"],
        bonus_keywords=["managed", "developed", "implemented", "created"],
        penalty_keywords=["asd", "asdf", "xxx"],  # Common spam words
    ),
    "greenhouse": PlatformConfig(
        name="Greenhouse",
        keyword_weight=55,
        role_match_weight=25,
        formatting_weight=20,
        max_file_size_mb=2,
        accepted_formats=["pdf", "docx"],
        strict_parsing=False,
        focus_areas=["diversity", "culture_fit", "impact", "leadership"],
        bonus_keywords=[
            "collaborated",
            "mentored",
            "inclusive",
            "accessible",
            "diverse",
            "equity",
        ],
        penalty_keywords=["sole developer", "i did everything"],
    ),
    "glassdoor": PlatformConfig(
        name="Glassdoor",
        keyword_weight=45,
        role_match_weight=30,
        formatting_weight=25,
        max_file_size_mb=2,
        accepted_formats=["pdf", "docx"],
        strict_parsing=False,
        focus_areas=["company_research", "salary", "culture"],
        bonus_keywords=["salary", "compensation", "benefits", "team", "growth"],
        penalty_keywords=["confidential", "nda"],
    ),
    "monster": PlatformConfig(
        name="Monster",
        keyword_weight=40,
        role_match_weight=30,
        formatting_weight=30,
        max_file_size_mb=1,
        accepted_formats=["pdf", "docx", "txt"],
        strict_parsing=True,
        focus_areas=["standard_ats", "keywords", "experience"],
        bonus_keywords=["experienced", "managed", "developed", "led"],
        penalty_keywords=["asd", "asdf", "xxx"],
    ),
    "lever": PlatformConfig(
        name="Lever",
        keyword_weight=50,
        role_match_weight=25,
        formatting_weight=25,
        max_file_size_mb=2,
        accepted_formats=["pdf", "docx"],
        strict_parsing=False,
        focus_areas=["culture_fit", "values", "team_impact"],
        bonus_keywords=[
            "passionate",
            "motivated",
            "driven",
            "values",
            "purpose",
            "mission",
        ],
        penalty_keywords=["unmotivated", "lazy"],
    ),
}


def get_platform_config(platform: str) -> Optional[PlatformConfig]:
    """Get configuration for a specific platform."""
    return ATS_PLATFORMS.get(platform.lower())


def get_all_platforms() -> Dict[str, PlatformConfig]:
    """Get all supported platforms."""
    return ATS_PLATFORMS


def extract_keywords_from_jd(job_description: str) -> Set[str]:
    """Extract keywords from job description using existing skills loader."""
    all_skills = get_all_skills()
    if not all_skills:
        load_skills()
        all_skills = get_all_skills()

    text_lower = job_description.lower()
    found_skills = set()

    for skill in all_skills:
        pattern = r"\b" + re.escape(skill) + r"\b"
        if re.search(pattern, text_lower):
            found_skills.add(skill)

    return found_skills


def extract_resume_skills(resume_text: str) -> Set[str]:
    """Extract skills from resume text."""
    all_skills = get_all_skills()
    if not all_skills:
        load_skills()
        all_skills = get_all_skills()

    text_lower = resume_text.lower()
    found_skills = set()

    for skill in all_skills:
        pattern = r"\b" + re.escape(skill) + r"\b"
        if re.search(pattern, text_lower):
            found_skills.add(skill)

    return found_skills


def calculate_keyword_score(
    resume_skills: Set[str], jd_skills: Set[str], keyword_weight: float
) -> Tuple[float, List[str], List[str]]:
    """Calculate keyword match score."""
    if not jd_skills:
        return 0.0, [], []

    exact_matches = resume_skills.intersection(jd_skills)
    missing_skills = list(jd_skills - resume_skills)

    match_ratio = len(exact_matches) / len(jd_skills) if jd_skills else 0
    score = match_ratio * keyword_weight

    return score, list(exact_matches), missing_skills


def calculate_role_match_score(
    resume_text: str, job_description: str, role_match_weight: float
) -> float:
    """Calculate role match score using embeddings."""
    embedding_model = get_embedding_model()

    experience_section = extract_experience_section(resume_text)
    if not experience_section:
        experience_section = resume_text[:1000]

    similarity = embedding_model.cosine_similarity(experience_section, job_description)
    score = similarity * role_match_weight

    return max(0, min(score, role_match_weight))


def extract_experience_section(text: str) -> str:
    """Extract experience section from resume."""
    patterns = [
        r"(?i)experience.*?(?=education|skills|summary|projects|$)",
        r"(?i)work experience.*?(?=education|skills|summary|projects|$)",
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.DOTALL)
        if match:
            return match.group(0)[:2000]

    return text[:2000]


def calculate_formatting_score(resume_text: str, config: PlatformConfig) -> float:
    """Calculate formatting compliance score."""
    score = 0.0
    max_score = config.formatting_weight

    lines = resume_text.split("\n")
    bullets = [line for line in lines if line.strip().startswith(("•", "-", "*"))]

    if bullets:
        score += 5

    has_sections = any(
        keyword in resume_text.lower()
        for keyword in ["experience", "education", "skills", "summary"]
    )
    if has_sections:
        score += 5

    for bonus_word in config.bonus_keywords:
        if bonus_word in resume_text.lower():
            score += 2

    for penalty_word in config.penalty_keywords:
        if penalty_word in resume_text.lower():
            score -= 3

    return max(0, min(score, max_score))


def check_file_compliance(
    file_size_bytes: int, file_extension: str, config: PlatformConfig
) -> Tuple[bool, str]:
    """Check if file meets platform requirements."""
    max_bytes = config.max_file_size_mb * 1024 * 1024

    if file_size_bytes > max_bytes:
        return False, f"File too large. Max {config.max_file_size_mb}MB allowed."

    if file_extension.lower() not in config.accepted_formats:
        return (
            False,
            f"Format not supported. Accepts: {', '.join(config.accepted_formats)}",
        )

    return True, "OK"


def analyze_platform_ats(resume_text: str, job_description: str, platform: str) -> Dict:
    """
    Analyze resume against specific ATS platform.

    Returns detailed scoring breakdown with platform-specific insights.
    """
    config = get_platform_config(platform)
    if not config:
        return {"error": f"Platform '{platform}' not supported"}

    jd_skills = extract_keywords_from_jd(job_description)
    resume_skills = extract_resume_skills(resume_text)

    keyword_score, matched_keywords, missing_keywords = calculate_keyword_score(
        resume_skills, jd_skills, config.keyword_weight
    )

    role_match_score = calculate_role_match_score(
        resume_text, job_description, config.role_match_weight
    )

    formatting_score = calculate_formatting_score(resume_text, config)

    total_score = keyword_score + role_match_score + formatting_score

    recommendations = generate_recommendations(
        platform, missing_keywords, keyword_score, config.keyword_weight
    )

    return {
        "platform": config.name,
        "platform_key": platform.lower(),
        "total_score": round(total_score, 2),
        "subscores": {
            "keywords": round(keyword_score, 2),
            "role_match": round(role_match_score, 2),
            "formatting": round(formatting_score, 2),
        },
        "matched_skills": matched_keywords,
        "missing_skills": missing_keywords[:10],
        "focus_areas": config.focus_areas,
        "recommendations": recommendations,
    }


def generate_recommendations(
    platform: str,
    missing_skills: List[str],
    keyword_score: float,
    max_keyword_score: float,
) -> List[str]:
    """Generate platform-specific recommendations."""
    recommendations = []

    coverage = keyword_score / max_keyword_score if max_keyword_score > 0 else 0

    if coverage < 0.5:
        recommendations.append(
            f"Add more {platform.title()}-relevant keywords from the job description"
        )

    if missing_skills:
        recommendations.append(
            f"Add these missing skills: {', '.join(missing_skills[:5])}"
        )

    if platform == "linkedin":
        recommendations.append("Include certifications and leadership achievements")
    elif platform == "indeed":
        recommendations.append(
            "Ensure resume is in plain text format for better parsing"
        )
    elif platform == "greenhouse":
        recommendations.append(
            "Include diversity and culture fit keywords (collaborated, mentored, inclusive)"
        )

    if not recommendations:
        recommendations.append("Resume is well-optimized for this platform!")

    return recommendations


def simulate_linkedin_parsing(resume_text: str) -> Dict:
    """
    Simulate how LinkedIn would parse a resume.
    Focuses on skills extraction and profile completeness.
    """
    experience_section = extract_experience_section(resume_text)

    extracted_skills = extract_resume_skills(resume_text)

    has_contact = bool(
        re.search(r"\b[\w\.-]+@[\w\.-]+\.\w+", resume_text)
        or re.search(r"\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}", resume_text)
    )

    has_summary = bool(re.search(r"(?i)summary|objective|profile", resume_text))

    section_count = sum(
        1
        for keyword in ["experience", "education", "skills", "summary"]
        if keyword in resume_text.lower()
    )

    completeness_score = (
        (20 if has_contact else 0)
        + (20 if has_summary else 0)
        + (30 if extracted_skills else 0)
        + (30 * section_count / 4)
    )

    return {
        "contacts_found": has_contact,
        "summary_found": has_summary,
        "skills_found": list(extracted_skills)[:10],
        "sections_found": section_count,
        "profile_completeness": round(completeness_score, 2),
    }


def simulate_indeed_parsing(resume_text: str) -> Dict:
    """
    Simulate how Indeed's company ATS would parse a resume.
    Focuses on simple text parsing and key information extraction.
    """
    lines = resume_text.split("\n")

    job_titles = []
    companies = []
    dates = []

    for line in lines:
        if len(line) < 50 and any(
            word in line.lower()
            for word in ["engineer", "developer", "manager", "analyst", "designer"]
        ):
            job_titles.append(line.strip())

        if any(
            company in line
            for company in ["Google", "Microsoft", "Amazon", "Meta", "Apple", "Netflix"]
        ):
            companies.append(line.strip())

        date_match = re.search(
            r"(?i)(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[\s\d,]+", line
        )
        if date_match:
            dates.append(date_match.group())

    text_length = len(resume_text)
    is_too_short = text_length < 500
    is_too_long = text_length > 10000

    warnings_list = []
    if is_too_short:
        warnings_list = ["Resume too short"]
    elif is_too_long:
        warnings_list = ["Resume too long - may be truncated"]

    return {
        "job_titles_found": job_titles[:5],
        "companies_found": companies[:5],
        "dates_found": dates[:5],
        "text_length": text_length,
        "is_optimal_length": not is_too_short and not is_too_long,
        "warnings": warnings_list,
    }


def simulate_greenhouse_parsing(resume_text: str) -> Dict:
    """
    Simulate how Greenhouse ATS would parse a resume.
    Focuses on DEI keywords and culture fit.
    """
    dei_keywords = [
        "diversity",
        "inclusive",
        "equity",
        "accessible",
        "mentored",
        "coached",
        "collaborated",
        "team",
        "community",
    ]

    impact_keywords = [
        "achieved",
        "increased",
        "reduced",
        "improved",
        "transformed",
        "led",
        " Spearheaded",
    ]

    dei_matches = [kw for kw in dei_keywords if kw in resume_text.lower()]
    impact_matches = [kw for kw in impact_keywords if kw in resume_text.lower()]

    dei_score = min(50, len(dei_matches) * 15)
    impact_score = min(50, len(impact_matches) * 10)

    return {
        "dei_keywords_found": dei_matches,
        "impact_keywords_found": impact_matches,
        "dei_score": dei_score,
        "impact_score": impact_score,
        "culture_fit_indicators": len(dei_matches) + len(impact_matches),
    }


def simulate_glassdoor_parsing(resume_text: str) -> Dict:
    """
    Simulate how Glassdoor would parse a resume.
    Focuses on company reputation and salary-related keywords.
    """
    company_keywords = [
        "fortune",
        "fortune 500",
        "fortune 1000",
        "top company",
        "growth",
        "revenue",
        "valuation",
        "ipo",
    ]
    salary_keywords = [
        "salary",
        "compensation",
        "benefits",
        "equity",
        "stock options",
        "bonus",
        "paid time off",
        "remote",
        "flexible",
    ]

    company_matches = [kw for kw in company_keywords if kw in resume_text.lower()]
    salary_matches = [kw for kw in salary_keywords if kw in resume_text.lower()]

    # Check for company names
    top_companies = [
        "Google",
        "Microsoft",
        "Amazon",
        "Meta",
        "Apple",
        "Netflix",
        "Stripe",
        "Airbnb",
    ]
    companies_found = [c for c in top_companies if c in resume_text]

    return {
        "company_reputation_keywords": company_matches,
        "compensation_keywords": salary_matches,
        "top_companies_mentioned": companies_found,
        "company_score": min(50, len(company_matches) * 15 + len(companies_found) * 10),
        "salary_indicator": min(50, len(salary_matches) * 20),
    }


def simulate_monster_parsing(resume_text: str) -> Dict:
    """
    Simulate how Monster ATS would parse a resume.
    Focuses on standard formatting and keywords.
    """
    lines = resume_text.split("\n")

    # Check for standard sections
    has_experience = any("experience" in line.lower() for line in lines)
    has_education = any("education" in line.lower() for line in lines)
    has_skills = any("skills" in line.lower() for line in lines)

    section_score = sum([has_experience, has_education, has_skills]) * 20

    # Check for bullet points
    bullets = [line for line in lines if line.strip().startswith(("•", "-", "*"))]
    bullet_score = min(25, len(bullets) * 5)

    # Check for contact info
    has_email = bool(re.search(r"\b[\w\.-]+@[\w\.-]+\.\w+", resume_text))
    has_phone = bool(re.search(r"\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}", resume_text))
    contact_score = 25 if (has_email and has_phone) else 10

    return {
        "has_standard_sections": has_experience and has_education and has_skills,
        "has_bullet_points": len(bullets) > 0,
        "has_contact_info": has_email or has_phone,
        "formatting_score": section_score + bullet_score + contact_score,
    }


def simulate_lever_parsing(resume_text: str) -> Dict:
    """
    Simulate how Lever ATS would parse a resume.
    Focuses on culture fit and values-based language.
    """
    values_keywords = [
        "passionate",
        "motivated",
        "driven",
        "dedicated",
        "committed",
        "values",
        "mission",
        "purpose",
        "impact",
        "meaningful",
        "team player",
        "collaborative",
        "innovative",
        "creative",
    ]

    values_matches = [kw for kw in values_keywords if kw in resume_text.lower()]

    # Check for achievements
    achievement_keywords = [
        "achieved",
        "accomplished",
        "delivered",
        "exceeded",
        "awarded",
    ]
    achievement_matches = [
        kw for kw in achievement_keywords if kw in resume_text.lower()
    ]

    # Career progression indicators
    progression_keywords = ["promoted", "advanced", "grew", "expanded", "led"]
    progression_matches = [
        kw for kw in progression_keywords if kw in resume_text.lower()
    ]

    return {
        "values_keywords_found": values_matches,
        "achievement_keywords_found": achievement_matches,
        "progression_keywords_found": progression_matches,
        "culture_fit_score": min(50, len(values_matches) * 10),
        "impact_score": min(30, len(achievement_matches) * 10),
        "progression_score": min(20, len(progression_matches) * 5),
    }


def multi_platform_analysis(resume_text: str, job_description: str) -> Dict:
    """
    Run analysis across all supported platforms.
    Returns comparison results.
    """
    results = {}

    for platform in ATS_PLATFORMS.keys():
        platform_result = analyze_platform_ats(resume_text, job_description, platform)
        results[platform] = {
            "score": platform_result.get("total_score", 0),
            "matched": len(platform_result.get("matched_skills", [])),
            "missing": platform_result.get("missing_skills", []),
        }

    best_platform = max(results.keys(), key=lambda p: results[p]["score"])
    worst_platform = min(results.keys(), key=lambda p: results[p]["score"])

    return {
        "platforms": results,
        "best_platform": best_platform,
        "best_score": results[best_platform]["score"],
        "worst_platform": worst_platform,
        "worst_score": results[worst_platform]["score"],
        "recommendation": f"Best for {best_platform.title()} - focus on those keywords",
    }
