---
name: resumegpt-system-architect
description: >-
  Audits, streamlines, and elevates the ResumeGPT full-stack architecture.
  Use when analyzing system performance, pruning dead code/endpoints, optimizing
  memory footprint for 8GB RAM constraints, enforcing frontend-backend API contracts,
  or implementing 10x features like JD-targeted resume generation and real-time diffing.
---

# ResumeGPT System Architect

## Overview
`resumegpt-system-architect` is the master architectural intelligence skill for **ResumeGPT**. It provides systematic workflows to audit system health, reduce latency, isolate heavy ML dependencies, enforce Pydantic contracts, and design high-impact features (such as 1-click JD-targeted tailoring and closed-loop ATS scoring).

## Dependencies
- **managing-python-dependencies**: For managing virtual environment packages without global pollution.
- **accidental-data-loss-prevention**: Before pruning database files or deleting production assets.

## Quick Start
To audit the entire ResumeGPT codebase for dead endpoints, heavy imports, and contract alignment:
```powershell
uv run python .agents/skills/resumegpt-system-architect/scripts/audit_architecture.py audit --output scratch/arch_audit.json
```

To benchmark module load times and check memory safety on 8GB machines:
```powershell
uv run python .agents/skills/resumegpt-system-architect/scripts/audit_architecture.py benchmark --output scratch/benchmarks.json
```

---

## Architecture Principles & Guardrails

### 1. 8GB RAM Machine Protection (Strict)
- **Never import `app.main` in unit/contract tests.** `app.main` transitively imports PyTorch, spaCy, and Sentence-Transformers, which hangs local test runs.
- **Contract Tests**: Must test Pydantic schemas and lightweight routers in isolation (`tests/test_frontend_contract.py`).
- **Heavy Fullstack Tests**: Gated by `$env:FULLSTACK_TESTS="1"` in `conftest.py`.

### 2. Zero AI Slop & Clean Design System
- **Theme**: Deep Obsidian Slate (`#070b14`), Precision Cyan/Sky (`#0ea5e9`), Electric Emerald (`#10b981`).
- **Forbidden**: Fuzzy violet/purple gradients, generic glowing cards, unstyled high-contrast white textareas inside dark mode cards.
- **Typography**: `Plus Jakarta Sans` for UI, `JetBrains Mono` for ATS metrics, numbers, and code blocks.

### 3. API Contract Integrity
- All backend routes are mounted under root (`http://localhost:8000`), **never** `/api/...`.
- Analyzer expects: `{"resume_text": "...", "job_description": "..."}` &rarr; Returns `ats_score`, `subscores`, `skill_matches`, `missing_skills`, `recommendations`.
- Job Tracker requires `Authorization: Bearer <token>` with `company_name` and `position_title` payload keys.

---

## Utility Scripts (CLI-Based)

The skill includes a dedicated architectural audit script at `.agents/skills/resumegpt-system-architect/scripts/audit_architecture.py`.

### Subcommands:

1. **`audit`**: Inspects API routes, Pydantic schemas, and verifies which endpoints are actively consumed by the frontend.
   ```powershell
   python .agents/skills/resumegpt-system-architect/scripts/audit_architecture.py audit --output scratch/audit.json
   ```

2. **`benchmark`**: Measures import times for core and heavy dependencies to spot latency bottlenecks.
   ```powershell
   python .agents/skills/resumegpt-system-architect/scripts/audit_architecture.py benchmark --output scratch/benchmarks.json
   ```

3. **`clean`**: Identifies orphaned backups, stale build files, and temporary caches.
   ```powershell
   python .agents/skills/resumegpt-system-architect/scripts/audit_architecture.py clean --dry-run
   ```

4. **`verify`**: Runs both the frontend JSDOM test suite and the lightweight backend contract test suite in sequence.
   ```powershell
   python .agents/skills/resumegpt-system-architect/scripts/audit_architecture.py verify
   ```

---

## Systematic Workflows

### Workflow 1: Auditing & Pruning Legacy Bloat
1. Run `audit_architecture.py audit --output scratch/audit.json`.
2. Inspect `scratch/audit.json` for unused routers, obsolete endpoints, or mismatched request payload fields.
3. Remove or refactor obsolete endpoints in `backend/app/api/`.
4. Re-verify full test suite with `audit_architecture.py verify`.

### Workflow 2: Implementing 10x Features (e.g. JD-Tailored Builder)
1. Define the Pydantic schema in `backend/app/models/schemas.py` (`TailorResumeRequest`, `TailorResumeResponse`).
2. Implement the transformation logic in `backend/app/services/` with closed-loop ATS scoring (ensuring target score >= 90%).
3. Mount the lightweight router in `backend/app/api/`.
4. Update `frontend/index.html` with real-time UI components (visual diffs, loading indicators, toast notifications).
5. Add unit tests in `backend/tests/test_frontend_contract.py` and `frontend/tests/run-tests.mjs`.

### Workflow 3: Dual-Tier Test Verification
Whenever making changes across backend or frontend:
1. Run JSDOM frontend tests: `cd frontend && npm test`.
2. Run lightweight backend contract tests:
   ```powershell
   $env:HF_HUB_OFFLINE="1"; $env:TRANSFORMERS_OFFLINE="1"; $env:TOKENIZERS_PARALLELISM="false"
   cd backend && ..\.venv\Scripts\python.exe -m pytest tests/test_frontend_contract.py -q
   ```
3. Update [memory.md](file:///d:/resumegpt/memory.md) with test results and architectural state.

---

## Common Pitfalls & Mistakes

- ❌ **Accidentally importing `app.main` in test files**: Causes PyTorch and spaCy to load synchronously, hanging machines with <= 8GB RAM.
- ❌ **Adding `/api` prefix to routes**: Frontend contracts expect root paths (`/analyze`, `/export`, `/builder/text`).
- ❌ **Breaking dark theme immersion**: Placing raw unstyled `bg-white` inside dark modals. All modals must use `#111827` / `#0b1120` with white/10 borders.
- ❌ **Forgetting `memory.md` synchronization**: Always record state changes in `memory.md` after architecture modifications.
