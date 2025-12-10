import sys
import subprocess
import os
from typing import List
from uaft.utils import Console, Colors
from uaft.tracker import track_result
from uaft.config import load_config

console = Console()


def run_tests(args: List[str]):
    """Run tests with optional flags."""
    # Load config to determine base command
    config = load_config()
    test_config = config.get("test", {})

    # Default to pytest if not configured
    base_cmd = "pytest"
    base_args = []

    if isinstance(test_config, str):
        parts = test_config.split()
        base_cmd = parts[0]
        base_args = parts[1:]
    elif isinstance(test_config, dict):
        base_cmd = test_config.get("command", "pytest")
        base_args = test_config.get("args", [])

    cmd = [base_cmd] + base_args

    # Parse our flags and pass others to pytest
    if "--parallel" in args:
        cmd.append("-n")
        cmd.append("auto")
        args.remove("--parallel")

    if "--json" in args:
        # Extract value
        try:
            idx = args.index("--json")
            json_file = args[idx + 1]
            cmd.append(f"--json-report-file={json_file}")
            args.remove("--json")
            args.remove(json_file)
        except IndexError:
            console.print(f"{Colors.RED}Error: --json requires a filename{Colors.ENDC}")
            sys.exit(1)

    should_track = False
    if "--track" in args:
        should_track = True
        args.remove("--track")

    # Pass through remaining args (like test paths)
    cmd.extend(args)

    is_dry_run = False
    if "--dry-run" in args:
        is_dry_run = True
        if "--dry-run" in cmd:
            cmd.remove("--dry-run")

    console.print(f"{Colors.CYAN}Running tests:{Colors.ENDC} {' '.join(cmd)}")

    if is_dry_run:
        return

    if is_dry_run:
        return

    try:
        ret = subprocess.run(cmd).returncode
    except FileNotFoundError:
        # Fallback logic for pytest
        if base_cmd == "pytest":
            console.print(f"[yellow]Warning: 'pytest' not found. Falling back to built-in 'unittest'.[/yellow]")
            # Construct unittest command
            # We need to handle args carefully. unittest discover doesn't take -v the same way as pytest
            # but -v is supported.
            fallback_cmd = [sys.executable, "-m", "unittest", "discover"]
            
            # Add verbose if present in original args
            if "-v" in cmd or "--verbose" in cmd:
                fallback_cmd.append("-v")
                
            # Add start directory if provided in args (simple heuristic)
            # Filter out flags from args to find paths
            paths = [arg for arg in args if not arg.startswith("-")]
            if paths:
                # unittest discover takes -s start_dir
                fallback_cmd.extend(["-s", paths[0]])
            
            console.print(f"{Colors.CYAN}Running fallback:{Colors.ENDC} {' '.join(fallback_cmd)}")
            try:
                ret = subprocess.run(fallback_cmd).returncode
            except Exception as e:
                console.print(f"[red]Error running fallback tests: {e}[/red]")
                sys.exit(1)
        else:
            console.print(f"[red]Error: Command '{base_cmd}' not found. Is it installed?[/red]")
            sys.exit(1)
    except KeyboardInterrupt:
        console.print("\n[yellow]Tests interrupted.[/yellow]")
        sys.exit(130)

    if should_track:
        project_name = os.path.basename(os.getcwd())
        status = "pass" if ret == 0 else "fail"
        details = "Tests passed" if ret == 0 else "Tests failed"
        track_result(project_name, status, details)

    sys.exit(ret)
