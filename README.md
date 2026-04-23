# ResumeGPT — AI Resume Analyzer & ATS Booster

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python" alt="Python">
  <img src="https://img.shields.io/badge/FastAPI-0.109+-009688?style=for-the-badge&logo=fastapi" alt="FastAPI">
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License">
  <img src="https://img.shields.io/badge/Status-Active-purple?style=for-the-badge" alt="Status">
</p>

**ResumeGPT** is an AI-powered resume analyzer and ATS booster built with FastAPI, spaCy, and sentence-transformers. A free & open source alternative to Jobscan ($50/mo), Teal ($29/mo), and Rezi ($29/mo).

## ✨ Features

| Feature | Description |
|---------|-------------|
| **Resume Parsing** | Upload PDF/DOCX resumes, extract text and sections |
| **ATS Scoring** | Keyword matching, role match, experience relevance, quality analysis |
| **6 ATS Platforms** | LinkedIn, Indeed, Greenhouse, Glassdoor, Monster, Lever |
| **A/B Testing** | Compare resume versions with callback tracking |
| **AI Cover Letter Generator** | Generate tailored cover letters (Groq/Gemini/OpenAI) |
| **Resume Builder** | Build resumes in 7 professional templates |
| **Job Application Tracker** | Track applications with status updates |
| **Interview Prep Generator** | Generate mock interview questions |
| **Salary Insights** | Estimate salary ranges |

## 🚀 Quick Start

### Backend
```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --port 8000
```

### Frontend
Open `frontend/index.html` in browser.

## 📡 API Endpoints

- `POST /parse` - Parse resume
- `POST /analyze` - ATS scoring
- `POST /ats-simulator/{platform}` - Platform-specific analysis
- `POST /rewrite` - Bullet rewrites
- `POST /ab-test/create` - A/B testing
- `POST /job-tracker` - Job tracking
- `POST /cover-letter/generate` - Cover letters

## 🛠️ Tech Stack

- **Backend**: FastAPI, SQLAlchemy, spaCy, sentence-transformers
- **Frontend**: HTML/CSS/JS
- **Database**: SQLite (PostgreSQL-ready)
- **LLM**: Groq, Gemini, OpenAI, HuggingFace

## 📄 License

MIT License

## ⭐ Star this repo if it helps!

---
Built with ❤️ using FastAPI, spaCy, and sentence-transformers