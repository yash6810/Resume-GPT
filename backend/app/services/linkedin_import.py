import re
from typing import Dict, List, Optional


def parse_linkedin_profile(text: str) -> Dict:
    """Parse LinkedIn profile text and extract structured data."""
    result = {
        "contact": {
            "name": "",
            "email": "",
            "phone": "",
            "location": "",
            "linkedin": "",
            "website": "",
        },
        "summary": "",
        "skills": [],
        "experience": [],
        "education": [],
        "certifications": [],
    }

    lines = text.split("\n")
    lines = [line.strip() for line in lines if line.strip()]

    if not lines:
        return result

    # Extract name (usually first line)
    result["contact"]["name"] = lines[0]

    # Extract contact info using regex
    text_lower = text.lower()

    # Email
    email_match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)
    if email_match:
        result["contact"]["email"] = email_match.group()

    # Phone
    phone_match = re.search(
        r"[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}", text
    )
    if phone_match:
        result["contact"]["phone"] = phone_match.group()

    # LinkedIn URL
    linkedin_match = re.search(
        r"(?:linkedin\.com/in/|linkedin\.com/pub/)[a-zA-Z0-9-]+", text
    )
    if linkedin_match:
        result["contact"]["linkedin"] = "https://" + linkedin_match.group()

    # Location (look for common patterns)
    location_patterns = [
        r"(?:Location|Address|Based in)[:\s]*([^\n]+)",
        r"([A-Z][a-z]+,\s*[A-Z]{2}(?:\s*\d{5})?)",
        r"([A-Z][a-z]+\s*(?:Area|Region|District))",
    ]
    for pattern in location_patterns:
        location_match = re.search(pattern, text)
        if location_match:
            result["contact"]["location"] = location_match.group(1).strip()
            break

    # Extract sections
    current_section = None
    section_content = []

    section_headers = {
        "summary": ["summary", "about", "profile", "overview"],
        "experience": [
            "experience",
            "work experience",
            "employment",
            "professional experience",
        ],
        "education": ["education", "academic", "qualifications"],
        "skills": ["skills", "expertise", "competencies"],
        "certifications": ["certifications", "certificates", "licenses"],
    }

    for line in lines:
        line_lower = line.lower().strip()

        # Check if this line is a section header
        found_section = None
        for section, keywords in section_headers.items():
            if any(keyword in line_lower for keyword in keywords):
                if len(line) < 50:  # Section headers are usually short
                    found_section = section
                    break

        if found_section:
            # Process previous section
            if current_section and section_content:
                _process_section(current_section, section_content, result)

            current_section = found_section
            section_content = []
        else:
            if current_section:
                section_content.append(line)

    # Process last section
    if current_section and section_content:
        _process_section(current_section, section_content, result)

    return result


