# ResumeGPT - Project Memory

## Project Status: MVP Complete + Resume Builder + Multiple Templates + User Auth + History + Dark Mode + LLM Integration + Cover Letter Generator + PDF Export + Frontend Auth UI + Multi-LLM Support + NER Entity Extraction Complete + Real-time ATS Scoring + Streamlit Frontend + Chrome Extension + Industry Templates + Job Tracker + Interview Prep

## What Was Built
ResumeGPT is an AI Resume Analyzer & ATS Booster with a Resume Builder feature, multiple resume templates, user authentication with frontend UI, resume history tracking, dark mode, multi-LLM-powered bullet rewriting (Groq/Gemini/OpenAI/HuggingFace), cover letter generation, PDF export, custom NER entity extraction, real-time ATS scoring, a modern Streamlit frontend, a Chrome extension for scanning job boards, industry-specific templates with tailored keywords and suggestions for Tech, Finance, Healthcare, Marketing, Education, and Consulting, a Job Tracker for managing job applications with status tracking, follow-ups, and interview scheduling, and Interview Prep with AI-generated questions based on resume and job description.

## Folder Structure
```
resumegpt/
├── backend/
│   ├── app/
│   │   ├── main.py          # FastAPI app with all routers
│   │   ├── api/
│   │   │   ├── parse.py     # POST /parse - PDF/DOCX extraction
│   │   │   ├── analyze.py   # POST /analyze - ATS scoring
│   │   │   ├── rewrite.py   # POST /rewrite - Bullet rewrites
│   │   │   ├── export.py    # POST /export - DOCX export
│   │   │   ├── builder.py   # POST /builder/export, /builder/text, GET /builder/templates
│   │   │   ├── auth.py      # POST /auth/register, /auth/login, GET/PUT /auth/me
│   │   │   ├── history.py   # POST /history/save, GET /history/list, /history/{id}, DELETE, /history/stats/summary
│   │   │   └── cover_letter.py # POST /cover-letter/generate, /cover-letter/export
│   │   ├── core/
│   │   │   ├── skills_loader.py  # Loads skills.json
│   │   │   ├── embeddings.py     # sentence-transformers + FAISS
│   │   │   └── database.py       # SQLAlchemy models (User, ResumeHistory)
│   │   ├── services/
│   │   │   ├── parser.py    # PDF/DOCX text extraction
│   │   │   ├── scoring.py   # ATS score calculation
│   │   │   ├── templates.py # Resume template generators
│   │   │   ├── llm.py       # LLM integration (Groq/Gemini/OpenAI/HuggingFace) for rewrites
│   │   │   ├── cover_letter.py # Cover letter generation service
│   │   │   ├── pdf_export.py   # PDF export service
│   │   │   ├── ner.py       # NER entity extraction service (custom model)
│   │   │   └── train_ner.py # NER training script for Colab
│   │   └── models/
│   │       └── schemas.py   # Pydantic models
│   ├── models/
│   │   └── resume_ner/      # Trained NER model (17 entity types)
│   ├── tests/
│   │   └── test_main.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
├── frontend/
│   ├── index.html           # Single-page app with Analyzer + Builder + Template Selector
│   └── app.py               # Streamlit frontend with real-time ATS scoring
├── extension/
│   ├── manifest.json        # Chrome extension configuration (Manifest V3)
│   ├── popup/
│   │   ├── popup.html       # Extension popup UI
│   │   ├── popup.css        # Popup styling (dark theme)
│   │   └── popup.js         # Popup logic
│   ├── content/
│   │   ├── content.js       # Job description detection
│   │   └── content.css      # Floating badge styles
│   ├── background/
│   │   └── service-worker.js # Background tasks
│   └── icons/               # Extension icons (16, 48, 128px)
│       └── STITCH_DESIGN_BRIEF.md # UI design brief for Google Stitch
├── data/
│   ├── skills.json          # 500+ skills across 18 categories
│   └── demo/
│       └── jobs.json        # 3 sample job descriptions
├── docs/
│   └── README.md
├── README.md
└── .gitignore
```

