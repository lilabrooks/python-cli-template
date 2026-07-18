---
title: Documentation log
type: log
status: current
date: 2026-07-17
owner: Lila Brooks
deciders: [Lila Brooks]
tags: [documentation, log]
---

# Documentation log

Dated changes to the docs bundle, newest first.

## 2026-07-17

- Fixed `rename-project`'s excluded-directory traversal for checkout paths
  containing glob characters such as square brackets. Directory-name pruning
  now keeps `.git`, virtual environments, and tool caches outside the rename;
  a regression test places rewriteable sentinels in each excluded directory.
- Added `CLAUDE.md` beside `AGENTS.md` in the source-distribution manifest and
  guarded both agent instruction entry points with a repository-health test.
- Aligned the manual template-setup path with the scripted one on cleanup.
  The README manual path and `rename-project`'s printed next steps now instruct
  removing all three single-use generator files (`rename-project`,
  `create-project`, `tests/test_create_project.py`), matching what
  `create-project` removes automatically. This stops projects created via the
  GitHub "Use this template" button from carrying generator tooling into their
  first commit.
- Kept claude-okf-repo-kit's safe same-name-file behavior visible during
  project creation. `create-project` now prints the installer summary and
  explains that `CLAUDE.2.md` is an inactive review candidate; the README
  documents the review, merge, deletion, verification, and commit sequence.
  A generated-project regression test preserves the live `CLAUDE.md` while
  checking candidate reporting, and a manual run against the sibling real kit
  passed its `verify-install` gate without warnings.
- Prepared the repository for public template use: generalized security and
  contribution guidance for generated projects, added support and contributor
  forms, documented the Bash/Make platform boundary, and clarified that the
  example wheel validates the chassis rather than distributing the generator.
  Project renaming now starts a fresh changelog and documentation log, while
  package and CI checks cover the complete source archive.

## 2026-07-14

- Added `scripts/check-env.py`, an environment preflight run first by
  `make check`, `make check-all`, and the code-quality workflow. Synced
  folders (iCloud Desktop & Documents and similar) stamp macOS hidden flags
  onto `.venv` files — Python 3.13+ skips hidden `.pth` files, silently
  breaking editable installs and console scripts while pytest still passes —
  and leave ` 2` conflict duplicates and `.icloud` placeholders. The preflight
  turns that damage into one actionable failure with the fix in the message;
  AGENTS.md and the README document it and the best-effort `.venv.nosync`
  fallback. The detector also catches conflict copies of tool directories
  themselves and deduplicates symlinked environment roots. Guarded by
  `tests/test_check_env.py`.
- Added Codex cloud setup-script guidance, stable help output for the project
  scripts, and a pip fallback that works when target paths contain brackets.
  Paths containing `#` now fail early because Python console-script shebangs
  cannot portably use them. Removed two undocumented Codex-local names from
  `.gitignore`; CI now exercises the bracketed-path case.
- Added `.venv.nosync/` to `.gitignore` so synced-folder checkouts can keep the
  conventional `.venv` link without cloud storage hiding editable-install
  `.pth` files.
- Marked the template package as first-party in Ruff configuration; the rename
  script carries the setting forward, preventing package-name-dependent import
  sorting failures in generated projects.
- Raised the branch-coverage floor from 70% to 90% and made the coverage run
  part of `make check` and `make check-all`; the cross-version gate now launches
  isolated uv environments from a temporary directory without using or
  replacing `.venv` or creating a lockfile.
  Added a root `AGENTS.md` with the stack commands and safety rules Codex needs
  on first use, tightened hook and skill mirror parity, added an installed
  console-script test, and added a Python 3.14 CI smoke job for the complete
  generated-project path.
- Made uv the preferred generated-project setup: `create-project` now runs
  `uv sync --all-extras`, writes the renamed project's `uv.lock`, and verifies
  through `uv run make check`. Machines without uv keep the venv/pip path, and
  `--pip` selects that fallback explicitly. CI exercises both paths. Corrected
  all workflow checkout steps to the current `actions/checkout@v6` release,
  set read-only repository permissions, fixed stale README layout details, and
  removed the obsolete Snyk label from the dependency-scanner manifest.
- Tightened generated-file safety: incomplete fences, symlink escapes,
  mismatched file/target lists, and duplicate targets are rejected before a
  write. Added regression tests for each case.
- Audited `.gitignore`: added Codex's local `.codex-log/`, anchored build and
  coverage reports to the repository root, and added repository-health tests
  for ignored artifacts and intentionally trackable project files.
- Documented the design rationale and agent usage in the README: why stack
  and process are separate layers, why a walking skeleton beats file stubs,
  and why the mechanics live in scripts. A new "Working with Claude Code and
  Codex" section states that the template uses bash/make, points at the worked
  Codex-mirror pattern in spec-drift and spec-agent-cli, and notes the
  pre-wired parity guards in the repository-health tests.
  `create-project`'s next-steps output now names the Codex path for the goal
  step. Docs only; no behavior change.
- Extended Dependabot to the `pip` ecosystem (weekly) alongside
  `github-actions`: unlike spec-agent-cli, this repo runs no Snyk, so
  Dependabot is the dependency-vulnerability watch; no secrets required.
- Added `scripts/create-project` and its smoke tests: the mechanical
  template-to-project sequence (extract, rename, merge, git-init, gate, kit
  install, tooling cleanup) now lives in one deterministic, agent-neutral
  script instead of being re-derived from README prose each time — per the
  division-of-labor rule that mechanics that must never vary belong in
  scripts. The sequence was proven manually on spec-drift first; the script
  encodes that run. Version 0.1.1.
- Seeded the repository from python-cli-template: a walking-skeleton CLI with
  the quality gate (ruff, mypy strict, pytest with a 70% branch-coverage
  floor, OKF docs validation), repository-health tests, CI workflows, and an
  optional model-provider layer. The chassis was extracted one time from
  spec-agent-cli, where each piece shipped and was hardened in production use.
