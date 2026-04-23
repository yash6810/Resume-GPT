import re
import math
from typing import List, Dict, Tuple, Set
from app.core.skills_loader import get_all_skills, load_skills
from app.core.embeddings import get_embedding_model
from app.models.schemas import SubScores, SkillMatch, AnalyzeResponse

# Constants for scoring weights
KEYWORDS_WEIGHT = 40
ROLE_MATCH_WEIGHT = 30
EXPERIENCE_RELEVANCE_WEIGHT = 20
QUALITY_WEIGHT = 10

# Action verbs for quality scoring
ACTION_VERBS = {
    "achieved",
    "improved",
    "trained",
    "managed",
    "created",
    "resolved",
    "negotiated",
    "developed",
    "launched",
    "increased",
    "decreased",
    "designed",
    "implemented",
    "led",
    "established",
    "built",
    "generated",
    "delivered",
    "optimized",
    "streamlined",
    "automated",
    "analyzed",
    "coordinated",
    "directed",
    "enhanced",
    "facilitated",
    "formulated",
    "initiated",
    "integrated",
    "maintained",
    "monitored",
    "orchestrated",
    "organized",
    "performed",
    "planned",
    "produced",
    "recommended",
    "reduced",
    "researched",
    "restructured",
    "revamped",
    "solved",
    "supervised",
    "transformed",
}

# Metric patterns
METRIC_PATTERNS = [
    r"\d+%",  # percentages
    r"\$\d+",  # dollar amounts
    r"\d+x",  # multipliers
    r"\d+:\d+",  # ratios
    r"\d{1,3}(?:,\d{3})+",  # large numbers with commas
]


def extract_skills_from_text(text: str) -> Set[str]:
    """Extract skills from text using exact matching."""
    all_skills = get_all_skills()
    if not all_skills:
        load_skills()
        all_skills = get_all_skills()

    text_lower = text.lower()
    found_skills = set()

    # Check for each skill in the text
    for skill in all_skills:
        # Use word boundary matching for better accuracy
        pattern = r"\b" + re.escape(skill) + r"\b"
        if re.search(pattern, text_lower):
            found_skills.add(skill)

    return found_skills


def extract_skills_semantic(text: str, threshold: float = 0.65) -> Set[str]:
    """Extract skills using semantic similarity."""
    embedding_model = get_embedding_model()
    all_skills = get_all_skills()

    if not all_skills:
        return set()

    # Build index if not already built
    if embedding_model.index is None:
        skills_list = list(all_skills)
        embedding_model.build_skill_index(skills_list)

    # Split text into sentences for better matching
    sentences = re.split(r"[.!?\n]", text)
    found_skills = set()

    for sentence in sentences:
        if len(sentence.strip()) < 10:
            continue

        similar_skills = embedding_model.find_similar_skills(
            sentence.strip(), top_k=3, threshold=threshold
        )
        for skill, score in similar_skills:
            found_skills.add(skill)

    return found_skills


def calculate_keywords_score(
    resume_skills: Set[str], jd_skills: Set[str]
) -> Tuple[float, List[SkillMatch], List[str]]:
    """Calculate keywords score based on skill matches."""
    if not jd_skills:
        return 0.0, [], []

    exact_matches = resume_skills.intersection(jd_skills)
    missing_skills = jd_skills - resume_skills

    # Calculate score
    exact_match_score = len(exact_matches) / len(jd_skills)
    keywords_score = exact_match_score * KEYWORDS_WEIGHT

    # Create skill matches list
    skill_matches = [SkillMatch(skill=skill, type="exact") for skill in exact_matches]

    return keywords_score, skill_matches, list(missing_skills)


def calculate_role_match_score(resume_text: str, job_description: str) -> float:
    """Calculate role match score using cosine similarity."""
    embedding_model = get_embedding_model()

    # Extract experience section if available
    experience_text = extract_experience_section(resume_text)
    if not experience_text:
        experience_text = resume_text[:1000]  # Fallback to first 1000 chars

    # Calculate cosine similarity
    similarity = embedding_model.cosine_similarity(experience_text, job_description)

    # Scale to weight
    role_match_score = similarity * ROLE_MATCH_WEIGHT

    return max(0, min(role_match_score, ROLE_MATCH_WEIGHT))


def calculate_experience_relevance_score(experience_text: str) -> float:
    """Calculate experience relevance based on metrics and impact."""
    if not experience_text:
        return 0.0

    score = 0.0

    # Check for metrics
    metrics_found = 0
    for pattern in METRIC_PATTERNS:
        matches = re.findall(pattern, experience_text)
        metrics_found += len(matches)

    # Score based on metrics presence
    if metrics_found >= 5:
        score += 15.0
    elif metrics_found >= 3:
        score += 10.0
    elif metrics_found >= 1:
        score += 5.0

    # Check for impact words
    impact_words = [
        "reduced",
        "increased",
        "improved",
        "optimized",
        "enhanced",
        "boosted",
        "accelerated",
    ]
    impact_found = sum(1 for word in impact_words if word in experience_text.lower())

    if impact_found >= 3:
        score += 5.0
    elif impact_found >= 1:
        score += 3.0

    return min(score, EXPERIENCE_RELEVANCE_WEIGHT)


