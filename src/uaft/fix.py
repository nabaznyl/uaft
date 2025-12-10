import os
import subprocess
import sys
from uaft.config import load_config

DEFAULT_FIXERS = {
    "python": ["black . --quiet", "isort . --quiet"],
    "node": ["npm run lint:fix"],
    "bash": ["shfmt -w ."],
}


def run_command(cmd):
    try:
        print(f"  Running {cmd.split()[0]}...")
        subprocess.run(cmd, shell=True, check=False)
    except Exception as e:
        print(f"  Error running {cmd}: {e}")


def run_fix(args):
    """
    Auto-fix code quality issues.
    Usage: uaft fix
    """
    if "--help" in args:
        print("Usage: uaft fix")
        sys.exit(0)

    config = load_config()
    fix_config = config.get("fix", {})

    # If fix_config is a list, it's a direct command sequence (override all detection)
    if isinstance(fix_config, list):
        print("Running configured fix commands...")
        for cmd in fix_config:
            run_command(cmd)
        print("✅ Auto-fix complete")
        return

    # Otherwise, treat it as a dict of project types (merge with defaults)
    # We prioritize user config over defaults
    fixers = DEFAULT_FIXERS.copy()
    if isinstance(fix_config, dict):
        fixers.update(fix_config)

    print("Running code quality auto-fix...")
    ran_any = False

    # Detect Python
    has_python = (
        os.path.exists("pyproject.toml")
        or os.path.exists("requirements.txt")
        or os.path.exists("setup.py")
    )
    
    if not has_python:
        # Fallback: check for any .py files
        try:
            ret = subprocess.run(
                "find . -name '*.py' -not -path '*/.*' -not -path '*/venv/*' -print -quit | grep -q .",
                shell=True,
            )
            if ret.returncode == 0:
                has_python = True
        except Exception:
            pass

    if has_python:
        print("→ Detected Python project")
        if "python" in fixers:
            for cmd in fixers["python"]:
                run_command(cmd)
            ran_any = True

    # Detect Node.js
    if os.path.exists("package.json"):
        print("→ Detected Node.js project")
        if "node" in fixers:
            for cmd in fixers["node"]:
                run_command(cmd)
            ran_any = True

    # Detect Bash (simple check for .sh files)
    # We use 'find' to check if any sh files exist, to avoid running shfmt on empty
    has_bash = False
    try:
        # Quick check for any .sh file
        ret = subprocess.run(
            "find . -name '*.sh' -not -path '*/.*' -print -quit | grep -q .",
            shell=True,
        )
        if ret.returncode == 0:
            has_bash = True
    except Exception:
        pass

    if has_bash:
        print("→ Detected Bash scripts")
        if "bash" in fixers:
            for cmd in fixers["bash"]:
                run_command(cmd)
            ran_any = True

    if not ran_any:
        print("No supported project type detected or no fixers configured.")
    else:
        print("✅ Auto-fix complete")
