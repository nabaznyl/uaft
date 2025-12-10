#!/usr/bin/env python3
"""
UAFT CLI Entry Point
Implements the Universal Automation Framework Tool command line interface.
"""

import sys
import os
import subprocess
from typing import Dict, Any, Optional
from uaft.config import load_config
from uaft.watch import Watcher
from uaft.cleanup import run_cleanup
from uaft.test_runner import run_tests
from uaft.init import run_init
from uaft.plugin_manager import list_plugins, run_plugin, install_plugin
from uaft.publish import run_publish
from uaft.repo import run_repo


def confirm_action(action_desc: str, args: list) -> bool:
    """
    Ask for confirmation before proceeding.
    Returns True if confirmed, False otherwise.
    Removes -y/--yes from args if present.
    """
    skip_confirm = False
    if "--yes" in args:
        args.remove("--yes")
        skip_confirm = True
    if "-y" in args:
        args.remove("-y")
        skip_confirm = True

    if skip_confirm:
        return True

    try:
        response = input(f"Are you sure you want to {action_desc}? [y/N] ").strip().lower()
        if response == 'y':
            return True
        print("Operation cancelled.")
        return False
    except (KeyboardInterrupt, EOFError):
        print("\nOperation cancelled.")
        return False


def show_help():
    """Show usage and available tasks"""
    print("Usage: uaft <command> [options] [args]")
    print("       uaft <task> [args]")
    print("       uaft <plugin> [args]")

    print("\nCore Commands:")
    print("  init          Initialize a new uaft project (creates uaft.json)")
    print("  fix           Run configured code fixers (see uaft.json)")
    print("  cleanup       Clean configured artifacts (see uaft.json)")
    print("  test          Run tests (see uaft.json)")
    print("  watch         Watch for file changes and run a command")
    print("  publish       Build and publish to PyPI")
    print("  repo          Manage Git repository (init, create, push)")
    print("  plugin        Manage external plugins")
    print("  hooks         Manage git hooks")
    print("  help          Show this help message")

    print("\nOptions:")
    print("  --version     Show version")
    print(
        "  --help        Show help for a specific command (e.g., 'uaft cleanup --help')"
    )

    plugins = list_plugins()
    if plugins:
        print("\nInstalled Plugins:")
        for p in plugins:
            print(f"  {p}")

    config = load_config()
    if config:
        print("\nAvailable Tasks (from uaft.json):")
        reserved = ["version", "project"]

        max_len = 0
        tasks = []
        for key, value in config.items():
            if key not in reserved and isinstance(value, dict) and "commands" in value:
                tasks.append((key, value.get("description", "")))
                max_len = max(max_len, len(key))

        if max_len > 0:
            for name, desc in tasks:
                print(f"  {name.ljust(max_len + 2)} {desc}")
        else:
            print("  (No tasks found)")
    else:
        print("\n(No uaft.json found in current directory or ~/.config/uaft/uaft.json)")


def run_task(task_name: str):
    """Execute a named task"""
    config = load_config()
    if not config:
        print(
            "Error: uaft.yaml not found in current directory or ~/.config/uaft/uaft.yaml"
        )
        sys.exit(1)

    if task_name not in config:
        print(f'Error: Task "{task_name}" not found in uaft.yaml')
        sys.exit(1)

    task = config[task_name]
    print(f"Running task: {task_name}")
    if "description" in task:
        print(f'Description: {task["description"]}')

    commands = task.get("commands", [])
    for cmd in commands:
        print(f"> {cmd}")
        # Run command in shell
        try:
            ret = subprocess.run(cmd, shell=True).returncode
            if ret != 0:
                print(f"Command failed with exit code {ret}")
                sys.exit(ret)
        except KeyboardInterrupt:
            print("\nTask interrupted")
            sys.exit(130)


