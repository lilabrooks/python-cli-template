# Repository instructions

## Purpose

This repository is a Python 3.12+ command-line application with a `src/`
layout. It may be the `python-cli-template` checkout or a project created from
that template.

When `scripts/create-project` exists and the task is to start a separate
project, use that script. It handles extraction, renaming, environment setup,
and verification.

## Setup

For a project created from this template, use uv and commit the generated
`uv.lock`:

```bash
uv sync --all-extras
uv run make check
```

The template checkout intentionally has no lockfile. To work on the template
itself without creating one, use uv's pip interface:

```bash
uv venv
uv pip install -e ".[dev,anthropic,openai]"
make check
```

The portable fallback is:

```bash
python3 -m venv .venv
.venv/bin/pip install -e ".[dev,anthropic,openai]"
make check
```

For Codex cloud environments, put the applicable setup block above in the
environment setup script: setup runs with network access, while agent-phase
internet access is off by default.

The default `echo` provider works offline. Treat Anthropic and OpenAI calls as
external operations that require the matching optional dependency, network
access, and an environment-provided API key.

## Verification

Run `make check` before handing off a change. It runs Ruff lint and formatting
checks, strict mypy, pytest with branch coverage, and documentation validation.
The coverage floor is 90%.

Use `make check-all` when a change may behave differently across Python 3.12,
3.13, and 3.14. It requires `uv`, can download interpreters, and uses isolated
environments without replacing the project's `.venv` or writing a lockfile.

## Change rules

- Add or update tests when behavior changes.
- Update `README.md` when setup, commands, or user-visible behavior changes.
- Record documentation-bundle changes at the top of `docs/log.md`.
- Keep package, changelog, and documentation version references consistent.
- Keep provider tests offline. Use fakes or mocks for vendor SDK calls.
- Never commit `.env`, `.venv/`, coverage databases, caches, or build output.
- Preserve safe file-write behavior: reject path escapes and refuse overwrites
  unless the caller explicitly opts in.
