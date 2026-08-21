#!/usr/bin/env python
"""Quick server start script that automatically uses the project virtual environment."""

import os
import sys
import subprocess

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.join(ROOT_DIR, "backend")

# Resolve virtual environment python binary
VENV_PYTHON_WIN = os.path.join(ROOT_DIR, ".venv", "Scripts", "python.exe")
VENV_PYTHON_UNIX = os.path.join(ROOT_DIR, ".venv", "bin", "python")

if os.path.isfile(VENV_PYTHON_WIN):
    PYTHON_BIN = VENV_PYTHON_WIN
elif os.path.isfile(VENV_PYTHON_UNIX):
    PYTHON_BIN = VENV_PYTHON_UNIX
else:
    PYTHON_BIN = sys.executable

os.chdir(BACKEND_DIR)

port = int(os.getenv("PORT", 8000))
print(f"Starting ResumeGPT server on http://localhost:{port}...")
print(f"Using Python runtime: {PYTHON_BIN}")

try:
    subprocess.run([PYTHON_BIN, "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", str(port), "--reload"])
except KeyboardInterrupt:
    print("\nServer stopped.")
