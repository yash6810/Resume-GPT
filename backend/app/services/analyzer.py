
import re

def _extract_keywords(text: str) -> set:
    """Extracts keywords from text by lowercasing and splitting words."""
    # A more sophisticated implementation would use NLP libraries (e.g., NLTK, spaCy)
    # to handle stop words, stemming, lemmatization, and multi-word phrases.
    # For MVP, we do a simple split and filter.
    words = re.findall(r'\b\w+\b', text.lower())
    # Filter out very common short words that are unlikely to be keywords
    stop_words = set([
        "a", "an", "and", "are", "as", "at", "be", "by", "for", "from", "has", "he", "in", "is", "it", "its", "of", "on", "that", "the", "to", "was", "were", "will", "with"
    ])
    return {word for word in words if word not in stop_words and len(word) > 2} # Filter out short words and stop words

def analyze_resume_vs_jd(resume_text: str, resume_sections: dict, job_description: str) -> dict:
    """
    Compares resume content against a job description to identify matches, gaps, and suggestions.
    """
    jd_keywords = _extract_keywords(job_description)
    resume_keywords = _extract_keywords(resume_text)

    # Matched keywords
    matched_keywords = list(jd_keywords.intersection(resume_keywords))

    # Missing keywords (in JD but not in resume)
    missing_keywords = list(jd_keywords.difference(resume_keywords))

    # Calculate a simple match score
    # This is a very basic score; a real-world scenario would weigh keywords,
    # consider relevance, context, frequency, etc.
    if not jd_keywords:
        match_score = 0
    else:
        match_score = (len(matched_keywords) / len(jd_keywords)) * 100
        match_score = round(match_score, 2)

    # Generate basic suggestions
    suggestions = []
    if missing_keywords:
        suggestions.append(f"Consider adding or highlighting experience related to: {', '.join(missing_keywords[:5])} (top 5 missing keywords).")
    if match_score < 70:
        suggestions.append("Your resume could be better tailored to this job description. Try to incorporate more relevant keywords and quantify your achievements.")
    else:
        suggestions.append("Great job! Your resume seems well-aligned with the job description.")

    return {
        "match_score": match_score,
        "matched_keywords": matched_keywords,
        "missing_keywords": missing_keywords,
        "suggestions": suggestions,
        "jd_keywords_extracted": list(jd_keywords)
    }
