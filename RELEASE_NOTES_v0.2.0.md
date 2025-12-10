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
