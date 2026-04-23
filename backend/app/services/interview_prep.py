import os
import json
from typing import List, Optional, Dict
import requests

# Load environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
HUGGINGFACE_API_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")


def generate_questions_with_groq(
    resume_text: str, job_description: str, question_types: List[str]
) -> Optional[Dict]:
    """Use Groq to generate interview questions."""
    if not GROQ_API_KEY:
        return None

    prompt = f"""Based on this resume and job description, generate interview questions.

Resume:
{resume_text[:2000]}

Job Description:
{job_description[:2000]}

Generate questions for these types: {", ".join(question_types)}

For each question type, provide 3-5 questions with suggested answer tips.

Reply ONLY with JSON in this format:
{{
  "technical": [
    {{"question": "...", "tips": "..."}}
  ],
  "behavioral": [
    {{"question": "...", "tips": "..."}}
  ],
  "situational": [
    {{"question": "...", "tips": "..."}}
  ],
  "company": [
    {{"question": "...", "tips": "..."}}
  ]
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
                "max_tokens": 1500,
            },
            timeout=60,
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


def generate_questions_with_gemini(
    resume_text: str, job_description: str, question_types: List[str]
) -> Optional[Dict]:
    """Use Gemini to generate interview questions."""
    if not GEMINI_API_KEY:
        return None

    prompt = f"""Based on this resume and job description, generate interview questions.

Resume:
{resume_text[:2000]}

Job Description:
{job_description[:2000]}

Generate questions for these types: {", ".join(question_types)}

For each question type, provide 3-5 questions with suggested answer tips.

Format as JSON:
{{
  "technical": [
    {{"question": "...", "tips": "..."}}
  ],
  "behavioral": [
    {{"question": "...", "tips": "..."}}
  ],
  "situational": [
    {{"question": "...", "tips": "..."}}
  ],
  "company": [
    {{"question": "...", "tips": "..."}}
  ]
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
                        "maxOutputTokens": 1500,
                    },
                },
                timeout=60,
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


def generate_questions_with_openai(
    resume_text: str, job_description: str, question_types: List[str]
) -> Optional[Dict]:
    """Use OpenAI to generate interview questions."""
    if not OPENAI_API_KEY:
        return None

    prompt = f"""Based on this resume and job description, generate interview questions.

Resume:
{resume_text[:2000]}

Job Description:
{job_description[:2000]}

Generate questions for these types: {", ".join(question_types)}

For each question type, provide 3-5 questions with suggested answer tips.

Reply ONLY with JSON in this format:
{{
  "technical": [
    {{"question": "...", "tips": "..."}}
  ],
  "behavioral": [
    {{"question": "...", "tips": "..."}}
  ],
  "situational": [
    {{"question": "...", "tips": "..."}}
  ],
  "company": [
    {{"question": "...", "tips": "..."}}
  ]
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
                "max_tokens": 1500,
            },
            timeout=60,
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


def generate_interview_questions(
    resume_text: str, job_description: str, question_types: List[str] = None
) -> Dict:
    """Generate interview questions using available LLM providers."""
    if question_types is None:
        question_types = ["technical", "behavioral", "situational", "company"]

    # Try LLM providers in order
    result = generate_questions_with_groq(resume_text, job_description, question_types)
    if result:
        return result

    result = generate_questions_with_gemini(
        resume_text, job_description, question_types
    )
    if result:
        return result

    result = generate_questions_with_openai(
        resume_text, job_description, question_types
    )
    if result:
        return result

    # Rule-based fallback
    return generate_rule_based_questions(resume_text, job_description, question_types)


def generate_rule_based_questions(
    resume_text: str, job_description: str, question_types: List[str]
) -> Dict:
    """Generate interview questions using rule-based approach."""
    import re

    # Extract skills from job description
    common_skills = [
        "Python",
        "JavaScript",
        "Java",
        "C++",
        "SQL",
        "React",
        "Node.js",
        "AWS",
        "Docker",
        "Kubernetes",
        "Git",
        "Agile",
        "Scrum",
        "Leadership",
        "Communication",
    ]

    jd_lower = job_description.lower()
    mentioned_skills = [skill for skill in common_skills if skill.lower() in jd_lower]

    result = {}

    if "technical" in question_types:
        result["technical"] = [
            {
                "question": f"Can you explain your experience with {mentioned_skills[0] if mentioned_skills else 'the required technologies'}?",
                "tips": "Provide specific examples of projects and outcomes.",
            },
            {
                "question": "Walk me through how you would approach a complex technical problem.",
                "tips": "Use the STAR method: Situation, Task, Action, Result.",
            },
            {
                "question": "Describe a challenging bug you encountered and how you resolved it.",
                "tips": "Focus on your debugging process and what you learned.",
            },
        ]

    if "behavioral" in question_types:
        result["behavioral"] = [
            {
                "question": "Tell me about a time when you had to work under pressure to meet a deadline.",
                "tips": "Show how you prioritize and manage stress effectively.",
            },
            {
                "question": "Describe a situation where you had to collaborate with a difficult team member.",
                "tips": "Demonstrate your communication and conflict resolution skills.",
            },
            {
                "question": "Give an example of when you took initiative on a project.",
                "tips": "Highlight your proactive approach and leadership qualities.",
            },
        ]

    if "situational" in question_types:
        result["situational"] = [
            {
                "question": "How would you handle a situation where you disagree with your manager's approach?",
                "tips": "Show respect for hierarchy while advocating for your ideas.",
            },
            {
                "question": "What would you do if you discovered a critical bug right before a release?",
                "tips": "Demonstrate your judgment and risk assessment abilities.",
            },
            {
                "question": "How would you prioritize multiple urgent tasks with the same deadline?",
                "tips": "Explain your prioritization framework and communication approach.",
            },
        ]

    if "company" in question_types:
        result["company"] = [
            {
                "question": "Why do you want to work for this company?",
                "tips": "Research the company and align your values with theirs.",
            },
            {
                "question": "What do you know about our products/services?",
                "tips": "Show genuine interest and understanding of their business.",
            },
            {
                "question": "Where do you see yourself in 5 years?",
                "tips": "Align your career goals with the company's growth opportunities.",
            },
        ]

    return result
