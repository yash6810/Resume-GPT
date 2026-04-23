# ResumeGPT — AI Resume Analyzer & ATS Booster (Solo MVP)

## Run locally (quick)
1. cd backend
2. python -m venv .venv && source .venv/bin/activate
3. pip install -r requirements.txt
4. uvicorn app.main:app --reload --port 8000

## MVP Endpoints
- POST /parse -> parse uploaded resume
- POST /analyze -> analyze resume vs JD
- POST /rewrite -> rewrite a bullet with target keywords
- POST /export -> export DOCX

## Notes
- This is a personal project MVP. No account system. Data is ephemeral by default.
