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

- Documented the design rationale and agent usage in the README: why stack
  and process are separate layers (and therefore why no agent config ships
  in the template), why a walking skeleton beats file stubs, and why the
  mechanics live in scripts. A new "Working with Claude Code and Codex"
  section states that the template is agent-neutral bash/make, points at the
  worked Codex-mirror pattern in spec-drift and spec-agent-cli, and notes the
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
