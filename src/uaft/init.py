import os
import sys
import json

DEFAULT_CONFIG = {
    "version": 1.0,
    "project": "my-new-project",
    "fix": {
        "python": ["black .", "isort ."],
        "node": ["npm run lint:fix"],
        "bash": ["shfmt -w ."],
    },
    "cleanup": [
        "**/__pycache__",
        "**/*.pyc",
        "**/*.egg-info",
        "dist/",
        "build/",
        ".pytest_cache",
        ".coverage",
        "node_modules",
    ],
    "test": {
        "command": "pytest",
        "args": ["-v"],
        "description": "Run tests (defaults to pytest, falls back to unittest)"
    },
    "setup": {
        "description": "Setup development environment",
        "commands": [
            "echo 'Setting up environment...'",
            "# pip install -r requirements.txt",
            "# npm install",
        ],
    },
    "dev": {
        "description": "Install with dev dependencies",
        "commands": [
            "echo 'Installing dev dependencies...'",
            "# pip install -e .[dev]",
            "# npm install --include=dev",
        ],
    },
    "hooks": {
        "description": "Install pre-commit hooks",
        "commands": [
            "echo 'Installing hooks...'",
            "# pre-commit install",
        ],
    },
    "quick-start": {
        "description": "Run project demo/quick start",
        "commands": [
            "echo 'Running quick start...'",
            "# ./scripts/start.sh",
        ],
    },
    "check": {
        "description": "Run full quality check",
        "commands": [
            "echo 'Running quality checks...'",
            "uaft lint",
            "uaft test",
        ],
    },
    "doctor": {
        "description": "Diagnose environment setup",
        "commands": [
            "echo 'Checking environment...'",
            "# ./scripts/diagnose.sh",
        ],
    },
    "lint": {
        "description": "Lint code",
        "commands": [
            "echo 'Linting...'",
            "# flake8 .",
            "# npm run lint",
        ],
    },
    "ready": {
        "description": "Verify environment is ready",
        "commands": [
            "echo 'Verifying readiness...'",
            "# ./scripts/verify.sh",
        ],
    },
}


def run_init(args):
    """Initialize a new uaft project."""
    force = "--force" in args or "-f" in args

    if os.path.exists("uaft.json") and not force:
        print("Error: uaft.json already exists.")
        print("Use 'uaft init --force' to overwrite it.")
        sys.exit(1)

    with open("uaft.json", "w") as f:
        json.dump(DEFAULT_CONFIG, f, indent=2)

    print("✅ Created uaft.json")
    print("Edit it to configure your project tasks and tools.")
