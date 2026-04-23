"""
Download Resume NER datasets from multiple sources.
Combines them into a unified format for training.

Datasets:
1. yashpwr/resume-ner-training-data (HuggingFace) - 22,855 examples
2. dotin-inc/resume-dataset-NER-annotations (GitHub) - 545 resumes
3. Custom synthetic data generation

Output: backend/data/ner_datasets/raw/combined_dataset.json
"""

import json
import os
import re
import sys
from pathlib import Path
from typing import List, Dict, Any

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


def extract_entities_from_text(text: str) -> List[Dict]:
    """
    Extract entities from resume text using regex patterns.
    Returns list of entity dicts with start, end, label.
    """
    entities = []

    patterns = {
        "EMAIL": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
        "PHONE": r"\b(?:\+?1[-.]?)?\(?[0-9]{3}\)?[-.]?[0-9]{3}[-.]?[0-9]{4}\b",
        "URL": r"https?://(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&/=]*)",
        "LINKEDIN": r"linkedin\.com/in/[a-zA-Z0-9-]+",
        "GITHUB": r"github\.com/[a-zA-Z0-9-]+",
        "YEAR": r"\b(?:19|20)\d{2}\b",
    }

    for label, pattern in patterns.items():
        for match in re.finditer(pattern, text, re.IGNORECASE):
            entities.append(
                {"start": match.start(), "end": match.end(), "label": label}
            )

    return entities


def download_huggingface_dataset() -> List[Dict]:
    """
    Download yashpwr/resume-ner-training-data from HuggingFace.
    Dataset format: {"messages": [{"role": "...", "content": "..."}]}
    We extract resume text from 'user' messages and create entity labels.
    """
    print("=" * 60)
    print("Downloading yashpwr/resume-ner-training-data from HuggingFace...")
    print("=" * 60)

    try:
        from datasets import load_dataset

        dataset = load_dataset("yashpwr/resume-ner-training-data", split="train")
        print(f"Downloaded {len(dataset)} examples")

        # Convert chat format to NER training format
        examples = []
        skipped = 0

        for item in dataset:
            messages = item.get("messages", [])

            # Extract resume text from user message
            resume_text = ""
            for msg in messages:
                if msg.get("role") == "user":
                    content = msg.get("content", "")
                    # Remove common prefixes
                    content = content.replace(
                        "Please summarize the following resume:", ""
                    )
                    content = content.replace("Summarize this resume:", "")
                    content = content.replace("Please analyze this resume:", "")
                    resume_text = content.strip()
                    break

            # Skip if no resume text or too short
            if not resume_text or len(resume_text) < 50:
                skipped += 1
                continue

            # Extract entities using regex
            entities = extract_entities_from_text(resume_text)

            examples.append(
                {"text": resume_text, "entities": entities, "source": "yashpwr"}
            )

        print(f"Converted {len(examples)} examples from HuggingFace")
        if skipped > 0:
            print(f"  Skipped {skipped} examples (no resume text or too short)")
        return examples

    except ImportError:
        print("ERROR: 'datasets' library not installed.")
        print("Install with: pip install datasets")
        return []
    except Exception as e:
        print(f"ERROR downloading HuggingFace dataset: {e}")
        import traceback

        traceback.print_exc()
        return []


