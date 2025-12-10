import os
import sys
import subprocess
import stat

PLUGIN_DIR = os.path.expanduser("~/.config/uaft/plugins")


def ensure_plugin_dir():
    if not os.path.exists(PLUGIN_DIR):
        os.makedirs(PLUGIN_DIR)


def list_plugins():
    """List available plugins."""
    ensure_plugin_dir()
    plugins = []
    if os.path.exists(PLUGIN_DIR):
        for f in os.listdir(PLUGIN_DIR):
            path = os.path.join(PLUGIN_DIR, f)
            if os.path.isfile(path) and os.access(path, os.X_OK):
                plugins.append(f)
    return sorted(plugins)


def run_plugin(name, args):
    """Run a plugin."""
    ensure_plugin_dir()
    plugin_path = os.path.join(PLUGIN_DIR, name)

    if not os.path.exists(plugin_path):
        print(f"Error: Plugin '{name}' not found.")
        return False

    if not os.access(plugin_path, os.X_OK):
        print(f"Error: Plugin '{name}' is not executable.")
        return False

    try:
        # Pass arguments to the plugin
        cmd = [plugin_path] + args
        subprocess.run(cmd, check=False)
        return True
    except Exception as e:
        print(f"Error running plugin {name}: {e}")
        return False


def install_plugin(path):
    """Install a script as a plugin."""
    ensure_plugin_dir()
    if not os.path.exists(path):
        print(f"Error: File '{path}' not found.")
        return

    name = os.path.basename(path)
    dest = os.path.join(PLUGIN_DIR, name)

    try:
        # Copy and make executable
        with open(path, "rb") as src, open(dest, "wb") as dst:
            dst.write(src.read())

        st = os.stat(dest)
        os.chmod(dest, st.st_mode | stat.S_IEXEC)
        print(f"✅ Installed plugin '{name}'")
    except Exception as e:
        print(f"Error installing plugin: {e}")
