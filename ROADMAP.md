# UAFT Roadmap (2025-2026)

**Vision:** To be the standard, zero-dependency automation framework for modern development.

## Phase 1: Zero-Dependency Core (Completed - v0.2.0)
- [x] **Zero Dependencies**: Removed `rich`, `click`, `pyyaml`, `watchdog`.
- [x] **Configuration**: Migrated to `uaft.json` (Standard Library JSON).
- [x] **Core Commands**: Implemented `init`, `fix`, `cleanup`, `test` with pure Python.
- [x] **Safety**: Added confirmation prompts for destructive/long-running actions (`test`).
- [x] **Standardization**: Implemented universal task templates in `uaft init`.
- [x] **Watch Mode v1**: Basic polling-based file watcher.

## Phase 2: Integration & Expansion (Q1 2026)
- [ ] **Remote Plugins**: Support installing plugins from URLs (e.g., `uaft plugin install https://...`).
- [ ] **Interactive Mode**: A simple TUI for selecting tasks (using standard library `curses` or raw input).
- [ ] **Git Integration**: Built-in git hook management and status checks.

## Phase 3: Ecosystem (Q2 2026)
- [ ] **Language Templates**: `uaft init --lang python`, `uaft init --lang node` (Enhanced).
- [ ] **CI/CD Integration**: GitHub Actions / GitLab CI templates that use `uaft`.
- [ ] **Registry**: A simple JSON-based registry for discovering community plugins.

## Phase 4: Advanced Features (Q3 2026)
- [ ] **Parallel Execution**: Run independent tasks in parallel (using `multiprocessing`).
- [ ] **Dependency Graph**: Define task dependencies (e.g., `test` depends on `build`).
- [ ] **Watch Mode 2.0**: Smarter file watching with debounce and gitignore support.
