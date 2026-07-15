# Changelog

All notable changes to this project are documented here. The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
