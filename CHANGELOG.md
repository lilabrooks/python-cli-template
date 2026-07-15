# Changelog

All notable changes to this project are documented here. The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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
  including the `.venv.nosync` mitigation for synced checkouts.

### Changed

- Raised the branch-coverage floor to 90% and made coverage part of
  `make check` and `make check-all`. Cross-version checks now launch isolated
  uv environments from a temporary directory, without using or replacing
  `.venv` or creating `uv.lock`.
- Codex hook and skill mirror checks now reject missing source directories,
  missing mirror entries, and extra mirror entries.
- CI exercises both generated-project setup paths: uv and venv/pip.
- GitHub Actions now use the current `actions/checkout@v6` release instead of
  the nonexistent v7 tag and declare read-only repository permissions.
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
