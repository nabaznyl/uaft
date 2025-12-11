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
