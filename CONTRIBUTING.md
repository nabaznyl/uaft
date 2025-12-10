# Contributing to UAFT

Thank you for your interest in contributing to UAFT (Universal Automation Framework Tool)! We welcome contributions from the community to help make this tool better for everyone.

## Code of Conduct

By participating in this project, you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md).

## How to Contribute

### Reporting Bugs

If you find a bug, please open an issue on GitHub with the following details:
- A clear description of the issue.
- Steps to reproduce the behavior.
- Expected behavior vs. actual behavior.
- Your environment details (OS, Python version, UAFT version).

### Suggesting Enhancements

We welcome ideas for new features! Please open an issue to discuss your idea before implementing it.

### Pull Requests

1.  **Fork the repository** and create your branch from `mother`.
2.  **Install development dependencies**:
    ```bash
    pip install -e .[dev]
    ```
3.  **Make your changes**. Ensure your code follows the project's style.
4.  **Run tests**:
    ```bash
    uaft test
    ```
5.  **Submit a Pull Request** to the `mother` branch. Provide a clear description of your changes.

## Development Setup

1.  Clone the repository.
2.  Create a virtual environment:
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```
3.  Install in editable mode:
    ```bash
    pip install -e .
    ```

## Style Guide

- We use `black` for Python formatting.
- We use `isort` for import sorting.
- Run `uaft fix` to automatically format your code before submitting.

## License

By contributing, you agree that your contributions will be licensed under the [MIT License](LICENSE).
