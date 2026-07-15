---
title: Documentation log
type: log
status: current
date: 2026-07-14
owner: Lila Brooks
deciders: [Lila Brooks]
tags: [documentation, log]
---

# Documentation log

Dated changes to the docs bundle, newest first.

## 2026-07-14

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
