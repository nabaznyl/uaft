# UAFT Project Bookmark
**Date:** December 10, 2025
**Status:** Phase 2 Paused (Automation Complete, Features Pending)
**Version:** v0.2.1
**Branch:** `mother`

## 🛑 Where We Left Off
We successfully professionalized the project with **Zero-Dependency Core**, **PyPI Automation**, and **Git Automation**. We paused development to switch focus to the `lmapp` project.

## 🏗️ Current State
- **Published:** PyPI (v0.2.1)
- **Repo:** GitHub (nabaznyl/uaft)
- **Clean:** Legacy bash scripts removed. Pure Python structure.

## 📋 Pending Tasks (Phase 2 Expansion)
When you return, these are the next immediate tasks:

1.  **Remote Plugins**
    *   **Goal:** Allow installing plugins from URLs.
    *   **File:** `src/uaft/plugin_manager.py`
    *   **Command:** `uaft plugin install https://example.com/plugin.sh`

2.  **Interactive Mode**
    *   **Goal:** TUI menu for selecting tasks.
    *   **File:** New file (e.g., `src/uaft/interactive.py`)
    *   **Command:** `uaft interactive` or just `uaft` with no args.

## 🔄 How to Resume
1.  `cd ~/projects/uaft`
2.  `source .venv/bin/activate`
3.  Review `TODO.md` and `ROADMAP.md`
