# ResumeGPT - Start Server Script
$ErrorActionPreference = "Continue"

Write-Host "Starting ResumeGPT server..." -ForegroundColor Cyan

# Change to backend directory
Set-Location $PSScriptRoot\backend

# Start uvicorn in background
$process = Start-Process -FilePath "python" -ArgumentList "-m", "uvicorn", "app.main:app", "--reload", "--port", "8000" -NoNewWindow -PassThru

# Wait for server to start
Start-Sleep -Seconds 8

# Check if server is running
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/health" -TimeoutSec 5 -UseBasicParsing
    if ($response.StatusCode -eq 200) {
        Write-Host "Server is running!" -ForegroundColor Green
        Write-Host "API available at: http://localhost:8000" -ForegroundColor Cyan
        Write-Host "API docs at: http://localhost:8000/docs" -ForegroundColor Cyan
    }
} catch {
    Write-Host "Server may not be ready yet..." -ForegroundColor Yellow
}

# Return the process ID
return $process.Id