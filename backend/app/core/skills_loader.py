import json
import os
from typing import List, Dict, Set
from pathlib import Path

# Global skills database
SKILLS_DB: Dict[str, List[str]] = {}
SKILLS_SET: Set[str] = set()


def load_skills(skills_file="data/skills.json") -> Dict[str, List[str]]:
    """Load skills from JSON file."""
    global SKILLS_DB, SKILLS_SET

    if skills_file is None:
        # Try multiple possible locations
        possible_paths = [
            "data/skills.json",
            os.path.join(os.path.dirname(__file__), "..", "..", "data", "skills.json"),
            os.path.join(os.path.dirname(__file__), "..", "data", "skills.json"),
        ]

        for path in possible_paths:
            if os.path.exists(path):
                skills_file = path
                break

        if not skills_file:
            skills_file = possible_paths[0]

    try:
        with open(skills_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Handle both dict and list formats
        if isinstance(data, dict):
            SKILLS_DB = data
        elif isinstance(data, list):
            # Convert list format to dict
            SKILLS_DB = {"skills": data}
        else:
            SKILLS_DB = {}

        # Create flat set for fast lookup
        SKILLS_SET = set()
        for category_skills in SKILLS_DB.values():
            if isinstance(category_skills, list):
                SKILLS_SET.update([skill.lower() for skill in category_skills])

        print(f"Loaded {len(SKILLS_SET)} skills from {len(SKILLS_DB)} categories")
        return SKILLS_DB
    except FileNotFoundError:
        print(f"Skills file not found: {skills_file}")
        SKILLS_DB = {}
        SKILLS_SET = set()
        return SKILLS_DB
    except json.JSONDecodeError as e:
        print(f"Error parsing skills JSON: {e}")
        SKILLS_DB = {}
        SKILLS_SET = set()
        return SKILLS_DB


def get_all_skills() -> Set[str]:
    """Get all skills as a flat set."""
    if not SKILLS_SET:
        load_skills()
    return SKILLS_SET


def get_skills_by_category(category: str) -> List[str]:
    """Get skills for a specific category."""
    if not SKILLS_DB:
        load_skills()
    return SKILLS_DB.get(category, [])


def get_skill_categories() -> List[str]:
    """Get list of all skill categories."""
    if not SKILLS_DB:
        load_skills()
    return list(SKILLS_DB.keys())


def find_skill_category(skill: str) -> str:
    """Find which category a skill belongs to."""
    if not SKILLS_DB:
        load_skills()

    skill_lower = skill.lower()
    for category, skills in SKILLS_DB.items():
        if skill_lower in [s.lower() for s in skills]:
            return category
    return "unknown"
