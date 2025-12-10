import os
import stat
import sys


def get_template_content(template_name):
    """Read template content from the templates directory"""
    # Try to find the template relative to this file
    base_dir = os.path.dirname(os.path.abspath(__file__))
    template_path = os.path.join(base_dir, "templates", template_name)

    if os.path.exists(template_path):
        with open(template_path, "r") as f:
            return f.read()

    print(f"Error: Could not find template {template_name} at {template_path}")
    return None


def install_hooks():
    """Install git hooks into the current repository"""
    if not os.path.exists(".git"):
        print("Error: Not a git repository (no .git directory found)")
        sys.exit(1)

    hooks_dir = os.path.join(".git", "hooks")
    os.makedirs(hooks_dir, exist_ok=True)

    hooks = ["post-merge", "pre-push"]

    for hook_name in hooks:
        content = get_template_content(hook_name)
        if not content:
            continue

        hook_path = os.path.join(hooks_dir, hook_name)

        # Write hook content
        with open(hook_path, "w") as f:
            f.write(content)

        # Make executable
        st = os.stat(hook_path)
        os.chmod(hook_path, st.st_mode | stat.S_IEXEC)

        print(f"✅ Installed {hook_name} hook")


def run_hooks_command(args):
    """Entry point for hooks command"""
    if "--help" in args:
        print("Usage: uaft hooks install")
        sys.exit(0)

    if len(args) > 0 and args[0] == "install":
        install_hooks()
    else:
        print("Usage: uaft hooks install")
        sys.exit(1)
