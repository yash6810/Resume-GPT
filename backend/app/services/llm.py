import os
import json
from typing import List, Optional
import requests

# Load environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
HUGGINGFACE_API_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")


def rewrite_with_groq(bullet: str, target_keywords: List[str]) -> Optional[List[str]]:
    """Use Groq to rewrite bullet point (fastest, unlimited free tier)."""
    if not GROQ_API_KEY:
        return None

    prompt = f"""Rewrite this resume bullet point to include these keywords: {", ".join(target_keywords)}

Original: {bullet}

Provide exactly 2 versions:
1. ATS-optimized (keyword-rich, passes automated screening)
2. Human-friendly (natural, engaging for recruiters)

Reply ONLY with JSON, no other text: {{"ats": "...", "human": "..."}}"""

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
                "max_tokens": 300,
            },
            timeout=30,
        )

        if response.status_code == 200:
            result = response.json()
            content = result["choices"][0]["message"]["content"]
            # Try to parse JSON from response
            content = content.strip()
            # Extract JSON from markdown code blocks if present
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()
            # Find JSON object in the content
            import re

            json_match = re.search(r'\{[^{}]*"ats"[^{}]*"human"[^{}]*\}', content)
            if json_match:
                content = json_match.group()
            parsed = json.loads(content)
            return [parsed["ats"], parsed["human"]]
    except Exception as e:
        print(f"Groq error: {e}")

    return None


def rewrite_with_gemini(bullet: str, target_keywords: List[str]) -> Optional[List[str]]:
    """Use Gemini to rewrite bullet point."""
    if not GEMINI_API_KEY:
        return None

    prompt = f"""Rewrite this resume bullet point to include these keywords: {", ".join(target_keywords)}

Original: {bullet}

Provide exactly 2 versions:
1. ATS-optimized (keyword-rich, passes automated screening)
2. Human-friendly (natural, engaging for recruiters)

Format as JSON: {{"ats": "...", "human": "..."}}"""

    # Try multiple models in case of quota limits
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
                        "maxOutputTokens": 300,
                    },
                },
                timeout=30,
            )

            if response.status_code == 200:
                result = response.json()
                content = result["candidates"][0]["content"]["parts"][0]["text"]
                # Try to parse JSON from response
                content = content.strip()
                if content.startswith("```"):
                    content = content.split("\n", 1)[1].rsplit("```", 1)[0].strip()
                parsed = json.loads(content)
                return [parsed["ats"], parsed["human"]]
            elif response.status_code == 429:
                # Quota exceeded, try next model
                continue
        except Exception as e:
            print(f"Gemini error ({model}): {e}")
            continue

    return None


def rewrite_with_openai(bullet: str, target_keywords: List[str]) -> Optional[List[str]]:
    """Use OpenAI to rewrite bullet point."""
    if not OPENAI_API_KEY:
        return None

    prompt = f"""Rewrite this resume bullet point to include these keywords: {", ".join(target_keywords)}

Original: {bullet}

Provide exactly 2 versions:
1. ATS-optimized (keyword-rich, passes automated screening)
2. Human-friendly (natural, engaging for recruiters)

Format as JSON: {{"ats": "...", "human": "..."}}"""

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
                "max_tokens": 300,
            },
            timeout=30,
        )

        if response.status_code == 200:
            result = response.json()
            content = result["choices"][0]["message"]["content"]
            parsed = json.loads(content)
            return [parsed["ats"], parsed["human"]]
    except Exception as e:
        print(f"OpenAI error: {e}")

    return None


def rewrite_with_huggingface(
    bullet: str, target_keywords: List[str]
) -> Optional[List[str]]:
    """Use HuggingFace Inference API to rewrite bullet point."""
    if not HUGGINGFACE_API_TOKEN:
        return None

    prompt = f"""Rewrite this resume bullet point to include: {", ".join(target_keywords)}

Original: {bullet}

ATS version:"""

    try:
        response = requests.post(
            "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2",
            headers={
                "Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}",
                "Content-Type": "application/json",
            },
            json={
                "inputs": prompt,
                "parameters": {
                    "max_new_tokens": 200,
                    "temperature": 0.7,
                    "return_full_text": False,
                },
            },
            timeout=60,
        )

        if response.status_code == 200:
            result = response.json()
            text = result[0]["generated_text"].strip()

            # Parse the response into two variants
            if "\n" in text:
                parts = text.split("\n", 1)
                ats = parts[0].strip()
                human = parts[1].strip() if len(parts) > 1 else ats
                return [ats, human]
            return [text, text]
    except Exception as e:
        print(f"HuggingFace error: {e}")

    return None


def rewrite_bullet_with_llm(
    bullet: str, target_keywords: List[str]
) -> Optional[List[str]]:
    """
    Try to rewrite bullet using available LLM services.
    Priority: Groq (fastest) → Gemini → OpenAI → HuggingFace → Rule-based
    """
    # Try Groq first (fastest, unlimited free tier)
    result = rewrite_with_groq(bullet, target_keywords)
    if result:
        return result

    # Try Gemini only if Groq failed
    result = rewrite_with_gemini(bullet, target_keywords)
    if result:
        return result

    # Try OpenAI
    result = rewrite_with_openai(bullet, target_keywords)
    if result:
        return result

    # Fall back to HuggingFace
    result = rewrite_with_huggingface(bullet, target_keywords)
    if result:
        return result

    # Rule-based fallback always returns a result
    return None
