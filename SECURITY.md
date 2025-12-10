# Security Policy

## Supported Versions

Use this section to tell people about which versions of your project are
currently being supported with security updates.

| Version | Supported          |
| ------- | ------------------ |
| 0.2.x   | :white_check_mark: |
| < 0.2.0 | :x:                |

## Reporting a Vulnerability

We take the security of UAFT seriously. If you discover a security vulnerability, please do NOT open a public issue.

Instead, please report it responsibly by emailing **anonmaly@example.com** (replace with actual security email if available).

Please include:
- A description of the vulnerability.
- Steps to reproduce the issue.
- Potential impact.

We will acknowledge your report within 48 hours and provide an estimated timeline for a fix.

## Security Best Practices for Users

- Always review `uaft.json` configurations before running automation scripts in untrusted projects.
- Use the `--dry-run` flag with `uaft cleanup` to verify what will be deleted.
- Keep UAFT updated to the latest version via `pip install --upgrade uaft`.
