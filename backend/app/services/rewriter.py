def rewrite_bullet_point(bullet_point: str, target_keywords: str) -> str:
    """
    Rewrites a resume bullet point to incorporate target keywords.
    For MVP, this is a simple rule-based rewriter.
    A more advanced version would use an LLM.
    """
    keywords_list = [k.strip() for k in target_keywords.split(',') if k.strip()]

    if not keywords_list:
        return bullet_point # No keywords to add

    # Simple approach: append keywords to the end or try to integrate them
    # For MVP, let's just append or rephrase to include them.
    # A more sophisticated approach would involve NLP for context-aware insertion.
    
    # Check if the bullet point already ends with a punctuation mark
    if bullet_point and bullet_point[-1] in ['.', '!', '?']:
        rewritten_bullet = f"{bullet_point[:-1]}, incorporating {', '.join(keywords_list)}."
    else:
        rewritten_bullet = f"{bullet_point} (incorporating {', '.join(keywords_list)})."
        
    return rewritten_bullet