## API Endpoints
- `GET /` - Welcome message with all endpoints listed
- `GET /health` - Health check
- `POST /parse` - Upload resume (PDF/DOCX) → text + sections
- `POST /analyze` - Resume text + JD → ATS score, missing skills, recommendations
- `POST /rewrite` - Bullet + keywords → 2 variants (ATS-optimized, human-friendly)
- `POST /export` - Resume text + changes → DOCX download
- `POST /export/pdf` - Resume text + changes → PDF download
- `GET /builder/templates` - List available resume templates
- `GET /builder/industry-templates` - List industry-specific templates
- `GET /builder/industry-templates/{id}` - Get specific industry template
- `GET /builder/industry-templates/{id}/keywords` - Get industry keywords
- `GET /builder/industry-templates/{id}/skills` - Get skills by category
- `GET /builder/industry-templates/{id}/bullets` - Get bullet templates
- `POST /builder/industry-templates/{id}/generate-summary` - Generate industry summary
- `POST /builder/text` - Form data → text preview
- `POST /builder/export` - Form data → DOCX download
- `POST /cover-letter/generate` - Generate cover letter from resume + JD
- `POST /cover-letter/export` - Export cover letter as DOCX
- `POST /ner/extract` - Extract entities from resume text using custom NER model
- `GET /ner/status` - Check NER model status
- `POST /auth/register` - Register new user (email, username, password)
- `POST /auth/login` - Login user → JWT access token
- `GET /auth/me` - Get current user profile (requires auth)
- `PUT /auth/me` - Update user profile (requires auth)
- `POST /history/save` - Save resume analysis to history (requires auth)
- `GET /history/list` - List all resume history for current user (requires auth)
- `GET /history/{history_id}` - Get specific resume history entry (requires auth)
- `DELETE /history/{history_id}` - Delete resume history entry (requires auth)
- `GET /history/stats/summary` - Get history statistics (total analyses, avg/highest/lowest scores)
- `POST /job-tracker` - Create new job application (requires auth)
- `GET /job-tracker` - List all job applications (requires auth)
- `GET /job-tracker/{job_id}` - Get specific job application (requires auth)
- `PUT /job-tracker/{job_id}` - Update job application (requires auth)
- `DELETE /job-tracker/{job_id}` - Delete job application (requires auth)
- `GET /job-tracker/stats/summary` - Get job tracker statistics (requires auth)
- `POST /interview-prep` - Generate interview questions based on resume and JD

## How To Run
```bash
cd D:\resumegpt\backend
D:\resumegpt\.venv\Scripts\activate          # Windows
python -m uvicorn app.main:app --reload --port 8000  # From backend dir
```
Then open `D:\resumegpt\frontend\index.html` in browser.

## Important: Server Must Be Running
**The backend server MUST be running for the frontend to work.** The frontend makes API calls to `http://localhost:8000`. If you see errors like "Failed to fetch" or preview/export not working, the server is not running.

To start the server:
```bash
cd D:\resumegpt\backend
D:\resumegpt\.venv\Scripts\activate
python -m uvicorn app.main:app --reload --port 8000
```

You should see: `INFO: Uvicorn running on http://127.0.0.1:8000`

## Important Fixes Made
- Changed relative imports (`from ...services`) to absolute imports (`from app.services`) in all API files
- Fixed JavaScript syntax error in frontend (`fileName.textContent:` → `fileName.textContent =`)
- Server must run from `backend` directory, not `app` directory

## Dependencies Installed
- fastapi, uvicorn, python-multipart, pdfminer.six, python-docx, fpdf2, pydantic
- sentence-transformers, torch, faiss-cpu (for embeddings/scoring)
- sqlalchemy, passlib[bcrypt], python-jose[cryptography], PyJWT, bcrypt (for authentication)
- python-dotenv (for loading .env file)

## LLM API Configuration
The app supports multiple LLM providers with automatic fallback:
1. **Groq** (Primary) - llama-3.1-8b-instant - Fastest, unlimited free tier
2. **Gemini** - gemini-2.5-flash, gemini-2.0-flash-lite, gemini-2.0-flash - Free tier with quota
3. **OpenAI** - gpt-3.5-turbo - Paid, high quality
4. **HuggingFace** - Mistral-7B - Free, slower
5. **Rule-based** - Always works as fallback