def calculate_quality_score(resume_text: str) -> float:
    """Calculate quality score based on action verbs, bullet length, and structure."""
    if not resume_text:
        return 0.0

    score = 0.0

    # Extract bullets (lines starting with - or • or *)
    bullets = re.findall(r"^[\s]*[-•*][\s]*(.+)$", resume_text, re.MULTILINE)

    if not bullets:
        # Try to extract sentences as pseudo-bullets
        bullets = re.split(r"[.!?\n]", resume_text)
        bullets = [b.strip() for b in bullets if len(b.strip()) > 20]

    if not bullets:
        return 0.0

    # Check action verbs
    action_verb_count = 0
    for bullet in bullets:
        words = bullet.lower().split()
        if words and words[0] in ACTION_VERBS:
            action_verb_count += 1

    action_verb_ratio = action_verb_count / len(bullets) if bullets else 0
    score += min(action_verb_ratio * 10, 5.0)

    # Check bullet length (8-25 words is optimal)
    optimal_length_count = 0
    for bullet in bullets:
        word_count = len(bullet.split())
        if 8 <= word_count <= 25:
            optimal_length_count += 1

    optimal_length_ratio = optimal_length_count / len(bullets) if bullets else 0
    score += min(optimal_length_ratio * 10, 5.0)

    return min(score, QUALITY_WEIGHT)


def extract_experience_section(text: str) -> str:
    """Extract the experience section from resume text."""
    # Simple heuristic: look for common experience section headers
    experience_patterns = [
        r"(?i)experience.*?(?=education|skills|summary|projects|$)",
        r"(?i)work experience.*?(?=education|skills|summary|projects|$)",
        r"(?i)employment history.*?(?=education|skills|summary|projects|$)",
    ]

    for pattern in experience_patterns:
        match = re.search(pattern, text, re.DOTALL)
        if match:
            return match.group(0)[:2000]  # Limit to first 2000 chars

    return text[:2000]  # Fallback


def extract_jd_skills(job_description: str) -> Set[str]:
    """Extract required skills from job description."""
    # Combine exact and semantic matching
    exact_skills = extract_skills_from_text(job_description)

    # For semantic matching, we need to be more careful
    # Only add semantic matches that aren't already found
    try:
        semantic_skills = extract_skills_semantic(job_description, threshold=0.7)
        # Only add semantic matches that aren't already exact matches
        semantic_skills = semantic_skills - exact_skills
        all_jd_skills = exact_skills.union(semantic_skills)
    except Exception:
        # If semantic matching fails, just use exact matches
        all_jd_skills = exact_skills

    return all_jd_skills


def generate_recommendations(
    missing_skills: List[str], quality_issues: List[str]
) -> List[str]:
    """Generate actionable recommendations."""
    recommendations = []

    if missing_skills:
        recommendations.append(
            f"Add these missing skills to your resume: {', '.join(missing_skills[:5])}"
        )

    if "metrics" in quality_issues:
        recommendations.append(
            "Add quantifiable metrics to your experience bullets (e.g., percentages, dollar amounts)"
        )

    if "action_verbs" in quality_issues:
        recommendations.append(
            "Start more bullets with strong action verbs (e.g., Led, Developed, Implemented)"
        )

    if "bullet_length" in quality_issues:
        recommendations.append(
            "Keep bullets between 8-25 words for optimal readability"
        )

    if not recommendations:
        recommendations.append(
            "Your resume looks well-optimized! Consider tailoring it further for specific roles."
        )

    return recommendations


def analyze_resume(resume_text: str, job_description: str) -> AnalyzeResponse:
    """Main function to analyze resume against job description."""
    # Extract skills
    resume_skills = extract_skills_from_text(resume_text)
    jd_skills = extract_jd_skills(job_description)

    # Calculate scores
    keywords_score, skill_matches, missing_skills = calculate_keywords_score(
        resume_skills, jd_skills
    )
    role_match_score = calculate_role_match_score(resume_text, job_description)

    experience_text = extract_experience_section(resume_text)
    experience_relevance_score = calculate_experience_relevance_score(experience_text)
    quality_score = calculate_quality_score(resume_text)

    # Create subscores
    subscores = SubScores(
        keywords=round(keywords_score, 2),
        role_match=round(role_match_score, 2),
        experience_relevance=round(experience_relevance_score, 2),
        quality=round(quality_score, 2),
    )

    # Total score
    total_score = (
        keywords_score + role_match_score + experience_relevance_score + quality_score
    )
    total_score = round(min(max(total_score, 0), 100), 2)

    # Quality issues for recommendations
    quality_issues = []
    bullets = re.findall(r"^[\s]*[-•*][\s]*(.+)$", resume_text, re.MULTILINE)
    if not bullets:
        bullets = re.split(r"[.!?\n]", resume_text)
        bullets = [b.strip() for b in bullets if len(b.strip()) > 20]

    metrics_found = sum(
        1 for pattern in METRIC_PATTERNS for _ in re.findall(pattern, resume_text)
    )
    if metrics_found < 2:
        quality_issues.append("metrics")

    action_verb_count = sum(
        1
        for bullet in bullets
        if bullet.lower().split() and bullet.lower().split()[0] in ACTION_VERBS
    )
    if action_verb_count < len(bullets) * 0.3:
        quality_issues.append("action_verbs")

    recommendations = generate_recommendations(missing_skills, quality_issues)

    return AnalyzeResponse(
        ats_score=total_score,
        subscores=subscores,
        skill_matches=skill_matches,
        missing_skills=missing_skills,
        recommendations=recommendations,
    )
