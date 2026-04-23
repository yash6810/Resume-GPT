#!/usr/bin/env python
"""Quick server start script."""

import subprocess
import time
import sys
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)) + "/backend")

print("Starting ResumeGPT server...")
proc = subprocess.Popen(
    [sys.executable, "-m", "uvicorn", "app.main:app", "--port", "8000"],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
)

print("Waiting for server to start...")
time.sleep(10)

print("Server should be running at http://localhost:8000")
print("To stop: Ctrl+C")