def download_github_dataset() -> List[Dict]:
    """
    Download dotin-inc/resume-dataset-NER-annotations from GitHub.
    Returns list of training examples.
    Dataset format: XML with <label type="...">text</label> tags
    """
    print("\n" + "=" * 60)
    print("Downloading dotin-inc/resume-dataset-NER-annotations from GitHub...")
    print("=" * 60)

    try:
        import requests
        import zipfile
        import io
        import re

        # Label type mapping to our entity types
        LABEL_MAP = {
            "Name": "PERSON",
            "Location": "LOCATION",
            "Email Address": "EMAIL",
            "Designation": "JOB_TITLE",
            "Job Specific Skills": "SKILL",
            "Soft Skills": "SKILL",
            "Companies worked at": "COMPANY",
            "Years of Experience": "YEARS_EXPERIENCE",
            "College Name": "SCHOOL",
            "Degree": "DEGREE",
            "Graduation Year": "GRADUATION_YEAR",
            "Certifications": "CERTIFICATION",
        }

        def parse_xml_to_entities(xml_content: str) -> tuple:
            """Parse XML content and extract text with entity spans."""
            # Remove XML header
            xml_content = re.sub(r"<\?xml[^?]*\?>", "", xml_content)
            xml_content = xml_content.replace("<cv>", "").replace("</cv>", "")

            # Extract entities from label tags
            entities = []
            clean_text = xml_content

            # Pattern: <label type="TYPE">TEXT</label>
            pattern = r'<label\s+type="([^"]+)"[^>]*>([^<]+)</label>'

            offset = 0
            for match in re.finditer(pattern, xml_content):
                label_type = match.group(1)
                entity_text = match.group(2)
                full_match = match.group(0)

                # Map label type to our types
                mapped_label = LABEL_MAP.get(label_type, None)

                if mapped_label:
                    # Find position in clean text
                    start = clean_text.find(full_match, offset)
                    if start != -1:
                        # Replace label tag with just text
                        clean_text = (
                            clean_text[:start]
                            + entity_text
                            + clean_text[start + len(full_match) :]
                        )
                        end = start + len(entity_text)
                        entities.append(
                            {"start": start, "end": end, "label": mapped_label}
                        )
                        offset = end
                    else:
                        # Fallback: just remove the tag
                        clean_text = clean_text.replace(full_match, entity_text, 1)
                else:
                    # Unknown label type: just remove the tag
                    clean_text = clean_text.replace(full_match, entity_text, 1)

            # Clean up extra whitespace
            clean_text = re.sub(r"\s+", " ", clean_text).strip()

            return clean_text, entities

        url = "https://github.com/dotin-inc/resume-dataset-NER-annotations/archive/refs/heads/master.zip"
        print(f"Downloading from {url}...")

        response = requests.get(url, timeout=60)
        response.raise_for_status()

        examples = []

        # Outer zip contains nested zip files
        with zipfile.ZipFile(io.BytesIO(response.content)) as outer_z:
            print(f"  Found {len(outer_z.namelist())} files in outer archive")

            # Find nested zip files (training data)
            nested_zips = [f for f in outer_z.namelist() if f.endswith(".zip")]
            print(f"  Found {len(nested_zips)} nested zip files")

            for nested_zip_name in nested_zips:
                if "test" in nested_zip_name.lower():
                    print(f"  Skipping test data: {nested_zip_name}")
                    continue

                print(f"  Processing: {nested_zip_name}")

                try:
                    with outer_z.open(nested_zip_name) as nested_file:
                        nested_content = nested_file.read()

                        # Open the nested zip
                        with zipfile.ZipFile(io.BytesIO(nested_content)) as inner_z:
                            # Find XML files
                            xml_files = [
                                f for f in inner_z.namelist() if f.endswith(".xml")
                            ]
                            print(f"    Found {len(xml_files)} XML files")

                            for xml_file in xml_files:
                                try:
                                    with inner_z.open(xml_file) as f:
                                        content = f.read().decode("utf-8")

                                        # Parse XML to extract text and entities
                                        text, entities = parse_xml_to_entities(content)

                                        if text and len(text) > 50:
                                            examples.append(
                                                {
                                                    "text": text,
                                                    "entities": entities,
                                                    "source": "dotin",
                                                }
                                            )

                                except (UnicodeDecodeError, Exception) as e:
                                    continue

                except Exception as e:
                    print(f"    Error processing {nested_zip_name}: {e}")
                    continue

        print(f"Downloaded {len(examples)} examples from GitHub")
        return examples

    except Exception as e:
        print(f"ERROR downloading GitHub dataset: {e}")
        import traceback

        traceback.print_exc()
        return []


