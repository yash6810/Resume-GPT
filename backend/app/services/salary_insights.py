import os
import json
from typing import Optional, Dict, List
import requests

# Load environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
HUGGINGFACE_API_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")


def estimate_salary_with_groq(
    skills: List[str], job_title: str, location: str, years_experience: int
) -> Optional[Dict]:
    """Use Groq to estimate salary range."""
    if not GROQ_API_KEY:
        return None

    prompt = f"""Based on the following information, estimate the salary range in USD.

Job Title: {job_title}
Location: {location}
Years of Experience: {years_experience}
Key Skills: {", ".join(skills[:10])}

Provide a salary estimate with:
1. Minimum salary (USD)
2. Maximum salary (USD)
3. Median salary (USD)
4. Factors affecting the salary
5. Tips to increase earning potential

Reply ONLY with JSON in this format:
{{
  "min_salary": 80000,
  "max_salary": 120000,
  "median_salary": 100000,
  "currency": "USD",
  "factors": ["factor1", "factor2"],
  "tips": ["tip1", "tip2"],
  "market_trend": "growing/stable/declining"
}}"""

    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": "llama-3.1-8b-instant",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.7,
                "max_tokens": 500,
            },
            timeout=30,
        )

        if response.status_code == 200:
            result = response.json()
            content = result["choices"][0]["message"]["content"]
            content = content.strip()

            # Extract JSON from markdown code blocks if present
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()

            # Find JSON object in the content
            import re

            json_match = re.search(r"\{[\s\S]*\}", content)
            if json_match:
                content = json_match.group()

            parsed = json.loads(content)
            return parsed
    except Exception as e:
        print(f"Groq error: {e}")

    return None


def estimate_salary_with_gemini(
    skills: List[str], job_title: str, location: str, years_experience: int
) -> Optional[Dict]:
    """Use Gemini to estimate salary range."""
    if not GEMINI_API_KEY:
        return None

    prompt = f"""Based on the following information, estimate the salary range in USD.

Job Title: {job_title}
Location: {location}
Years of Experience: {years_experience}
Key Skills: {", ".join(skills[:10])}

Provide a salary estimate with:
1. Minimum salary (USD)
2. Maximum salary (USD)
3. Median salary (USD)
4. Factors affecting the salary
5. Tips to increase earning potential

Format as JSON:
{{
  "min_salary": 80000,
  "max_salary": 120000,
  "median_salary": 100000,
  "currency": "USD",
  "factors": ["factor1", "factor2"],
  "tips": ["tip1", "tip2"],
  "market_trend": "growing/stable/declining"
}}"""

    models = ["gemini-2.5-flash", "gemini-2.0-flash-lite", "gemini-2.0-flash"]

    for model in models:
        try:
            response = requests.post(
                f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={GEMINI_API_KEY}",
                headers={"Content-Type": "application/json"},
                json={
                    "contents": [{"parts": [{"text": prompt}]}],
                    "generationConfig": {
                        "temperature": 0.7,
                        "maxOutputTokens": 500,
                    },
                },
                timeout=30,
            )

            if response.status_code == 200:
                result = response.json()
                content = result["candidates"][0]["content"]["parts"][0]["text"]
                content = content.strip()

                # Extract JSON from markdown code blocks if present
                if "```json" in content:
                    content = content.split("```json")[1].split("```")[0].strip()
                elif "```" in content:
                    content = content.split("```")[1].split("```")[0].strip()

                import re

                json_match = re.search(r"\{[\s\S]*\}", content)
                if json_match:
                    content = json_match.group()

                parsed = json.loads(content)
                return parsed
        except Exception as e:
            print(f"Gemini error ({model}): {e}")
            continue

    return None


def estimate_salary_with_openai(
    skills: List[str], job_title: str, location: str, years_experience: int
) -> Optional[Dict]:
    """Use OpenAI to estimate salary range."""
    if not OPENAI_API_KEY:
        return None

    prompt = f"""Based on the following information, estimate the salary range in USD.

Job Title: {job_title}
Location: {location}
Years of Experience: {years_experience}
Key Skills: {", ".join(skills[:10])}

Provide a salary estimate with:
1. Minimum salary (USD)
2. Maximum salary (USD)
3. Median salary (USD)
4. Factors affecting the salary
5. Tips to increase earning potential

Reply ONLY with JSON in this format:
{{
  "min_salary": 80000,
  "max_salary": 120000,
  "median_salary": 100000,
  "currency": "USD",
  "factors": ["factor1", "factor2"],
  "tips": ["tip1", "tip2"],
  "market_trend": "growing/stable/declining"
}}"""

    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENAI_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": "gpt-3.5-turbo",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.7,
                "max_tokens": 500,
            },
            timeout=30,
        )

        if response.status_code == 200:
            result = response.json()
            content = result["choices"][0]["message"]["content"]
            content = content.strip()

            # Extract JSON from markdown code blocks if present
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()

            import re

            json_match = re.search(r"\{[\s\S]*\}", content)
            if json_match:
                content = json_match.group()

            parsed = json.loads(content)
            return parsed
    except Exception as e:
        print(f"OpenAI error: {e}")

    return None