def main():
    """Main entry point"""
    args = sys.argv[1:]
    if len(args) < 1:
        show_help()
        sys.exit(1)

    command = args[0]

    if command in ["help", "--help", "-h"]:
        show_help()
        sys.exit(0)

    if command in ["version", "--version", "-v"]:
        print("UAFT v0.3.0")
        sys.exit(0)

    if command == "task":
        if len(args) < 2:
            print("Usage: uaft task <task_name>")
            sys.exit(1)
        task_name = args[1]
        run_task(task_name)

    elif command == "init":
        run_init(args[1:])

    elif command == "plugin":
        if len(args) < 2:
            print("Usage: uaft plugin <list|install> [args]")
            sys.exit(1)
        sub = args[1]
        if sub == "list":
            print("Installed plugins:")
            for p in list_plugins():
                print(f"  {p}")
        elif sub == "install":
            if len(args) < 3:
                print("Usage: uaft plugin install <path_to_script>")
                sys.exit(1)
            install_plugin(args[2])
        else:
            print(f"Unknown plugin command: {sub}")

    elif command == "watch":
        # Simple argument parsing for watch
        # uaft watch --cmd "make test" --patterns "*.py,*.sh"
        cmd_to_run = None
        patterns = None

        # Try to find --cmd
        try:
            if "--cmd" in args:
                idx = args.index("--cmd")
                cmd_to_run = args[idx + 1]
            elif len(args) > 1 and not args[1].startswith("-"):
                # Assume second arg is command if not flag
                cmd_to_run = args[1]

            if "--patterns" in args:
                idx = args.index("--patterns")
                pats = args[idx + 1]
                patterns = pats.split(",")
        except IndexError:
            print("Error: Missing argument value")
            sys.exit(1)

        if not cmd_to_run:
            print("Usage: uaft watch --cmd <command> [--patterns <ext1,ext2>]")
            sys.exit(1)

        watcher = Watcher(cmd_to_run, patterns)
        watcher.run()

    elif command == "hooks":
        from uaft.hooks import run_hooks_command

        run_hooks_command(args[1:])

    elif command == "track-test":
        from uaft.tracker import run_tracker

        run_tracker(args[1:])

    elif command == "fix":
        from uaft.fix import run_fix

        # Check for help first
        if "--help" in args or "-h" in args:
            run_fix(args[1:])
            return

        if not confirm_action("run code fixers", args):
            sys.exit(0)

        run_fix(args[1:])

    elif command == "cleanup":
        if "help" in args or "--help" in args:
            print("Usage: uaft cleanup [options]")
            print("\nOptions:")
            print("  --dry-run    Show what would be deleted without actually deleting")
            print("  --yes, -y    Skip confirmation prompt")
            sys.exit(0)

        if not confirm_action("clean up configured artifacts", args):
            sys.exit(0)

        dry_run = "--dry-run" in args
        run_cleanup(dry_run=dry_run)

    elif command == "test":
        if "help" in args or "--help" in args:
            print("Usage: uaft test [options] [test_args]")
            print("\nOptions:")
            print("  --track        Track test results")
            print("  --parallel     Run tests in parallel (if supported)")
            print("  --json <file>  Output results to JSON")
            print("  --yes, -y      Skip confirmation prompt")
            sys.exit(0)

        if not confirm_action("run tests", args):
            sys.exit(0)

        test_args = args[1:]
        run_tests(test_args)

    elif command == "publish":
        if "--help" in args or "-h" in args:
            run_publish(args[1:])
            return

        if not confirm_action("build and publish to PyPI", args):
            sys.exit(0)
        run_publish(args[1:])

    elif command == "repo":
        run_repo(args[1:])

    else:
        # Check if it's a direct task call (convenience)
        config = load_config()
        if config and command in config and command not in ["version", "project"]:
            run_task(command)
        # Check if it's a plugin
        elif command in list_plugins():
            run_plugin(command, args[1:])
        else:
            print(f"Unknown command: {command}")
            show_help()
            sys.exit(1)


if __name__ == "__main__":
    main()
