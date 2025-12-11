"""Progress bar utilities for UAFT commands with animated styling."""

import sys
import time
from typing import Optional, Callable, Any


class ProgressBar:
    """Animated progress bar similar to twine upload style."""
    
    def __init__(self, label: str, total: int = 100, width: int = 40):
        """
        Initialize progress bar.
        
        Args:
            label: Description of operation
            total: Total number of items/steps
            width: Width of progress bar
        """
        self.label = label
        self.total = total
        self.width = width
        self.current = 0
        self.start_time = None
    
    def start(self):
        """Start the progress bar."""
        self.start_time = time.time()
        self._render(0)
    
    def update(self, current: int, units: str = "items"):
        """
        Update progress.
        
        Args:
            current: Current progress value
            units: Unit label (items, files, bytes, etc)
        """
        self.current = min(current, self.total)
        self._render(current, units)
    
    def finish(self, message: str = "✅ Complete"):
        """Finish progress bar."""
        self.current = self.total
        elapsed = time.time() - self.start_time if self.start_time else 0
        sys.stdout.write(f"\r{message} • {elapsed:.2f}s\n")
        sys.stdout.flush()
    
    def _render(self, current: int, units: str = "items"):
        """Render progress bar to stdout."""
        if self.total == 0:
            pct = 100
        else:
            pct = int((current / self.total) * 100)
        
        filled = int((current / self.total) * self.width) if self.total > 0 else 0
        bar = "━" * filled + "─" * (self.width - filled)
        
        msg = f"{self.label} {current}/{self.total} {units}"
        progress = f"\r{msg}\n{pct}% ┃{bar}┃"
        
        sys.stdout.write(progress)
        sys.stdout.flush()


class TaskRunner:
    """Run tasks with progress tracking."""
    
    def __init__(self, task_name: str):
        self.task_name = task_name
        self.tasks = []
        self.failed = []
    
    def add_task(self, name: str, func: Callable, *args, **kwargs):
        """Add a task to run."""
        self.tasks.append((name, func, args, kwargs))
    
    def run(self, show_progress: bool = True) -> bool:
        """
        Run all tasks.
        
        Returns:
            True if all tasks succeeded, False if any failed
        """
        print(f"\n🔄 {self.task_name}")
        print("─" * 50)
        
        total = len(self.tasks)
        
        for idx, (name, func, args, kwargs) in enumerate(self.tasks, 1):
            status = f"[{idx}/{total}] {name}"
            print(f"\n{status}...", end=" ", flush=True)
            
            try:
                result = func(*args, **kwargs)
                print("✅ PASS")
            except Exception as e:
                print(f"❌ FAIL: {str(e)[:40]}")
                self.failed.append((name, str(e)))
        
        print("\n" + "─" * 50)
        if self.failed:
            print(f"❌ {len(self.failed)} task(s) failed:\n")
            for name, error in self.failed:
                print(f"  • {name}: {error[:60]}")
            return False
        else:
            print(f"✅ All {total} tasks completed successfully!\n")
            return True


class SpinnerStatus:
    """Display status with spinner animation."""
    
    FRAMES = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    
    def __init__(self, message: str):
        self.message = message
        self.frame = 0
        self.running = False
    
    def start(self):
        """Start spinner."""
        self.running = True
        self._show()
    
    def stop(self, final_message: str):
        """Stop spinner and show final message."""
        self.running = False
        sys.stdout.write(f"\r{final_message:<50}\n")
        sys.stdout.flush()
    
    def _show(self):
        """Display current frame."""
        if self.running:
            sys.stdout.write(f"\r{self.FRAMES[self.frame]} {self.message:<40}")
            sys.stdout.flush()
            self.frame = (self.frame + 1) % len(self.FRAMES)
            # In real implementation, would use threading for animation


def format_size(bytes_size: int) -> str:
    """Format bytes to human readable size."""
    for unit in ["B", "KB", "MB", "GB"]:
        if bytes_size < 1024:
            return f"{bytes_size:.1f} {unit}"
        bytes_size /= 1024
    return f"{bytes_size:.1f} TB"


def format_speed(bytes_count: int, seconds: float) -> str:
    """Format transfer speed."""
    if seconds == 0:
        return "∞ B/s"
    speed = bytes_count / seconds
    return f"{format_size(int(speed))}/s"

