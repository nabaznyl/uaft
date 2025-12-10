import os
import sys
import json
import datetime
import subprocess


def track_result(project, status, details=""):
    """Log a test result to the tracking file."""
    tracking_dir = os.path.expanduser("~/.local/share/test-tracking")
    results_file = os.path.join(tracking_dir, "results.jsonl")

    if not os.path.exists(tracking_dir):
        os.makedirs(tracking_dir)

    timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    hostname = os.uname().nodename

    try:
        branch = (
            subprocess.check_output(
                ["git", "rev-parse", "--abbrev-ref", "HEAD"], stderr=subprocess.DEVNULL
            )
            .decode()
            .strip()
        )
    except subprocess.CalledProcessError:
        branch = "unknown"

    record = {
        "timestamp": timestamp,
        "project": project,
        "status": status,
        "details": details,
        "branch": branch,
        "host": hostname,
    }

    with open(results_file, "a") as f:
        f.write(json.dumps(record) + "\n")

    print(f"✅ Recorded: {project} {status} at {timestamp}")


def generate_report(results_file, days):
    """Generate a simple report from the results file."""
    if not os.path.exists(results_file):
        print("No tracking data found.")
        return

    print(f"Test Report (Last {days} days)")
    print("-" * 40)

    cutoff = datetime.datetime.utcnow() - datetime.timedelta(days=days)

    try:
        with open(results_file, "r") as f:
            for line in f:
                try:
                    record = json.loads(line)
                    ts = datetime.datetime.strptime(
                        record["timestamp"], "%Y-%m-%dT%H:%M:%SZ"
                    )
                    if ts >= cutoff:
                        status_icon = "✅" if record["status"] == "pass" else "❌"
                        print(
                            f"{status_icon} {record['timestamp']} [{record['project']}] {record['details']} ({record['branch']})"
                        )
                except (json.JSONDecodeError, ValueError):
                    continue
    except Exception as e:
        print(f"Error reading report: {e}")


def run_tracker(args):
    """
    Track test results.
    Usage: uaft track-test <project> <status> [details]
           uaft track-test --report [days]
    """
    if len(args) == 0 or args[0] == "--help":
        print("Usage: uaft track-test <project> <status> [details]")
        print("       uaft track-test --report [days]")
        sys.exit(0)

    if args[0] == "--report":
        tracking_dir = os.path.expanduser("~/.local/share/test-tracking")
        results_file = os.path.join(tracking_dir, "results.jsonl")
        days = int(args[1]) if len(args) > 1 else 7
        generate_report(results_file, days)
        return

    if len(args) < 2:
        print(
            "Error: Missing arguments. Usage: uaft track-test <project> <status> [details]"
        )
        return

    project = args[0]
    status = args[1]
    details = args[2] if len(args) > 2 else ""

    track_result(project, status, details)
