import sys
import os
import json


# ANSI Colors
class Colors:
    HEADER = "\033[95m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


class Console:
    def print(self, text, style=None):
        # Simple replacement for rich.console.print
        # Supports basic [color] tags if we wanted, but for now just print
        # We can strip rich tags or map them

        # Map common rich tags to ANSI
        text = text.replace("[red]", Colors.RED).replace("[/red]", Colors.ENDC)
        text = text.replace("[green]", Colors.GREEN).replace("[/green]", Colors.ENDC)
        text = text.replace("[blue]", Colors.BLUE).replace("[/blue]", Colors.ENDC)
        text = text.replace("[cyan]", Colors.CYAN).replace("[/cyan]", Colors.ENDC)
        text = text.replace("[yellow]", Colors.YELLOW).replace("[/yellow]", Colors.ENDC)
        text = text.replace("[bold]", Colors.BOLD).replace("[/bold]", Colors.ENDC)

        print(text)


def load_json_config(path):
    if os.path.exists(path):
        try:
            with open(path, "r") as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            print(f"{Colors.RED}Error parsing {path}: {e}{Colors.ENDC}")
    return {}


def save_json_config(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
