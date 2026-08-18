#!/usr/bin/env python
"""Quick server start script."""

import subprocess
import time
import sys
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)) + "/backend")

port = int(os.getenv("PORT", 8000))
print(f"Starting ResumeGPT server on http://localhost:{port}...")
try:
    subprocess.run([sys.executable, "-m", "uvicorn", "app.main:app", "--port", str(port), "--reload"])
except KeyboardInterrupt:
    print("\nServer stopped.")
