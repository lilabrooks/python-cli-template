# Contributing

Thanks for helping keep this template boring in the best way: green checks,
small changes, and no mystery setup.

## Local setup

Use uv when possible:

```bash
uv sync --all-extras
uv run make check
```

Portable fallback:

```bash
python3 -m venv .venv
.venv/bin/pip install -e ".[dev,anthropic,openai]"
make check
```

If you are working in Codex cloud, put dependency installation in the
environment setup script so it runs while network access is available.

## Before opening a pull request

- Run `make check`.
- Keep the generated-project path working through `scripts/create-project`.
- Update `CHANGELOG.md` for user-visible changes.
- Mirror dependency changes between `pyproject.toml` and `requirements.txt`
  when optional extras change.
- Keep documentation agent-neutral unless a file is intentionally specific to
  one tool.

## Change style

Prefer small, direct patches. This repository is a template, so every extra
choice becomes something copied into new projects. Add defaults only when they
are useful for most Python CLI tools.

## Generated projects

When changing setup scripts, test at least one generated project. The CI smoke
test covers both uv and pip paths, but a local generated project is often the
fastest way to catch awkward output or missing cleanup.
