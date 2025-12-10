import os
import time
import subprocess
import sys
from typing import List, Optional


class Watcher:
    def __init__(
        self, command: str, patterns: Optional[List[str]] = None, debounce: float = 1.0
    ):
        self.command = command
        self.patterns = patterns or [".py", ".sh", ".yaml", ".yml", ".md"]
        self.debounce = debounce
        self.last_run = 0.0
        self._mtimes = {}

    def _scan(self) -> bool:
        """Scan for changes. Returns True if changes detected."""
        changed = False
        current_mtimes = {}

        for root, _, files in os.walk("."):
            # Skip common ignore dirs
            if any(
                x in root
                for x in [
                    ".git",
                    "__pycache__",
                    ".venv",
                    "node_modules",
                    ".pytest_cache",
                ]
            ):
                continue

            for f in files:
                if any(f.endswith(p) for p in self.patterns):
                    path = os.path.join(root, f)
                    try:
                        mtime = os.path.getmtime(path)
                        current_mtimes[path] = mtime

                        if path not in self._mtimes:
                            self._mtimes[path] = mtime
                            # Initial scan doesn't trigger change unless we want it to
                        elif self._mtimes[path] != mtime:
                            changed = True
                            print(f"File changed: {path}")
                    except OSError:
                        pass

        self._mtimes = current_mtimes
        return changed

    def run(self):
        print(f"Watching for changes in {self.patterns}...")
        print(f"Command: {self.command}")

        # Initial run
        self._execute()

        try:
            while True:
                if self._scan():
                    now = time.time()
                    if now - self.last_run >= self.debounce:
                        self._execute()
                        self.last_run = now
                time.sleep(0.5)
        except KeyboardInterrupt:
            print("\nWatch stopped.")

    def _execute(self):
        print(f"\n--- Running: {self.command} ---")
        try:
            subprocess.run(self.command, shell=True)
        except Exception as e:
            print(f"Error executing command: {e}")
        print("--- Waiting for changes ---")
