# ResumeGPT - Combined Test Suite Execution Script
# Sets environment flags and runs both frontend jsdom and backend contract tests

$ErrorActionPreference = "Stop"

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host " Running ResumeGPT Test Suite" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan

# 1. Run Frontend Tests
Write-Host "`n[1/2] Running Frontend UI Tests (jsdom)..." -ForegroundColor Yellow
Push-Location frontend
try {
    node tests/run-tests.mjs
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Frontend tests failed!" -ForegroundColor Red
        exit 1
    }
} finally {
    Pop-Location
}

# 2. Run Backend Lightweight Contract Tests
Write-Host "`n[2/2] Running Backend Lightweight Contract Tests..." -ForegroundColor Yellow
$env:HF_HUB_OFFLINE = "1"
$env:TRANSFORMERS_OFFLINE = "1"
$env:TOKENIZERS_PARALLELISM = "false"

.\.venv\Scripts\python.exe -m pytest backend\tests\test_frontend_contract.py -q
if ($LASTEXITCODE -ne 0) {
    Write-Host "Backend contract tests failed!" -ForegroundColor Red
    exit 1
}

Write-Host "`n==========================================" -ForegroundColor Green
Write-Host " ALL TESTS PASSED SUCCESSFULLY!" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Green
exit 0
