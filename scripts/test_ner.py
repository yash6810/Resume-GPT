"""
Test the trained NER model on sample resumes.
Verifies model accuracy and entity extraction.

Usage:
    python scripts/test_ner.py
"""

import sys
import os
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Add backend to path
BACKEND_PATH = PROJECT_ROOT / "backend"
sys.path.insert(0, str(BACKEND_PATH))


def test_ner_model():
    """Test the NER model with sample resumes."""
    print("=" * 60)
    print("ResumeGPT NER Model Tester")
    print("=" * 60)

    # Import NER service
    try:
        from app.services.ner import get_ner_service

        ner_service = get_ner_service()
    except ImportError as e:
        print(f"ERROR: Could not import NER service: {e}")
        print("Make sure you're running from the project root.")
        return

    # Check model status
    print("\nModel Status:")
    if ner_service.nlp:
        print(f"  [OK] Model loaded: {type(ner_service.nlp).__name__}")
        print(f"  Pipeline: {ner_service.nlp.pipe_names}")
    else:
        print("  [FAIL] No model loaded")

    # Test resumes
    test_resumes = [
        {
            "name": "Software Engineer Resume",
            "text": """
John Smith
Senior Software Engineer
Email: john.smith@gmail.com | Phone: (555) 123-4567
LinkedIn: linkedin.com/in/johnsmith | GitHub: github.com/johnsmith
Location: San Francisco, CA

SUMMARY
Experienced software engineer with 5 years of expertise in full-stack development.

EXPERIENCE
Senior Software Engineer at Google (2020 - Present)
- Developed microservices using Python and Go
- Led team of 5 engineers on cloud infrastructure project
- Reduced API latency by 40%

Software Engineer at Microsoft (2018 - 2020)
- Built React applications serving 1M+ users
- Implemented CI/CD pipelines with Jenkins

SKILLS
Python, JavaScript, React, Node.js, Go, AWS, Docker, Kubernetes, PostgreSQL

EDUCATION
Bachelor of Science in Computer Science, Stanford University, 2018
GPA: 3.8

CERTIFICATIONS
AWS Certified Solutions Architect
Google Cloud Professional Developer
            """,
        },
        {
            "name": "Data Scientist Resume",
            "text": """
Jane Doe
Data Scientist
Email: jane.doe@outlook.com | Phone: (555) 987-6543
Location: New York, NY

PROFESSIONAL EXPERIENCE
Data Scientist at Amazon (2021 - Present)
- Built ML models for demand forecasting using TensorFlow
- Analyzed 10TB+ datasets using Spark and Hadoop
- Improved prediction accuracy by 25%

Junior Data Analyst at Netflix (2019 - 2021)
- Created dashboards using Tableau and PowerBI
- Performed A/B testing for recommendation algorithms

EDUCATION
Master of Science in Data Science, MIT, 2019
Bachelor of Arts in Statistics, UC Berkeley, 2017

SKILLS
Python, R, SQL, TensorFlow, PyTorch, Scikit-learn, Pandas, Spark, Tableau

CERTIFICATIONS
TensorFlow Developer Certificate
            """,
        },
    ]

    # Run tests
    print("\n" + "=" * 60)
    print("Testing Entity Extraction")
    print("=" * 60)

    total_entities = 0
    entity_counts = {}

    for resume in test_resumes:
        print(f"\n--- {resume['name']} ---")

        # Extract entities
        entities = ner_service.extract_entities(resume["text"])
        skills = ner_service.extract_skills(resume["text"])
        sections = ner_service.extract_sections(resume["text"])

        # Count entities
        for entity_type, values in entities.items():
            if values:
                count = len(values)
                total_entities += count
                entity_counts[entity_type] = entity_counts.get(entity_type, 0) + count
                print(f"  {entity_type}: {values}")

        if skills:
            print(f"  SKILLS (from skills.json): {skills[:10]}...")  # Show first 10

        print(f"  Sections found: {list(sections.keys())}")

    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    print(f"Total entities extracted: {total_entities}")
    print("\nEntity distribution:")
    for entity_type, count in sorted(entity_counts.items(), key=lambda x: -x[1]):
        print(f"  {entity_type}: {count}")

    # Sample specific tests
    print("\n" + "=" * 60)
    print("Specific Entity Tests")
    print("=" * 60)

    test_cases = [
        ("Email extraction", "Contact me at test@example.com", ["EMAIL"]),
        ("Phone extraction", "Call me at (555) 123-4567", ["PHONE"]),
        ("URL extraction", "Visit https://github.com/user", ["URL"]),
        ("LinkedIn extraction", "linkedin.com/in/username", ["LINKEDIN"]),
    ]

    for test_name, text, expected_types in test_cases:
        entities = ner_service.extract_entities(text)
        found = any(entities.get(t) for t in expected_types)
        status = "[PASS]" if found else "[FAIL]"
        print(f"{status} - {test_name}")

    print("\n" + "=" * 60)
    print("Testing Complete!")
    print("=" * 60)


if __name__ == "__main__":
    test_ner_model()