def generate_synthetic_data() -> List[Dict]:
    """
    Generate synthetic resume training data.
    This augments the dataset with more varied examples.
    """
    print("\n" + "=" * 60)
    print("Generating synthetic training data...")
    print("=" * 60)

    templates = [
        {
            "text": "{name} is a {job_title} at {company} with {years} years of experience in {skills}.",
            "entities": [
                {"start": 0, "end": 1, "label": "PERSON"},
                {"start": 10, "end": 11, "label": "JOB_TITLE"},
                {"start": 15, "end": 16, "label": "COMPANY"},
                {"start": 22, "end": 23, "label": "YEARS_EXPERIENCE"},
                {"start": 28, "end": 29, "label": "SKILL"},
            ],
        },
        {
            "text": "Graduated with a {degree} from {school} in {year}.",
            "entities": [
                {"start": 14, "end": 15, "label": "DEGREE"},
                {"start": 21, "end": 22, "label": "SCHOOL"},
                {"start": 26, "end": 27, "label": "GRADUATION_YEAR"},
            ],
        },
        {
            "text": "Contact: {email} | {phone} | {linkedin}",
            "entities": [
                {"start": 9, "end": 10, "label": "EMAIL"},
                {"start": 12, "end": 13, "label": "PHONE"},
                {"start": 15, "end": 16, "label": "LINKEDIN"},
            ],
        },
    ]

    # Sample data for filling templates
    fill_data = {
        "name": [
            "John Smith",
            "Jane Doe",
            "Michael Johnson",
            "Emily Williams",
            "David Brown",
        ],
        "job_title": [
            "Software Engineer",
            "Data Scientist",
            "Product Manager",
            "DevOps Engineer",
            "UX Designer",
        ],
        "company": ["Google", "Microsoft", "Amazon", "Apple", "Meta"],
        "years": ["3", "5", "7", "10", "2"],
        "skills": [
            "Python, JavaScript, React",
            "Machine Learning, TensorFlow",
            "Agile, Scrum",
            "AWS, Docker, Kubernetes",
            "Figma, Sketch",
        ],
        "degree": [
            "Bachelor of Science in Computer Science",
            "Master of Data Science",
            "MBA",
            "PhD in Artificial Intelligence",
        ],
        "school": [
            "MIT",
            "Stanford University",
            "Harvard University",
            "UC Berkeley",
            "Carnegie Mellon",
        ],
        "year": ["2020", "2019", "2021", "2018", "2022"],
        "email": [
            "john.smith@email.com",
            "jane.doe@gmail.com",
            "michael.j@outlook.com",
        ],
        "phone": ["(555) 123-4567", "(555) 987-6543", "(555) 246-8135"],
        "linkedin": [
            "linkedin.com/in/johnsmith",
            "linkedin.com/in/janedoe",
            "linkedin.com/in/michaelj",
        ],
    }

    examples = []
    for _ in range(500):  # Generate 500 synthetic examples
        template = templates[len(examples) % len(templates)]
        text = template["text"]

        # Fill in template
        for key, values in fill_data.items():
            if "{" + key + "}" in text:
                import random

                text = text.replace("{" + key + "}", random.choice(values), 1)

        examples.append(
            {"text": text, "entities": template["entities"], "source": "synthetic"}
        )

    print(f"Generated {len(examples)} synthetic examples")
    return examples


def save_combined_dataset(
    huggingface_data: List[Dict],
    github_data: List[Dict],
    synthetic_data: List[Dict],
    output_path: str,
):
    """Save combined dataset to JSON file."""
    print("\n" + "=" * 60)
    print("Saving combined dataset...")
    print("=" * 60)

    combined = {
        "metadata": {
            "total_examples": len(huggingface_data)
            + len(github_data)
            + len(synthetic_data),
            "sources": {
                "huggingface": len(huggingface_data),
                "github": len(github_data),
                "synthetic": len(synthetic_data),
            },
            "entity_types": [
                "PERSON",
                "EMAIL",
                "PHONE",
                "LOCATION",
                "SKILL",
                "COMPANY",
                "JOB_TITLE",
                "DEGREE",
                "SCHOOL",
                "GRADUATION_YEAR",
                "CERTIFICATION",
                "YEARS_EXPERIENCE",
                "LINKEDIN",
                "URL",
            ],
        },
        "examples": huggingface_data + github_data + synthetic_data,
    }

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(combined, f, indent=2, ensure_ascii=False)

    print(f"Saved {combined['metadata']['total_examples']} examples to {output_path}")
    print(f"  - HuggingFace: {len(huggingface_data)}")
    print(f"  - GitHub: {len(github_data)}")
    print(f"  - Synthetic: {len(synthetic_data)}")


def main():
    """Main function to download and combine all datasets."""
    print("=" * 60)
    print("ResumeGPT NER Dataset Downloader")
    print("=" * 60)

    # Output path
    output_path = (
        PROJECT_ROOT
        / "backend"
        / "data"
        / "ner_datasets"
        / "raw"
        / "combined_dataset.json"
    )

    # Download datasets
    huggingface_data = download_huggingface_dataset()
    github_data = download_github_dataset()
    synthetic_data = generate_synthetic_data()

    # Save combined dataset
    if huggingface_data or github_data or synthetic_data:
        save_combined_dataset(
            huggingface_data, github_data, synthetic_data, str(output_path)
        )
        print("\n" + "=" * 60)
        print("DONE! Dataset downloaded and saved.")
        print("=" * 60)
        print(f"\nOutput: {output_path}")
        print("\nNext step: Run prepare_data.py to convert to spaCy format")
    else:
        print("\nERROR: No data downloaded. Check your internet connection.")


if __name__ == "__main__":
    main()
