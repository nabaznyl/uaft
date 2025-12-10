# UAFT - Universal Automation Framework Tool

**The "Make" for the modern era.** A lightweight, configuration-driven, and extensible automation framework designed to standardize workflows across any project.

## 🚀 Features

- **Universal Configuration**: Define project-specific rules in `uaft.json`. No more hardcoded scripts.
- **Plugin Architecture**: Extend functionality with any script (Bash, Python, etc.) via `uaft plugin`.
- **Smart Defaults**: Built-in support for `fix` (formatting), `cleanup` (artifacts), and `test` (execution & tracking).
- **Zero Dependencies**: Pure Python standard library. No `pip install` heavy deps required.

## 📦 Installation

```bash
pip install uaft
```

UAFT has **zero dependencies**. It installs instantly and runs anywhere Python 3.8+ is available.

## ⚡ Quick Start

1.  **Initialize a new project**:
    ```bash
    cd my-project
    uaft init
    ```
    This creates a `uaft.json` file with default settings.

2.  **Run standard commands**:
    ```bash
    uaft fix        # Run configured formatters (e.g., black, isort, prettier)
    uaft cleanup    # Remove configured artifacts (e.g., __pycache__, node_modules)
    uaft test       # Run tests
    ```

## 🔌 Plugin System

UAFT is designed to be extensible. You can install external scripts as first-class commands.

```bash
# Install a plugin (can be a local file or URL in the future)
uaft plugin install ./scripts/my-custom-tool.sh

# List installed plugins
uaft plugin list

# Run the plugin
uaft my-custom-tool arg1 arg2
```

## ⚙️ Configuration (`uaft.json`)

Control everything via `uaft.json`.

```json
{
  "project": "my-awesome-project",
  "fix": [
    "black src tests",
    "isort src tests"
  ],
  "cleanup": [
    "**/*.pyc",
    "**/__pycache__",
    "dist/",
    "build/"
  ],
  "test": {
    "command": "pytest",
    "args": ["-v"]
  }
}
```

## 🛠️ Core Commands

| Command | Description |
| :--- | :--- |
| `uaft init` | Generate a `uaft.json` configuration file. |
| `uaft fix` | Run code formatters and fixers defined in config. |
| `uaft cleanup` | Clean up build artifacts and temporary files. |
| `uaft test` | Run the test suite. Use `--track` to log results. |
| `uaft plugin` | Manage external plugins (install, list). |
| `uaft hooks` | Manage git hooks. |

## 🤝 Contributing

Contributions are welcome! Please see `CONTRIBUTING.md` for details.
