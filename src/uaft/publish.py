import os
import shutil
import subprocess
import sys
from uaft.utils import Console, Colors

console = Console()

def run_command(cmd, shell=True, check=True):
    try:
        subprocess.run(cmd, shell=shell, check=check)
    except subprocess.CalledProcessError as e:
        console.print(f"[red]Error running command: {cmd}[/red]")
        sys.exit(e.returncode)

def check_dependencies():
    """Check if build and twine are installed."""
    missing = []
    try:
        import build
    except ImportError:
        missing.append("build")
    
    try:
        import twine
    except ImportError:
        missing.append("twine")
        
    if missing:
        console.print(f"[yellow]Missing dependencies: {', '.join(missing)}[/yellow]")
        console.print("Installing them now...")
        run_command(f"{sys.executable} -m pip install {' '.join(missing)}")

def run_publish(args):
    """
    Build and publish the package to PyPI.
    Usage: uaft publish [--dry-run] [--test]
    """
    if "--help" in args:
        print("Usage: uaft publish [options]")
        print("\nOptions:")
        print("  --dry-run    Build but do not upload")
        print("  --test       Upload to TestPyPI instead of PyPI")
        sys.exit(0)

    dry_run = "--dry-run" in args
    use_test_pypi = "--test" in args

    console.print("[bold cyan]📦 UAFT Publisher[/bold cyan]")
    
    # 1. Check dependencies
    check_dependencies()

    # 2. Clean old artifacts
    console.print("\n[bold]Cleaning old builds...[/bold]")
    for pattern in ["dist", "build", "*.egg-info"]:
        if pattern == "*.egg-info":
            # Find and remove egg-info dirs
            for item in os.listdir("."):
                if item.endswith(".egg-info") and os.path.isdir(item):
                    shutil.rmtree(item)
                    console.print(f"  Removed {item}")
        elif os.path.exists(pattern):
            shutil.rmtree(pattern)
            console.print(f"  Removed {pattern}")

    # 3. Build
    console.print("\n[bold]Building package...[/bold]")
    run_command(f"{sys.executable} -m build")
    
    if dry_run:
        console.print("\n[green]✅ Build complete (Dry Run). Artifacts in dist/[/green]")
        return

    # 4. Upload
    console.print("\n[bold]🚀 Uploading to PyPI...[/bold]")
    
    repo_arg = "--repository testpypi" if use_test_pypi else ""
    
    # Interactive confirmation is handled by CLI wrapper usually, but let's be safe
    # Twine will ask for credentials if not in .pypirc
    
    try:
        cmd = f"{sys.executable} -m twine upload {repo_arg} dist/*"
        run_command(cmd)
        console.print("\n[bold green]✅ Successfully published![/bold green]")
    except Exception as e:
        console.print(f"\n[bold red]❌ Publish failed: {e}[/bold red]")
        sys.exit(1)
