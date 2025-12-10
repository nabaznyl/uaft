import os
import sys
import subprocess
import shutil
from uaft.utils import Console, Colors

console = Console()

def run_command(cmd, shell=True, check=True, capture_output=False):
    try:
        result = subprocess.run(
            cmd, 
            shell=shell, 
            check=check, 
            capture_output=capture_output, 
            text=True
        )
        return result
    except subprocess.CalledProcessError as e:
        if not capture_output:
            console.print(f"[red]Error running command: {cmd}[/red]")
        raise e

def check_gh_cli():
    """Check if GitHub CLI is installed."""
    return shutil.which("gh") is not None

def init_repo():
    """Initialize a local git repository."""
    if os.path.exists(".git"):
        console.print("[yellow]Git repository already initialized.[/yellow]")
        return

    console.print("[bold]Initializing Git repository...[/bold]")
    run_command("git init")
    
    # Check for .gitignore, create if missing
    if not os.path.exists(".gitignore"):
        console.print("Creating default .gitignore...")
        with open(".gitignore", "w") as f:
            f.write("__pycache__/\n*.pyc\n.env\n.venv/\ndist/\nbuild/\n*.egg-info/\n")
    
    console.print("Adding files...")
    run_command("git add .")
    
    console.print("Committing...")
    try:
        run_command('git commit -m "Initial commit"')
        console.print("[green]✅ Repository initialized locally.[/green]")
    except subprocess.CalledProcessError:
        console.print("[yellow]Nothing to commit (directory might be empty).[/yellow]")

def create_remote(visibility="public"):
    """Create a remote repository using GitHub CLI."""
    if not check_gh_cli():
        console.print("[red]GitHub CLI (gh) is not installed.[/red]")
        console.print("Please install it to automate remote creation: https://cli.github.com/")
        return

    # Check if already has remote
    try:
        res = run_command("git remote get-url origin", check=False, capture_output=True)
        if res.returncode == 0:
            console.print(f"[yellow]Remote 'origin' already exists: {res.stdout.strip()}[/yellow]")
            return
    except Exception:
        pass

    console.print(f"[bold]Creating {visibility} repository on GitHub...[/bold]")
    
    # Get directory name as default repo name
    repo_name = os.path.basename(os.getcwd())
    
    cmd = f"gh repo create {repo_name} --{visibility} --source=. --remote=origin"
    
    try:
        run_command(cmd)
        console.print(f"[green]✅ Remote repository created and linked.[/green]")
        
        # Push
        console.print("Pushing to origin...")
        run_command("git push -u origin HEAD")
        console.print("[green]✅ Code pushed to GitHub.[/green]")
        
    except subprocess.CalledProcessError:
        console.print("[red]Failed to create remote repository.[/red]")

def run_repo(args):
    """
    Manage Git repository.
    Usage: uaft repo <init|create|push> [options]
    """
    if not args or "--help" in args:
        print("Usage: uaft repo <command> [options]")
        print("\nCommands:")
        print("  init          Initialize local git repository")
        print("  create        Create remote repository (requires gh CLI)")
        print("  push          Push changes to remote")
        print("\nOptions for 'create':")
        print("  --public      Create public repository (default)")
        print("  --private     Create private repository")
        sys.exit(0)

    command = args[0]
    
    if command == "init":
        init_repo()
        
    elif command == "create":
        visibility = "public"
        if "--private" in args:
            visibility = "private"
        
        # Ensure local repo exists
        if not os.path.exists(".git"):
            init_repo()
            
        create_remote(visibility)
        
    elif command == "push":
        console.print("[bold]Pushing changes...[/bold]")
        try:
            run_command("git push")
        except subprocess.CalledProcessError:
            # Try setting upstream
            try:
                run_command("git push -u origin HEAD")
            except subprocess.CalledProcessError:
                console.print("[red]Push failed. Check your remote configuration.[/red]")
                
    else:
        console.print(f"[red]Unknown command: {command}[/red]")
        sys.exit(1)