Configure in `.env` file:
```
GROQ_API_KEY=gsk_...
GEMINI_API_KEY=AIza...
OPENAI_API_KEY=sk-...
HUGGINGFACE_API_TOKEN=hf_...
```

## ATS Scoring Weights
- Keywords: 40 points
- Role Match: 30 points
- Experience Relevance: 20 points
- Quality: 10 points
- Total: 0-100

## Frontend Features
1. **Analyzer Tab**: Upload resume, paste JD, get ATS score, see matched/missing skills, rewrite bullets, export as DOCX or PDF
2. **Builder Tab**: Fill contact info, summary, skills, add multiple experiences/education, preview, export as DOCX
3. **Template Selector**: Choose from 7 resume templates (Modern, Classic, Creative, Minimal, Executive, Tech, Academic)
4. **Industry Templates**: Select industry (Tech, Finance, Healthcare, Marketing, Education, Consulting) to get tailored keywords, skills, and suggestions
5. **Dark Mode**: Toggle between light and dark themes
6. **Cover Letter Generator**: Generate personalized cover letters from resume + job description
7. **Authentication**: Login/Register modals with JWT-based auth
8. **Resume History**: View past analyses when logged in
9. **NER Entity Extraction**: Extract names, emails, phones, skills, companies, etc. from resume text
10. **Job Tracker**: Track job applications with status, follow-ups, interview dates, and statistics
11. **Interview Prep**: AI-generated interview questions with tips for technical, behavioral, situational, and company-specific questions

## Resume Templates
1. **Modern**: Clean design with colored header and bullet-style skills (primary: dark blue, secondary: bright blue)
2. **Classic**: Traditional centered header with horizontal lines (black and gray tones)
3. **Creative**: Bold design with icons and accent colors (purple and orange accents)
4. **Minimal**: Sparse, elegant layout with generous whitespace (teal accent on dark gray)
5. **Executive**: Professional corporate style with navy blue accents
6. **Tech**: Modern tech-focused design with cyan-green accents
7. **Academic**: Traditional academic CV style with dark red accents

## Next Phase Ideas
- ~~User accounts + resume history~~ ✓ DONE
- ~~LLM integration for better rewrites~~ ✓ DONE
- ~~Multiple resume templates~~ ✓ DONE
- ~~Dark Mode~~ ✓ DONE
- ~~Cover Letter Generator~~ ✓ DONE
- ~~Fine-tune NER on resume dataset~~ ✓ DONE (Phase 1 - 5,000 examples)
- ~~Real-time ATS scoring in builder~~ ✓ DONE
- ~~Chrome extension for job boards~~ ✓ DONE
- ~~Industry Templates (Tech, Finance, Healthcare, Marketing, Education, Consulting)~~ ✓ DONE
- ~~Job Tracker feature~~ ✓ DONE
- ~~Advanced ATS simulation for specific platforms (LinkedIn, Indeed, Greenhouse)~~ ✓ DONE
- ~~Recruiter feedback loop (A/B tests)~~ ✓ DONE
- PostgreSQL migration (for production)
- Add more platforms (Glassdoor, Monster, Lever)

## Missing Features
- ~~Advanced ATS simulation for specific platforms~~ ✓ DONE (LinkedIn, Indeed, Greenhouse)
- ~~A/B test outcome tracking~~ ✓ DONE
- Fine-tune NER with more examples (Phase 2 - remaining 13,922 examples)

## Improvements
- Better error handling
- Loading states for cover letter generation
- Resume comparison feature
- Email integration for sharing

---

## Market Research & Competitive Analysis (March 2026)

### Market Overview
- Market Size: $1.5B+ (2025)
- ATS Usage: 98% of Fortune 500 companies use ATS
- Resume Rejection Rate: 75% filtered by ATS before human sees them
- Key Competitors: Jobscan ($50/mo), Teal ($29/mo), Rezi ($29/mo), ResumeWorded ($49/mo)

### Competitive Comparison

