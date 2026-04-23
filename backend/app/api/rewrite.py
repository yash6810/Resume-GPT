from fastapi import APIRouter, HTTPException
from app.models.schemas import RewriteRequest, RewriteResponse
from app.services.llm import rewrite_bullet_with_llm
import re

router = APIRouter()

# Common action verbs for resume bullets
ACTION_VERBS = [
    "Achieved",
    "Improved",
    "Trained",
    "Managed",
    "Created",
    "Resolved",
    "Negotiated",
    "Developed",
    "Launched",
    "Increased",
    "Decreased",
    "Designed",
    "Implemented",
    "Led",
    "Established",
    "Built",
    "Generated",
    "Delivered",
    "Optimized",
    "Streamlined",
    "Automated",
    "Analyzed",
    "Coordinated",
    "Directed",
    "Enhanced",
    "Facilitated",
    "Formulated",
    "Initiated",
    "Integrated",
    "Maintained",
    "Monitored",
    "Orchestrated",
    "Organized",
    "Performed",
    "Planned",
    "Produced",
    "Recommended",
    "Reduced",
    "Researched",
    "Restructured",
    "Revamped",
    "Solved",
    "Supervised",
    "Transformed",
]


def generate_ats_variant(bullet: str, target_keywords: list[str]) -> str:
    """Generate ATS-optimized version of a bullet point."""
    words = bullet.split()

    # Ensure it starts with an action verb
    if words and words[0].lower() not in [v.lower() for v in ACTION_VERBS]:
        words.insert(0, "Developed")

    # Add target keywords naturally
    for keyword in target_keywords:
        if keyword.lower() not in bullet.lower():
            # Insert keyword in a natural way
            if "using" in bullet.lower():
                idx = words.index("using") + 1
                words.insert(idx, keyword)
            elif "with" in bullet.lower():
                idx = words.index("with") + 1
                words.insert(idx, keyword)
            else:
                # Add at the end with context
                words.extend(["using", keyword])

    # Ensure proper length (8-25 words)
    if len(words) < 8:
        words.extend(["resulting", "in", "improved", "performance"])
    elif len(words) > 25:
        words = words[:25]

    return " ".join(words)


def generate_human_variant(bullet: str, target_keywords: list[str]) -> str:
    """Generate human-friendly version of a bullet point."""
    words = bullet.split()

    # Ensure it starts with an action verb
    if words and words[0].lower() not in [v.lower() for v in ACTION_VERBS]:
        words.insert(0, "Led")

    # Add keywords more naturally
    for keyword in target_keywords:
        if keyword.lower() not in bullet.lower():
            # Add with more context
            if "developed" in bullet.lower() or "built" in bullet.lower():
                words.extend(["leveraging", keyword])
            elif "managed" in bullet.lower() or "led" in bullet.lower():
                words.extend(["with", "expertise", "in", keyword])
            else:
                words.extend(["utilizing", keyword])

    # Ensure proper length
    if len(words) < 8:
        words.extend(["achieving", "significant", "results"])
    elif len(words) > 25:
        words = words[:25]

    return " ".join(words)


@router.post("/rewrite", response_model=RewriteResponse)
async def rewrite_bullet(request: RewriteRequest):
    """
    Rewrite a resume bullet point with target keywords.
    Returns two variants: ATS-optimized and human-friendly.
    Uses LLM if configured, otherwise falls back to rule-based rewriting.
    """
    # Validate input
    if not request.bullet or not request.bullet.strip():
        raise HTTPException(status_code=400, detail="Bullet text is required")

    if not request.target_keywords:
        raise HTTPException(status_code=400, detail="Target keywords are required")

    try:
        # Try LLM first
        llm_result = rewrite_bullet_with_llm(request.bullet, request.target_keywords)
        if llm_result:
            return RewriteResponse(variants=llm_result)

        # Fall back to rule-based approach
        ats_variant = generate_ats_variant(request.bullet, request.target_keywords)
        human_variant = generate_human_variant(request.bullet, request.target_keywords)

        return RewriteResponse(variants=[ats_variant, human_variant])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error rewriting bullet: {str(e)}")
