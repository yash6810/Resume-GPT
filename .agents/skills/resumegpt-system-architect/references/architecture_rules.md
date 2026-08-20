# ResumeGPT Architecture Reference & Rules

## 1. Machine Constraints (8GB RAM Protection)
- **Local Isolation Rule**: Unit and lightweight contract tests (`backend/tests/test_frontend_contract.py`) must never import `app.main` or any heavy modules (`torch`, `spacy`, `sentence_transformers`).
- **Cold Start Minimization**: Heavy ML pipelines are loaded lazily or called only on `/analyze` and `/ats-simulator` endpoints.
- **Environment Flags for Pytest**:
  ```powershell
  $env:HF_HUB_OFFLINE="1"
  $env:TRANSFORMERS_OFFLINE="1"
  $env:TOKENIZERS_PARALLELISM="false"
  ```

---

## 2. API Contract Mapping

| Endpoint | Method | Request Payload | Response Shape |
| :--- | :---: | :--- | :--- |
| `/health` | GET | None | `{"status": "healthy", "service": "resumegpt"}` |
| `/analyze` | POST | `{"resume_text": str, "job_description": str}` | `{ats_score, subscores, skill_matches, missing_skills, recommendations}` |
| `/parse` | POST | FormData (`resume`: PDF/DOCX) | `{"text": str, "sections": dict}` |
| `/export` | POST | `{"resume_text": str, "applied_changes": []}` | DOCX binary stream (`application/vnd...`) |
| `/export/pdf` | POST | `{"resume_text": str, "applied_changes": []}` | PDF binary stream (`application/pdf`) |
| `/builder/text`| POST | `ResumeBuilderRequest` | `{"text": str, "template": str}` |
| `/builder/export`| POST | `ResumeBuilderRequest` | DOCX stream (`resume_template.docx`) |
| `/interview-prep`| POST | `{"resume_text": str, "job_description": str, ...}` | `{"technical": [], "behavioral": [], ...}` |
| `/salary-insights`| POST | `{"job_title": str, "skills": [], ...}` | `{"min_salary", "max_salary", "median_salary", ...}` |
| `/job-tracker` | POST | `{"company_name": str, "position_title": str, ...}` | `JobApplicationResponse` (requires Bearer token) |

---

## 3. UI Design System Rules
- **No AI Slop**: Absolutely no fuzzy purple gradients, glowing borders, or unformatted white cards.
- **Primary Palette**: Obsidian Base (`#070b14`), Sky/Cyan (`#0ea5e9`), Mint/Emerald (`#10b981`), Amber (`#f59e0b`), Rose (`#f43f5e`).
- **Interactive Feedback**: All async actions must have loading spinners (`setLoading()`), error toasts (`showToast()`), and clear field validation indicators (`field-error`).
