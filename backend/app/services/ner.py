"""
Named Entity Recognition (NER) service for resume parsing.
Extracts skills, companies, dates, education, and other entities from resume text.

Supports:
1. Custom trained model (from Colab training)
2. Base spaCy model (en_core_web_sm)
3. Rule-based extraction (fallback)
"""

import spacy
from spacy.tokens import Doc
from typing import List, Dict, Any, Optional
import re
import json
import os


class ResumeNER:
    """NER service for extracting entities from resumes.

    Uses hybrid approach:
    1. Base spaCy model (en_core_web_sm) for PERSON, ORG, GPE
    2. Custom trained model for EMAIL, LINKEDIN, URL, etc.
    3. Regex patterns for PHONE, YEAR, GPA, etc.
    """

    def __init__(self):
        self.nlp_base = None  # spaCy base model for PERSON, ORG, GPE
        self.nlp_custom = None  # Custom model for EMAIL, LINKEDIN, etc.
        self.model_type = None
        # Path: backend/app/services -> backend -> project root -> model directory
        self.custom_model_path = os.path.join(
            os.path.dirname(__file__),
            "..",
            "..",
            "model_finetuned-20260331T075320Z-1-001",
            "model_finetuned",
            "resume_ner_finetuned",
        )
        self._load_models()

    def _load_models(self):
        """Load both base spaCy model and custom model."""
        # Load base spaCy model for PERSON, ORG, GPE detection
        try:
            self.nlp_base = spacy.load("en_core_web_sm")
            self.model_type = "hybrid"
            print("Loaded base spaCy model (en_core_web_sm)")
        except OSError:
            try:
                print("Downloading spaCy base model...")
                import subprocess

                subprocess.run(
                    ["python", "-m", "spacy", "download", "en_core_web_sm"],
                    capture_output=True,
                )
                self.nlp_base = spacy.load("en_core_web_sm")
                self.model_type = "hybrid"
                print("Downloaded and loaded base spaCy model")
            except Exception as e:
                print(f"Could not load base spaCy model: {e}")
                self.nlp_base = None

        # Load custom trained model for EMAIL, LINKEDIN, URL, etc.
        if os.path.exists(self.custom_model_path):
            try:
                for model_dir in ["model-best", "resume_ner_final", "."]:
                    model_path = os.path.join(self.custom_model_path, model_dir)
                    if os.path.exists(model_path) and os.path.isdir(model_path):
                        try:
                            self.nlp_custom = spacy.load(model_path)
                            print(f"Loaded custom NER model from {model_path}")
                            print(f"   Pipeline: {self.nlp_custom.pipe_names}")
                            return
                        except Exception as e:
                            print(f"   Failed to load {model_path}: {e}")
                            continue
            except Exception as e:
                print(f"Error loading custom model: {e}")

    def extract_entities(self, text: str) -> Dict[str, List[str]]:
        """
        Extract entities from resume text using hybrid approach.

        Uses:
        1. Base spaCy model for PERSON, ORG (COMPANY), GPE (LOCATION)
        2. Custom model for EMAIL, LINKEDIN, URL, etc.
        3. Regex patterns for PHONE, YEAR, GPA, etc.
        """
        entities = {}

        # Step 1: Use base spaCy model for PERSON, ORG, GPE
        if self.nlp_base:
            try:
                doc_base = self.nlp_base(text)
                label_map_base = {
                    "PERSON": "PERSON",
                    "PER": "PERSON",
                    "ORG": "COMPANY",
                    "GPE": "LOCATION",
                    "LOC": "LOCATION",
                    "DATE": "DATE",
                }
                for ent in doc_base.ents:
                    mapped = label_map_base.get(ent.label_, ent.label_)
                    if mapped not in entities:
                        entities[mapped] = []
                    entities[mapped].append(ent.text)
            except Exception as e:
                print(f"Error in base NER: {e}")

        # Step 2: Use custom model for EMAIL, LINKEDIN, URL, etc.
        if self.nlp_custom:
            try:
                doc_custom = self.nlp_custom(text)
                label_map_custom = {
                    "EMAIL": "EMAIL",
                    "PHONE": "PHONE",
                    "LINKEDIN": "LINKEDIN",
                    "URL": "URL",
                    "GITHUB": "GITHUB",
                    "YEAR": "YEAR",
                    "GPA": "GPA",
                    "DEGREE": "DEGREE",
                    "SKILL": "SKILL",
                    "COMPANY": "COMPANY",
                    "JOB_TITLE": "JOB_TITLE",
                    "SCHOOL": "SCHOOL",
                    "GRADUATION_YEAR": "GRADUATION_YEAR",
                    "CERTIFICATION": "CERTIFICATION",
                    "YEARS_EXPERIENCE": "YEARS_EXPERIENCE",
                }
                for ent in doc_custom.ents:
                    mapped = label_map_custom.get(ent.label_, ent.label_)
                    if mapped not in entities:
                        entities[mapped] = []
                    entities[mapped].append(ent.text)
            except Exception as e:
                print(f"Error in custom NER: {e}")

        # Step 3: Add regex pattern extraction (always works)
        pattern_entities = self._pattern_extraction(text)
        for key, values in pattern_entities.items():
            if key not in entities:
                entities[key] = []
            entities[key].extend(values)

        # Deduplicate all lists
        for key in entities:
            entities[key] = list(set(entities[key]))

        return entities

    def _pattern_extraction(self, text: str) -> Dict[str, List[str]]:
        """Extract entities using regex patterns."""
        patterns = {
            "EMAIL": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
            "PHONE": r"\b(?:\+?1[-.]?)?\(?[0-9]{3}\)?[-.]?[0-9]{3}[-.]?[0-9]{4}\b",
            "URL": r"https?://(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&/=]*)",
            "LINKEDIN": r"linkedin\.com/in/[a-zA-Z0-9-]+",
            "GITHUB": r"github\.com/[a-zA-Z0-9-]+",
            "YEAR": r"\b(?:19|20)\d{2}\b",
            "GPA": r"(?:GPA|gpa)[:\s]*(\d\.\d{1,2})",
            "DEGREE": r"\b(?:Bachelor|Master|PhD|B\.S\.|M\.S\.|B\.A\.|M\.A\.|M\.B\.A\.|Ph\.D\.|Associate|Diploma)\b[^\n,]*",
        }

        results = {}
        for entity_type, pattern in patterns.items():
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                # Handle tuple results from groups
                if matches and isinstance(matches[0], tuple):
                    results[entity_type] = [m[0] if m else "" for m in matches]
                else:
                    results[entity_type] = list(matches)

        return results

    def _fallback_extraction(self, text: str) -> Dict[str, List[str]]:
        """Fallback extraction when spaCy model is not available."""
        return self._pattern_extraction(text)

    def extract_skills(
        self, text: str, skills_list: Optional[List[str]] = None
    ) -> List[str]:
        """Extract skills from resume text using pattern matching."""
        if not skills_list:
            skills_path = os.path.join(
                os.path.dirname(__file__), "..", "..", "data", "skills.json"
            )
            if os.path.exists(skills_path):
                try:
                    with open(skills_path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        skills_list = []
                        for category_skills in data.values():
                            if isinstance(category_skills, list):
                                skills_list.extend(category_skills)
                except json.JSONDecodeError:
                    skills_list = []

        if not skills_list:
            return []

        found_skills = []
        text_lower = text.lower()

        for skill in skills_list:
            if not skill:
                continue
            escaped_skill = re.escape(skill.lower())
            pattern = r"\b" + escaped_skill + r"\b"
            if re.search(pattern, text_lower):
                found_skills.append(skill)

        return list(set(found_skills))

    def extract_sections(self, text: str) -> Dict[str, str]:
        """
        Extract resume sections from text.

        Returns:
            Dictionary with section names as keys and content as values
        """
        section_headers = [
            "experience",
            "education",
            "skills",
            "summary",
            "objective",
            "projects",
            "certifications",
            "awards",
            "publications",
            "work experience",
            "professional experience",
            "employment",
            "academic background",
            "qualifications",
            "achievements",
        ]

        sections = {}
        current_section = "header"
        current_content = []

        lines = text.split("\n")

        for line in lines:
            line_lower = line.strip().lower()

            # Check if this line is a section header
            is_header = False
            for header in section_headers:
                if header in line_lower and (
                    line_lower.startswith(header) or line.strip().isupper()
                ):
                    # Save previous section
                    if current_content:
                        sections[current_section] = "\n".join(current_content)
                    current_section = header
                    current_content = []
                    is_header = True
                    break

            if not is_header and line.strip():
                current_content.append(line.strip())

        # Save last section
        if current_content:
            sections[current_section] = "\n".join(current_content)

        return sections

    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the loaded model."""
        info = {
            "model_loaded": self.nlp_base is not None or self.nlp_custom is not None,
            "model_type": self.model_type,
            "custom_model_exists": os.path.exists(self.custom_model_path),
            "base_model_loaded": self.nlp_base is not None,
            "custom_model_loaded": self.nlp_custom is not None,
        }

        if self.nlp_base:
            info["base_pipeline"] = self.nlp_base.pipe_names
        if self.nlp_custom:
            info["custom_pipeline"] = self.nlp_custom.pipe_names
            if "ner" in self.nlp_custom.pipe_names:
                info["entity_labels"] = list(self.nlp_custom.pipe_labels.get("ner", []))

        return info


# Singleton instance
_ner_service = None


def get_ner_service() -> ResumeNER:
    """Get or create singleton NER service instance."""
    global _ner_service
    if _ner_service is None:
        _ner_service = ResumeNER()
    return _ner_service
