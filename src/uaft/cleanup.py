import os
import shutil
import glob
from uaft.utils import Console, Colors
from uaft.config import load_config

console = Console()

DEFAULT_CLEANUP_TARGETS = [
    # Python
    "**/__pycache__",
    "**/*.pyc",
    "**/*.pyo",
    "**/*.pyd",
    "**/.pytest_cache",
    "**/.mypy_cache",
    "**/.benchmarks",
    "**/.coverage",
    "**/htmlcov",
    "**/*.egg-info",
    "**/dist",
    "**/build",
    # Logs
    "**/*.log",
    "**/logs",
    "**/.logs",
    # Temp
    "**/*.tmp",
    "**/*.temp",
    "**/tmp",
]


def run_cleanup(dry_run: bool = False):
    """Clean up project artifacts."""

    config = load_config()
    targets = config.get("cleanup", DEFAULT_CLEANUP_TARGETS)

    total_removed = 0

    # Group by category for display
    categories = {
        "Python Cache": [
            "__pycache__",
            ".pyc",
            ".pyo",
            ".pyd",
            ".pytest_cache",
            ".mypy_cache",
        ],
        "Build Artifacts": ["dist", "build", ".egg-info"],
        "Logs & Temp": [".log", "logs", ".tmp", ".temp", "tmp"],
        "Coverage": [".coverage", "htmlcov", ".benchmarks"],
    }

    results = {cat: 0 for cat in categories}
    results["Other"] = 0

    for pattern in targets:
        # Recursive glob
        matches = glob.glob(pattern, recursive=True)

        for path in matches:
            if os.path.isdir(path):
                # Check which category
                cat = "Other"
                for c, pats in categories.items():
                    if any(p in path for p in pats):
                        cat = c
                        break

                if not dry_run:
                    try:
                        shutil.rmtree(path)
                        results[cat] += 1
                        total_removed += 1
                    except OSError as e:
                        console.print(f"[red]Error removing {path}: {e}[/red]")
                else:
                    results[cat] += 1
                    total_removed += 1

            elif os.path.isfile(path):
                cat = "Other"
                for c, pats in categories.items():
                    if any(p in path for p in pats):
                        cat = c
                        break

                if not dry_run:
                    try:
                        os.remove(path)
                        results[cat] += 1
                        total_removed += 1
                    except OSError as e:
                        console.print(f"[red]Error removing {path}: {e}[/red]")
                else:
                    results[cat] += 1
                    total_removed += 1

    # Simple table output replacement
    print(f"\n{Colors.HEADER}UAFT Cleanup Summary{Colors.ENDC}")
    print(f"{'Category':<20} {'Status':<15} {'Count':<10}")
    print("-" * 45)

    for cat, count in results.items():
        status = "Would Remove" if dry_run else "Removed"
        if count > 0:
            print(f"{cat:<20} {status:<15} {count:<10}")

    if total_removed == 0:
        console.print(f"{Colors.YELLOW}Nothing to clean.{Colors.ENDC}")
    else:
        if dry_run:
            console.print(
                f"\n{Colors.YELLOW}Dry run complete. Found {total_removed} items to remove.{Colors.ENDC}"
            )
        else:
            console.print(
                f"\n[green]Cleanup complete. Removed {total_removed} items.[/green]"
            )