| Feature | ResumeGPT | Jobscan | Teal | Rezi | ResumeLM (OSS) |
|---------|-----------|---------|------|------|-----------------|
| ATS Scoring | ✅ | ✅ | ✅ | ✅ | ✅ |
| AI Bullet Rewrites | ✅ | ✅ | ✅ | ✅ | ✅ |
| Cover Letter | ✅ | ❌ | ❌ | ❌ | ✅ |
| Resume Builder | ✅ | ✅ | ✅ | ✅ | ✅ |
| Multiple Templates | ✅ (7) | Limited | ✅ | ✅ (9) | Limited |
| Industry Templates | ✅ (6) | ❌ | ❌ | ❌ | ❌ |
| PDF Export | ✅ | ✅ | ✅ | ✅ | ✅ |
| User Auth | ✅ | ✅ | ✅ | ✅ | ✅ |
| History Tracking | ✅ | ✅ | ✅ | ❌ | ❌ |
| Dark Mode | ✅ | ❌ | ❌ | ❌ | ❌ |
| LLM Flexibility | ✅ (4 providers) | Closed | Closed | Closed | OpenAI only |
| Open Source | ✅ | ❌ | ❌ | ❌ | ✅ |
| Price | FREE | $50/mo | $29/mo | $29/mo | FREE |

### ResumeGPT Strengths
1. **Multi-LLM Support (Unique)** - Groq → Gemini → OpenAI → HuggingFace → Rule-based fallback
2. **Feature Completeness** - ATS Scoring + Bullet Rewrites + Cover Letters + Resume Builder + Industry Templates
3. **Free & Open Source** - Competitors charge $29-50/month
4. **Modern Tech Stack** - FastAPI, sentence-transformers, FAISS, Pydantic
5. **Privacy** - Self-hostable, user owns data

### ResumeGPT Weaknesses
1. **Chrome Extension Issues** - Job detection not working due to outdated selectors
2. **No Real-time Scoring** - Score only after upload, not as you type
3. **No Job Tracker** - Can't track applications like Teal
4. **No Mobile App** - Desktop only

### Recommended Next Phase (Priority Order)

**High Priority:**
1. ~~Chrome Extension - Scan resumes on LinkedIn/Indeed directly~~ ✓ DONE
2. Real-time Editor - Live ATS score as you type
3. ~~Industry Templates - Tech, Finance, Healthcare presets~~ ✓ DONE
4. ~~Resume Comparison - Compare before/after scores~~ ✓ DONE

**Medium Priority:**
5. ~~Job Tracker - Track applications like Teal~~ ✓ DONE
6. LinkedIn Integration - Import profile directly
7. ~~Interview Prep - AI-generated questions based on JD~~ ✓ DONE
8. Salary Insights - Based on resume skills

**Nice to Have:**
9. Mobile App - React Native or PWA
10. Team Features - Share with career coaches
11. A/B Testing - Track which resume version gets more callbacks

### Verdict
ResumeGPT is a solid MVP that competes with paid tools. It covers 80% of what Jobscan + Teal + Rezi offer combined, but for FREE. The main gaps are polish and distribution (marketing, Chrome Web Store listing). The project has potential to be a genuine free alternative to $30-50/month tools.

---

## NER Training Status (March 2026) - COMPLETE

### Training Complete ✅
- ✅ Dataset downloaded: 23,653 examples (22,843 HuggingFace + 310 GitHub + 500 synthetic)
- ✅ Data prepared: train.spacy (18,922), dev.spacy (2,365), test.spacy (2,366)
- ✅ Training scripts created (download_datasets.py, prepare_data.py, train_ner.ipynb)
- ✅ Colab notebook updated with memory optimization
- ✅ Training completed on Google Colab T4 GPU
- ✅ Model deployed to `backend/models/resume_ner/`
- ✅ API endpoint `/ner/extract` working

### Training Results
| Setting | Value |
|---------|-------|
| Model | spaCy blank (en) |
| Training examples | 5,000 (subset) |
| Batch size | 4 |
| Epochs | 30 |
| GPU | T4 (16GB VRAM) |
| Training time | ~30 min |
| Entity types | 17 |

