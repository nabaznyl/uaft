# UAFT Release Notes

All versions and changes are documented here.

---

# UAFT v0.2.1 Release Notes

**Date:** December 10, 2025
**Focus:** Automation & Governance

## 🚀 New Features

### PyPI Automation (`uaft publish`)
- **One-Command Release**: Build and upload to PyPI with a single command.
- **Safety First**: Includes `--dry-run` to verify builds without uploading.
- **TestPyPI Support**: Use `--test` to upload to TestPyPI for verification.
- **Auto-Cleanup**: Automatically cleans old build artifacts (`dist/`, `build/`, `*.egg-info`) before building.

### Git & GitHub Automation (`uaft repo`)
- **Repo Management**: Initialize (`init`), create remote (`create`), and push (`push`) from the CLI.
- **GitHub Integration**: Uses `gh` CLI to create public/private repositories and link them automatically.
- **Branching Standard**: Automatically renames the default branch to `mother`.

## 📄 Documentation & Governance
- **Standard Files**: Added `LICENSE` (MIT), `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`, `DISCLAIMER.md`.
- **Updated README**: Documented new commands and features.

## 🛠️ Improvements
- **Zero-Dependency Testing**: `uaft test` now falls back to `unittest` if `pytest` is not installed.
- **CLI UX**: Added confirmation prompts for major actions.

## 📦 Installation
```bash
pip install uaft
```


---

## Previous Releases

# UAFT v0.2.0 Release Notes

**"The Universal Release"**

This release marks a major milestone in the evolution of UAFT, transforming it from a project-specific tool into a universal, configuration-driven automation framework.

## 🌟 New Features

### Universal Configuration (`uaft.yaml`)
- **Config-Driven Workflows**: `fix`, `cleanup`, and `test` commands are now fully controlled by `uaft.yaml`.
- **Project Independence**: UAFT no longer contains hardcoded logic for specific projects.
- **`uaft init`**: Quickly scaffold a new `uaft.yaml` for any project.

### Plugin System
- **Extensibility**: Install external scripts as first-class UAFT commands.
- **Commands**:
    - `uaft plugin install <path/url>`
    - `uaft plugin list`
    - `uaft <plugin-name> [args]`

### Enhanced Testing
- **Integrated Tracking**: `uaft test --track` automatically logs results to the tracker database.
- **Flexible Runner**: Configure any test runner (pytest, npm test, cargo test) in `uaft.yaml`.

## 🛠️ Breaking Changes
- **`uaft fix`**: No longer defaults to hardcoded Python formatters. You MUST define `fix` steps in `uaft.yaml`.
- **`uaft cleanup`**: No longer defaults to hardcoded patterns. You MUST define `cleanup` patterns in `uaft.yaml`.

## 📦 Installation

```bash
pip install uaft
```

## 🚀 Getting Started

```bash
cd my-project
uaft init
uaft fix
```


---

**Note:** For detailed commit history, see the [git log](https://github.com/nabaznyl/uaft/commits/mother).