def _process_section(section: str, content: List[str], result: Dict):
    """Process a section's content and add to result."""
    if section == "summary":
        result["summary"] = " ".join(content)

    elif section == "skills":
        # Skills are usually comma-separated or one per line
        for line in content:
            if "," in line:
                skills = [s.strip() for s in line.split(",") if s.strip()]
                result["skills"].extend(skills)
            elif line and len(line) > 1 and len(line) < 50:
                result["skills"].append(line)

    elif section == "experience":
        current_exp = None
        for line in content:
            # Check for date patterns (new experience entry)
            date_match = re.search(
                r"(\d{4})\s*[-–]\s*(\d{4}|Present|Current|Now)", line, re.IGNORECASE
            )

            if date_match or (
                len(line) < 100
                and ("at " in line.lower() or "|" in line or "·" in line)
            ):
                # Save previous experience
                if current_exp:
                    result["experience"].append(current_exp)

                # Start new experience
                current_exp = {
                    "title": "",
                    "company": "",
                    "location": "",
                    "start_date": "",
                    "end_date": "",
                    "bullets": [],
                }

                if date_match:
                    current_exp["start_date"] = date_match.group(1)
                    current_exp["end_date"] = date_match.group(2)

                    # Extract title and company from the line
                    parts = line.split("|")
                    if len(parts) >= 2:
                        current_exp["title"] = parts[0].strip()
                        current_exp["company"] = parts[1].strip()
                    else:
                        # Try other separators
                        for sep in [" at ", " · ", " - "]:
                            if sep in line.lower():
                                parts = line.split(sep, 1)
                                current_exp["title"] = parts[0].strip()
                                current_exp["company"] = parts[1].strip()
                                break
                        if not current_exp["title"]:
                            current_exp["title"] = line
            else:
                # This is likely a bullet point
                if current_exp and line.startswith(("•", "-", "·", "*")):
                    bullet = line.lstrip("•-*· ").strip()
                    if bullet:
                        current_exp["bullets"].append(bullet)
                elif current_exp and not current_exp["title"]:
                    current_exp["title"] = line

        # Add last experience
        if current_exp:
            result["experience"].append(current_exp)

    elif section == "education":
        current_edu = None
        for line in content:
            # Check for degree patterns
            degree_keywords = [
                "bachelor",
                "master",
                "phd",
                "mba",
                "associate",
                "diploma",
                "certificate",
                "bs",
                "ms",
                "ba",
                "ma",
            ]
            if any(kw in line.lower() for kw in degree_keywords) or re.search(
                r"\d{4}", line
            ):
                if current_edu:
                    result["education"].append(current_edu)

                current_edu = {
                    "degree": "",
                    "school": "",
                    "location": "",
                    "graduation_date": "",
                    "gpa": None,
                }

                # Extract year
                year_match = re.search(r"\d{4}", line)
                if year_match:
                    current_edu["graduation_date"] = year_match.group()

                # Extract GPA
                gpa_match = re.search(r"GPA[:\s]*(\d+\.?\d*)", line, re.IGNORECASE)
                if gpa_match:
                    current_edu["gpa"] = gpa_match.group(1)

                # Degree and school
                parts = line.split("|")
                if len(parts) >= 2:
                    current_edu["degree"] = parts[0].strip()
                    current_edu["school"] = parts[1].strip()
                else:
                    current_edu["degree"] = line
            elif current_edu and not current_edu["school"]:
                current_edu["school"] = line

        if current_edu:
            result["education"].append(current_edu)

    elif section == "certifications":
        for line in content:
            line = line.lstrip("•-*· ").strip()
            if line and len(line) > 3:
                result["certifications"].append(line)


def format_linkedin_import(data: Dict) -> str:
    """Format parsed LinkedIn data for display."""
    lines = []

    if data["contact"]["name"]:
        lines.append(f"Name: {data['contact']['name']}")
    if data["contact"]["email"]:
        lines.append(f"Email: {data['contact']['email']}")
    if data["contact"]["phone"]:
        lines.append(f"Phone: {data['contact']['phone']}")
    if data["contact"]["location"]:
        lines.append(f"Location: {data['contact']['location']}")

    if data["summary"]:
        lines.append(f"\nSummary: {data['summary']}")

    if data["skills"]:
        lines.append(f"\nSkills: {', '.join(data['skills'])}")

    if data["experience"]:
        lines.append("\nExperience:")
        for exp in data["experience"]:
            lines.append(
                f"  - {exp['title']} at {exp['company']} ({exp['start_date']} - {exp['end_date']})"
            )
            for bullet in exp["bullets"]:
                lines.append(f"    • {bullet}")

    if data["education"]:
        lines.append("\nEducation:")
        for edu in data["education"]:
            lines.append(
                f"  - {edu['degree']} from {edu['school']} ({edu['graduation_date']})"
            )

    if data["certifications"]:
        lines.append("\nCertifications:")
        for cert in data["certifications"]:
            lines.append(f"  - {cert}")

    return "\n".join(lines)