### Entity Types Detected
PERSON, EMAIL, PHONE, LOCATION, SKILL, COMPANY, JOB_TITLE, DEGREE, SCHOOL, GRADUATION_YEAR, CERTIFICATION, YEARS_EXPERIENCE, LINKEDIN, URL, YEAR, GPA, GITHUB

### Current Model Performance
- ✅ EMAIL detection: Working
- ✅ LINKEDIN detection: Working
- ✅ PHONE detection: Working (regex)
- ✅ URL detection: Working (regex)
- ⚠️ Names, companies, skills: Needs fine-tuning (Phase 2)

### Training Phases
| Phase | Examples | Purpose | Status |
|-------|----------|---------|--------|
| Phase 1 | 5,000 | Initial training | ✅ COMPLETE |
| Phase 2 | +10,000 | Fine-tuning | Pending |
| Phase 3 | +remaining | Final polish | Pending |

**Total available**: 23,653 examples (18,922 train + 2,365 dev + 2,366 test)

### Issues Fixed
1. ✅ HuggingFace dataset format (chat format, not tokens/ner_tags)
2. ✅ GitHub dataset format (XML, not JSON)
3. ✅ Memory crash (OOM with 18,922 examples)
4. ✅ CuPy conflicts (cupy-cuda11x vs cupy-cuda12x)
5. ✅ GPU not being used (added spacy.prefer_gpu())
6. ✅ spaCy cfg file compatibility (renamed cfg.txt to cfg)
7. ✅ Emoji encoding issues in print statements

### Files
- `D:\resumegpt\notebooks\train_ner.ipynb` - Colab training notebook
- `D:\resumegpt\scripts\download_datasets.py` - Dataset download
- `D:\resumegpt\scripts\prepare_data.py` - Data preparation
- `D:\resumegpt\scripts\test_ner.py` - Model testing
- `D:\resumegpt\scripts\finetune_ner.py` - Fine-tuning script (Phase 2)
- `D:\resumegpt\NER_TRAINING_GUIDE.md` - Complete guide
- `D:\resumegpt\backend\models\resume_ner\` - Trained model

### API Usage
```bash
curl -X POST http://localhost:8000/ner/extract \
  -H "Content-Type: application/json" \
  -d '{"text": "John Smith, Software Engineer at Google. Email: john@gmail.com"}'
```

Response:
```json
{
  "entities": {
    "EMAIL": ["john@gmail.com"]
  },
  "skills": [],
  "sections": {...}
}
```

### Next Steps for NER
1. **Fine-tune with more examples** - Use remaining 13,922 examples
2. **Improve accuracy** - Train longer or with transformer model
3. **Add more entity types** - Certification, GPA, etc.
4. **Deploy to production** - Docker containerization

---

## Chrome Extension Issues (April 2026)

### Issue: Job Description Not Detected
**Problem**: The Chrome extension is not detecting jobs on job boards (LinkedIn, Indeed, etc.) and manual paste is also not working.

**Root Causes**:
1. **Outdated CSS Selectors** - Job boards frequently change their HTML structure. The selectors in `extension/content/content.js` (lines 89-140) are outdated:
   - LinkedIn: `.job-details-jobs-unified-top-card__job-title`, `.jobs-description__content`
   - Indeed: `.jobsearch-JobInfoHeader-title`, `.jobsearch-jobDescriptionText`
   - These selectors no longer match the current website layouts

2. **Manual Input Bug** - The "Paste Manual" toggle in `popup.js` (lines 179-187) may have event listener issues

3. **Content Script Injection** - Runs on all pages (`<all_urls>`) which may cause issues

### Planned Fix
**Approach**: Simplify the extension to rely on manual input instead of fragile auto-detection
- Remove dependency on CSS selectors that break frequently
- Improve manual job description input UX
- Add clipboard paste functionality
- Keep auto-detection as optional feature

### Files to Update
- `extension/content/content.js` - Update selectors or remove auto-detection
- `extension/popup/popup.js` - Fix manual input toggle
- `extension/popup/popup.html` - Improve manual input UI
- `extension/manifest.json` - Restrict content script to specific domains

### Status
- [ ] Update content.js selectors
- [ ] Fix manual input toggle
- [ ] Test on LinkedIn, Indeed, Glassdoor
- [ ] Add more robust detection with fallbacks
