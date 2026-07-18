# Changelog

All notable changes to this project are documented here. The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Root `CLAUDE.md` that imports `AGENTS.md`, so Claude Code and Codex read one
  set of repository instructions from a single source.

### Changed

- README now leads the "Using the template" section with the rename step the
  GitHub "Use this template" button cannot run, and describes the owner,
  contact, and version resets `rename-project` performs.

## [0.2.0] - 2026-07-17

### Added

- Root `AGENTS.md` with Codex setup, verification, and repository-safety
  instructions.
- Installed console-script coverage and a full generated-project CI smoke test.
- uv-first project setup with a project-specific lockfile and an explicit
  `--pip` fallback in `scripts/create-project`.
- Codex cloud guidance for installing dependencies during the network-enabled
  environment setup phase.
- `scripts/check-env.py`, an environment preflight that runs first in
  `make check`, `make check-all`, and the code-quality workflow: it detects
  file-sync damage (hidden `.pth` flags that Python 3.13+ silently skips,
  ` 2` conflict duplicates, `.icloud` placeholders) and prints the fix,
  including `.venv.nosync` as a best-effort fallback for synced checkouts.
- Canonical GitHub comparison links for changelog release headings.
- Repository community docs: `SECURITY.md`, `CONTRIBUTING.md`, and
  `CODE_OF_CONDUCT.md`.
- `SUPPORT.md`, structured bug, feature, and question forms, and a pull-request
  checklist for public contributors.
- Distribution smoke coverage that installs the wheel and runs the test suite
  from the built source archive.

### Changed

- Raised the branch-coverage floor to 90% and made coverage part of
  `make check` and `make check-all`. Cross-version checks now launch isolated
  uv environments from a temporary directory, without using or replacing
  `.venv` or creating `uv.lock`.
- Codex hook and skill mirror checks now reject missing source directories,
  missing mirror entries, and extra mirror entries.
- CI exercises both generated-project setup paths: uv and venv/pip.
- GitHub Actions use `actions/checkout@v7` and `actions/setup-python@v6`, pinned
  to verified full commit SHAs, with read-only repository permissions.
- Corrected stale README layout details and the dependency manifest's obsolete
  Snyk label.
- Generated-file parsing and writes now reject incomplete fences, symlink path
  escapes, mismatched file/target lists, and duplicate targets before writing.
- `.gitignore` now covers local Codex logs and anchors build/report output to
  the repository root so nested source directories remain trackable.
- Project-creation help no longer depends on shell-script line numbers. The pip
  fallback now supports bracketed target paths and rejects `#` paths before
  creating files because Python console-script shebangs cannot portably use
  them.
- Removed undocumented Codex-local filenames from `.gitignore` so unexpected
  repository files remain visible.
- Added `.venv.nosync/` support for virtual environments in cloud-synced
  checkouts while keeping the conventional `.venv` path ignored.
- Ruff now identifies the template package as first-party, so renamed projects
  keep valid import ordering regardless of the chosen package name.
- The environment preflight detects conflict copies of tool directories
  themselves and avoids double-reporting a virtual environment reached through
  both `.venv` and `.venv.nosync`.
- Generated projects now start at version 0.1.0 with fresh changelog and
  documentation history, preserve existing Git worktrees, and rerun the gate
  after optional kit installation.
- Source archives now include every file required by their bundled tests and
  repository gate.
- CI limits push runs to `main` and release tags, cancels superseded runs,
  checks shell syntax, applies job timeouts, and verifies built distributions.
- Community and support guidance is safe to copy into generated projects, and
  the README states the supported project-creation platforms and package
  publishing boundary.

## [0.1.1] - 2026-07-14

### Added

- `scripts/create-project`: one-command, agent-neutral project creation —
  extracts the committed template tree into a fresh or goal-only target,
  renames the skeleton, merges an existing `.gitignore`, git-inits, runs the
  gate in a new venv, optionally installs claude-okf-repo-kit, removes the
  template-side tooling from the target, and prints the remaining judgment
  steps. Contract guarded by `tests/test_create_project.py`.
- Dependabot now also watches the `pip` ecosystem weekly: this repo carries no
  Snyk scanning, so Dependabot covers Python dependency vulnerabilities in the
  scanner mirror and extras without needing secrets.

## [0.1.0] - 2026-07-14

### Added

- Walking-skeleton CLI (`skeleton-cli`) with `hello`, `ask`, and `providers`
  commands, seeded by python-cli-template.
- Quality gate: ruff (lint + format), mypy strict, pytest with a 70%
  branch-coverage floor, and OKF docs validation, wired into `make check` and
  three GitHub Actions workflows across Python 3.12-3.14.
- Repository-health tests: version agreement across the package, changelog,
  and docs; no tracked files matching `.gitignore`; scanner-manifest sync;
  optional dual-agent config parity.
- Optional model-provider layer: the one-method `LanguageModel` protocol, a
  provider registry with `echo`, `anthropic`, and `openai` adapters (vendor
  SDKs as optional extras with deferred imports), environment-only settings,
  and safe-by-default file writes.

[Unreleased]: https://github.com/lilabrooks/python-cli-template/compare/v0.2.0...HEAD
[0.2.0]: https://github.com/lilabrooks/python-cli-template/compare/v0.1.1...v0.2.0
[0.1.1]: https://github.com/lilabrooks/python-cli-template/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/lilabrooks/python-cli-template/releases/tag/v0.1.0
