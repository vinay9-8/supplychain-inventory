from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    ROOT / "README.md",
    ROOT / "backend" / "app.py",
    ROOT / "backend" / "requirements.txt",
    ROOT / "frontend" / "package.json",
    ROOT / "docker-compose.yml",
    ROOT / ".github" / "workflows" / "ci.yml",
]


def run_command(command: list[str], cwd: Path) -> bool:
    print(f"\n> {' '.join(command)}  (cwd={cwd})")
    result = subprocess.run(command, cwd=str(cwd))
    if result.returncode != 0:
        print(f"Command failed with exit code {result.returncode}")
        return False
    return True


def main() -> int:
    print("Running release readiness checks...\n")

    missing = [str(path.relative_to(ROOT)) for path in REQUIRED_FILES if not path.exists()]
    if missing:
        print("Missing required files:")
        for item in missing:
            print(f" - {item}")
        return 1

    print("Required project files present.")

    venv_python = ROOT / ".venv" / "Scripts" / "python.exe"
    python_executable = str(venv_python) if venv_python.exists() else sys.executable
    npm_executable = "npm.cmd" if os.name == "nt" else "npm"

    if not run_command([python_executable, "-m", "pytest", "backend/tests", "-q"], ROOT):
        return 1

    if shutil.which(npm_executable) is None:
        print(f"npm executable '{npm_executable}' not found in PATH.")
        return 1

    if not run_command([npm_executable, "run", "build"], ROOT / "frontend"):
        return 1

    print("\nRelease validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