def estimate_salary(
    skills: List[str], job_title: str, location: str, years_experience: int
) -> Dict:
    """Estimate salary using available LLM providers."""
    # Try LLM providers in order
    result = estimate_salary_with_groq(skills, job_title, location, years_experience)
    if result:
        result["provider"] = "groq"
        return result

    result = estimate_salary_with_gemini(skills, job_title, location, years_experience)
    if result:
        result["provider"] = "gemini"
        return result

    result = estimate_salary_with_openai(skills, job_title, location, years_experience)
    if result:
        result["provider"] = "openai"
        return result

    # Rule-based fallback
    return estimate_salary_rule_based(skills, job_title, location, years_experience)


def estimate_salary_rule_based(
    skills: List[str], job_title: str, location: str, years_experience: int
) -> Dict:
    """Estimate salary using rule-based approach."""
    # Base salary ranges by job title (in USD)
    base_salaries = {
        "software engineer": {"min": 80000, "max": 150000},
        "senior software engineer": {"min": 120000, "max": 200000},
        "data scientist": {"min": 90000, "max": 160000},
        "product manager": {"min": 100000, "max": 180000},
        "devops engineer": {"min": 90000, "max": 160000},
        "frontend developer": {"min": 70000, "max": 140000},
        "backend developer": {"min": 80000, "max": 150000},
        "full stack developer": {"min": 80000, "max": 150000},
        "machine learning engineer": {"min": 100000, "max": 180000},
        "data engineer": {"min": 90000, "max": 160000},
        "project manager": {"min": 70000, "max": 130000},
        "ux designer": {"min": 70000, "max": 130000},
        "marketing manager": {"min": 60000, "max": 120000},
        "sales representative": {"min": 40000, "max": 100000},
    }

    # Location multipliers
    location_multipliers = {
        "san francisco": 1.4,
        "new york": 1.35,
        "seattle": 1.3,
        "boston": 1.25,
        "austin": 1.15,
        "denver": 1.1,
        "chicago": 1.1,
        "los angeles": 1.2,
        "remote": 1.0,
        "default": 0.9,
    }

    # High-demand skill bonuses
    premium_skills = {
        "machine learning": 15000,
        "deep learning": 20000,
        "aws": 10000,
        "kubernetes": 10000,
        "docker": 5000,
        "react": 8000,
        "python": 5000,
        "java": 5000,
        "go": 10000,
        "rust": 15000,
    }

    # Find base salary
    title_lower = job_title.lower()
    base = base_salaries.get("software engineer")  # default

    for key, salary_range in base_salaries.items():
        if key in title_lower:
            base = salary_range
            break

    # Apply location multiplier
    location_lower = location.lower()
    multiplier = location_multipliers["default"]
    for loc, mult in location_multipliers.items():
        if loc in location_lower:
            multiplier = mult
            break

    # Apply experience adjustment (5% per year up to 20 years)
    exp_multiplier = 1 + (min(years_experience, 20) * 0.05)

    # Calculate salary range
    min_salary = int(base["min"] * multiplier * exp_multiplier)
    max_salary = int(base["max"] * multiplier * exp_multiplier)

    # Add skill bonuses
    skill_bonus = 0
    for skill in skills:
        skill_lower = skill.lower()
        for premium_skill, bonus in premium_skills.items():
            if premium_skill in skill_lower:
                skill_bonus += bonus
                break

    min_salary += skill_bonus
    max_salary += skill_bonus
    median_salary = (min_salary + max_salary) // 2

    # Generate factors
    factors = []
    if years_experience > 5:
        factors.append("Strong experience level commands higher compensation")
    if any(s.lower() in ["machine learning", "deep learning", "ai"] for s in skills):
        factors.append("AI/ML skills are in high demand")
    if any(s.lower() in ["aws", "azure", "gcp"] for s in skills):
        factors.append("Cloud expertise increases market value")
    if multiplier > 1.2:
        factors.append("High cost-of-living area affects base salary")
    if not factors:
        factors.append("Market rate for this role and experience level")

    # Generate tips
    tips = []
    if years_experience < 5:
        tips.append(
            "Gain 3-5 years of experience to significantly increase earning potential"
        )
    if not any(s.lower() in ["aws", "azure", "gcp"] for s in skills):
        tips.append("Add cloud certifications (AWS/Azure/GCP) to boost salary")
    if not any(s.lower() in ["machine learning", "data science"] for s in skills):
        tips.append("Consider adding ML/Data Science skills for higher compensation")
    tips.append("Negotiate based on total compensation (salary + equity + benefits)")
    tips.append("Research company salary ranges on Glassdoor and Levels.fyi")

    return {
        "min_salary": min_salary,
        "max_salary": max_salary,
        "median_salary": median_salary,
        "currency": "USD",
        "factors": factors,
        "tips": tips,
        "market_trend": "growing",
        "provider": "rule-based",
    }
