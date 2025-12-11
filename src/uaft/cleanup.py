import os
import shutil
import glob
from uaft.utils import Console, Colors
from uaft.progress import TaskRunner
from uaft.config import load_config
import logging

logger = logging.getLogger(__name__)
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
    """Clean up project artifacts with progress tracking."""
    config = load_config()
    targets = config.get("cleanup", DEFAULT_CLEANUP_TARGETS)

    total_removed = 0
    categories = {
        "Python Cache": ["__pycache__", ".pyc", ".pyo", ".pyd", ".pytest_cache", ".mypy_cache"],
        "Build Artifacts": ["dist", "build", ".egg-info"],
        "Logs & Temp": [".log", "logs", ".tmp", ".temp", "tmp"],
        "Coverage": [".coverage", "htmlcov", ".benchmarks"],
    }
    results = {cat: 0 for cat in categories}
    results["Other"] = 0

    # Collect all items first
    items_to_remove = []
    for pattern in targets:
        matches = glob.glob(pattern, recursive=True)
        for path in matches:
            if os.path.isdir(path) or os.path.isfile(path):
                cat = "Other"
                for c, pats in categories.items():
                    if any(p in path for p in pats):
                        cat = c
                        break
                items_to_remove.append((path, cat))

    # Create task runner
    runner = TaskRunner(f"🧹 Cleanup {'(DRY-RUN)' if dry_run else ''}")
    
    def remove_items():
        """Remove collected items."""
        for idx, (path, category) in enumerate(items_to_remove, 1):
            try:
                if os.path.isdir(path):
                    if not dry_run:
                        shutil.rmtree(path)
                    results[category] += 1
                elif os.path.isfile(path):
                    if not dry_run:
                        os.remove(path)
                    results[category] += 1
            except OSError as e:
                logger.warning(f"Error removing {path}: {e}")
        
        return len(items_to_remove)

    if items_to_remove:
        runner.add_task(
            f"Remove {len(items_to_remove)} artifacts",
            remove_items
        )
        runner.run()
    else:
        print(f"{Colors.YELLOW}ℹ️  Nothing to clean.{Colors.ENDC}\n")
        return

    # Display summary
    print(f"\n{Colors.HEADER}📊 Cleanup Summary{Colors.ENDC}")
    print(f"{'Category':<20} {'Status':<20} {'Count':<10}")
    print("-" * 50)
    
    total = 0
    for cat, count in results.items():
        if count > 0:
            status = "Would Remove" if dry_run else "Removed"
            print(f"{cat:<20} {status:<20} {count:<10}")
            total += count

    if dry_run:
        print(f"\n{Colors.YELLOW}ℹ️  Dry run complete. Found {total} items to remove.{Colors.ENDC}\n")
    else:
        print(f"\n{Colors.GREEN}✅ Cleanup complete. Removed {total} items.{Colors.ENDC}\n")
