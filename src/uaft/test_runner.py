import sys
import subprocess
import os
from typing import List
from uaft.utils import Console, Colors
from uaft.progress import TaskRunner
from uaft.tracker import track_result
from uaft.config import load_config

console = Console()


def run_tests(args: List[str]):
    """Run tests with optional flags and progress tracking."""
    config = load_config()
    test_config = config.get("test", {})

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

    if "--parallel" in args:
        cmd.append("-n")
        cmd.append("auto")
        args.remove("--parallel")

    if "--json" in args:
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

    cmd.extend(args)

    is_dry_run = False
    if "--dry-run" in args:
        is_dry_run = True
        if "--dry-run" in cmd:
            cmd.remove("--dry-run")

    console.print(f"{Colors.CYAN}🧪 Testing Configuration:{Colors.ENDC}\n")
    print(f"  • Command: {' '.join(cmd)}")
    print(f"  • Mode: {'DRY-RUN' if is_dry_run else 'EXECUTE'}")
    print()

    if is_dry_run:
        print(f"{Colors.YELLOW}ℹ️  DRY-RUN: No tests executed{Colors.ENDC}\n")
        return

    # Create task runner for test execution
    runner = TaskRunner("Test Execution")
    
    def execute_tests():
        """Execute the test command."""
        try:
            ret = subprocess.run(cmd).returncode
            return ret
        except FileNotFoundError:
            if base_cmd == "pytest":
                console.print(f"[yellow]⚠ 'pytest' not found. Falling back to unittest.[/yellow]")
                fallback_cmd = [sys.executable, "-m", "unittest", "discover"]
                
                if "-v" in cmd or "--verbose" in cmd:
                    fallback_cmd.append("-v")
                
                paths = [arg for arg in args if not arg.startswith("-")]
                if paths:
                    fallback_cmd.extend(["-s", paths[0]])
                
                console.print(f"{Colors.CYAN}Running fallback:{Colors.ENDC} {' '.join(fallback_cmd)}")
                return subprocess.run(fallback_cmd).returncode
            else:
                raise RuntimeError(f"Command '{base_cmd}' not found")
        except KeyboardInterrupt:
            console.print("\n[yellow]Tests interrupted by user[/yellow]")
            sys.exit(130)

    runner.add_task("Execute tests", execute_tests)
    success = runner.run()

    if should_track:
        project_name = os.path.basename(os.getcwd())
        status = "pass" if success else "fail"
        details = "Tests executed successfully" if success else "Tests had failures"
        track_result(project_name, status, details)

    sys.exit(0 if success else 1)
