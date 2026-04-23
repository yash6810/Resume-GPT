# ResumeGPT — AI Resume Analyzer & ATS Booster

A comprehensive AI-powered resume analyzer with ATS simulation, resume builder, and job application tracking.

## Features

- **Resume Parsing** - Upload PDF/DOCX resumes, extract text and sections
- **ATS Scoring** - Keyword matching, role match, experience relevance, quality analysis
- **ATS Platform Simulation** - Simulate 6 different ATS systems:
  - LinkedIn (skills focus)
  - Indeed (basic text parsing)
  - Greenhouse (DEI/culture focus)
  - Glassdoor (company/salary focus)
  - Monster (standard ATS)
  - Lever (values/culture fit)
- **A/B Testing** - Compare resume versions, track callback outcomes
- **Cover Letter Generator** - AI-powered cover letters
- **Resume Builder** - Build and export resumes in 7 templates
- **Job Tracker** - Track job applications
- **Interview Prep** - Generate interview questions
- **Salary Insights** - Estimate salary ranges

## Quick Start

### 1. Start Backend
```bash
cd backend
python -m venv .venv
.venv\Scripts\activate  # Windows
# or: source .venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --port 8000
```

### 2. Open Frontend
Open `frontend/index.html` in your browser (http://localhost:8000/docs for API docs)

## API Endpoints

| Endpoint | Description |
|----------|-------------|
| POST /parse | Upload and parse resume (PDF/DOCX) |
| POST /analyze | Analyze resume against job description |
| POST /analyze/quick | Quick ATS score |
| POST /ats-simulator/{platform} | Platform-specific ATS analysis |
| GET /ats-simulator/platforms | List all platforms |
| POST /ats-simulator/analyze | Compare all platforms |
| POST /rewrite | Rewrite bullet points |
| POST /export | Export as DOCX |
| POST /cover-letter/generate | Generate cover letter |
| POST /ab-test/create | Create A/B test |
| PUT /ab-test/{id}/outcome | Record callback outcome |
| GET /ab-test/stats/overview | A/B test statistics |
| POST /job-tracker | Track job applications |
| POST /interview-prep | Generate interview questions |

## Frontend Features (index.html)

1. **Analyzer Tab** - Upload resume, paste JD, get ATS score
2. **Builder Tab** - Build resume with templates
3. **Resume Comparison** - Compare two resumes with platform selector
4. **A/B Test Analytics** - Track resume performance
5. **Cover Letter** - Generate cover letters
6. **Job Tracker** - Track applications
7. **NER** - Extract entities from resume

## Tech Stack

- **Backend**: FastAPI, SQLAlchemy, spaCy, sentence-transformers
- **Frontend**: HTML, CSS, JavaScript (no frameworks)
- **Database**: SQLite (easily swappable to PostgreSQL)

## Project Structure

```
resumegpt/
├── backend/
│   ├── app/
│   │   ├── api/           # API endpoints
│   │   ├── services/      # Business logic
│   │   ├── core/         # Database, embeddings
│   │   └── models/       # SQLAlchemy models
│   └── requirements.txt
├── frontend/
│   └── index.html        # Single-page frontend
├── data/
│   └── skills.json      # 500+ skills
├── docs/
└── README.md
```

## Environment Variables

Create `backend/.env`:
```
GROQ_API_KEY=your_key
GEMINI_API_KEY=your_key
HUGGINGFACE_API_TOKEN=your_token
```

## Notes

- User authentication available (JWT)
- Data is stored in SQLite by default
- For PostgreSQL, see comments in `backend/.env`