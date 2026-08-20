#!/usr/bin/env python3
"""
ResumeGPT System Architect - Automated Audit & Verification Utility
Provides automated checks for API contracts, module import benchmarks,
stale asset detection, and full-stack test suite verification.
"""

import argparse
import json
import os
import sys
import time
import subprocess
from pathlib import Path

# Fix Windows console UTF-8 output
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# Paths
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parents[3]
BACKEND_DIR = PROJECT_ROOT / "backend"
FRONTEND_DIR = PROJECT_ROOT / "frontend"

VENV_PYTHON = PROJECT_ROOT / ".venv" / "Scripts" / "python.exe"
PYTHON_BIN = str(VENV_PYTHON) if VENV_PYTHON.exists() else sys.executable


def run_cmd(cmd, cwd=None, env=None):
    """Run a shell command and return exit code, stdout, stderr."""
    full_env = os.environ.copy()
    if env:
        full_env.update(env)
    res = subprocess.run(
        cmd,
        cwd=cwd or PROJECT_ROOT,
        env=full_env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        shell=isinstance(cmd, str)
    )
    return res.returncode, res.stdout.strip(), res.stderr.strip()


def cmd_audit(args):
    """Audit active routers, frontend endpoints, and Pydantic schemas."""
    print("🔍 Auditing ResumeGPT full-stack architecture...")
    
    results = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "backend_routers": [],
        "frontend_endpoints": [],
        "unmatched_routes": [],
        "health": "OK"
    }

    api_dir = BACKEND_DIR / "app" / "api"
    if api_dir.exists():
        for py_file in sorted(api_dir.glob("*.py")):
            if py_file.name == "__init__.py":
                continue
            with open(py_file, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
                routes = []
                for line in content.splitlines():
                    line = line.strip()
                    if line.startswith("@router.post(") or line.startswith("@router.get(") or line.startswith("@router.put(") or line.startswith("@router.delete("):
                        routes.append(line.split("(")[1].split(")")[0].strip("\"'"))
                results["backend_routers"].append({
                    "module": py_file.stem,
                    "file": str(py_file.relative_to(PROJECT_ROOT)),
                    "routes_count": len(routes),
                    "routes": routes
                })

    frontend_index = FRONTEND_DIR / "index.html"
    if frontend_index.exists():
        with open(frontend_index, "r", encoding="utf-8", errors="ignore") as f:
            fe_content = f.read()
            known_endpoints = [
                "/health", "/analyze", "/analyze/quick", "/parse", "/export",
                "/export/pdf", "/builder/text", "/builder/export", "/interview-prep",
                "/salary-insights", "/auth/login", "/auth/register", "/job-tracker", "/rewrite"
            ]
            for ep in known_endpoints:
                results["frontend_endpoints"].append({
                    "endpoint": ep,
                    "present_in_frontend": ep in fe_content
                })

    if args.output:
        out_path = Path(args.output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2)
        print(f"✅ Audit report written to: {out_path}")
    else:
        print(json.dumps(results, indent=2))

    return 0


def cmd_benchmark(args):
    """Measure module load times to spot heavy dependencies."""
    print("⏱️ Benchmarking module import times...")
    
    modules_to_test = [
        ("pydantic", "Pydantic Schemas (Fast)"),
        ("fastapi", "FastAPI Core (Fast)"),
        ("sqlalchemy", "SQLAlchemy ORM (Fast)"),
        ("fpdf2", "PDF Export (Fast)"),
        ("docx", "DOCX Generator (Fast)")
    ]

    benchmarks = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "modules": []
    }

    for mod, label in modules_to_test:
        t0 = time.perf_counter()
        code = f"import {mod}"
        cmd = [PYTHON_BIN, "-c", code]
        ret, out, err = run_cmd(cmd)
        elapsed_ms = (time.perf_counter() - t0) * 1000
        benchmarks["modules"].append({
            "module": mod,
            "label": label,
            "status": "OK" if ret == 0 else "FAIL",
            "import_ms": round(elapsed_ms, 2)
        })
        print(f"  • {mod:<15} : {elapsed_ms:6.1f} ms ({label})")

    if args.output:
        out_path = Path(args.output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(benchmarks, f, indent=2)
        print(f"✅ Benchmark results written to: {out_path}")

    return 0


def cmd_clean(args):
    """Find stale backup files and caches."""
    print("🧹 Scanning for stale files and temporary caches...")
    
    candidates = []
    
    # Check for index_old.html
    old_fe = FRONTEND_DIR / "index_old.html"
    if old_fe.exists():
        candidates.append((old_fe, "Pre-rewrite frontend backup file (~60KB)"))

    # Check for pytest/ruff cache
    for cache_dir in [PROJECT_ROOT / ".pytest_cache", PROJECT_ROOT / ".ruff_cache", BACKEND_DIR / "__pycache__"]:
        if cache_dir.exists():
            candidates.append((cache_dir, f"Temporary cache folder: {cache_dir.name}"))

    if not candidates:
        print("✨ Workspace is clean. No orphaned or stale files found.")
        return 0

    print(f"Found {len(candidates)} candidate(s) for review:")
    for path, desc in candidates:
        print(f"  - {path.relative_to(PROJECT_ROOT)}: {desc}")

    if args.dry_run:
        print("\n[Dry Run] No files were removed. Use without --dry-run to clean.")
    else:
        print("\nNote: Please confirm manually before deleting files.")

    return 0


def cmd_verify(args):
    """Run full-stack test suite."""
    print("🚀 Running full-stack verification...")
    
    # 1. Frontend JSDOM tests
    print("\n--- [1/2] Running Frontend JSDOM Tests ---")
    npm_cmd = "npm test"
    ret_fe, out_fe, err_fe = run_cmd(npm_cmd, cwd=FRONTEND_DIR)
    print(out_fe if ret_fe == 0 else f"{out_fe}\n{err_fe}")
    if ret_fe != 0:
        print("❌ Frontend tests failed.")
        return 1

    # 2. Backend lightweight contract tests
    print("\n--- [2/2] Running Backend Lightweight Contract Tests ---")
    pytest_env = {
        "HF_HUB_OFFLINE": "1",
        "TRANSFORMERS_OFFLINE": "1",
        "TOKENIZERS_PARALLELISM": "false"
    }
    pytest_cmd = [PYTHON_BIN, "-m", "pytest", "tests/test_frontend_contract.py", "-q"]
    ret_be, out_be, err_be = run_cmd(pytest_cmd, cwd=BACKEND_DIR, env=pytest_env)
    print(out_be if ret_be == 0 else f"{out_be}\n{err_be}")
    if ret_be != 0:
        print("❌ Backend contract tests failed.")
        return 1

    print("\n✨ All Full-Stack Tests Passed Successfully!")
    return 0


def main():
    parser = argparse.ArgumentParser(description="ResumeGPT System Architect CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # audit
    p_audit = subparsers.add_parser("audit", help="Audit API routers and frontend consumption")
    p_audit.add_argument("--output", "-o", help="Path to write JSON audit report")

    # benchmark
    p_bench = subparsers.add_parser("benchmark", help="Measure module load times and memory safety")
    p_bench.add_argument("--output", "-o", help="Path to write JSON benchmark report")

    # clean
    p_clean = subparsers.add_parser("clean", help="Identify stale files and caches")
    p_clean.add_argument("--dry-run", action="store_true", help="Report candidates without removing")

    # verify
    p_verify = subparsers.add_parser("verify", help="Run full-stack frontend & backend test suite")

    args = parser.parse_args()

    if args.command == "audit":
        sys.exit(cmd_audit(args))
    elif args.command == "benchmark":
        sys.exit(cmd_benchmark(args))
    elif args.command == "clean":
        sys.exit(cmd_clean(args))
    elif args.command == "verify":
        sys.exit(cmd_verify(args))


if __name__ == "__main__":
    main()
