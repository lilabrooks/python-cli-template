# Local quality checks. Mirrors the GitHub Actions workflows.
#
#   make check       Run lint, type-check, tests, and docs validation on the
#                    active interpreter (whatever your .venv has). This is the
#                    everyday command.
#   make check-all   Run the same checks across every supported Python version.
#                    Uses uv to fetch interpreters on demand; CI already does
#                    this on push, so reach for it mainly to reproduce a
#                    version-specific failure locally.
#
# Individual targets (lint, typecheck, test, okf, coverage) are available too.

PYTHON ?= $(if $(wildcard .venv/bin/python),.venv/bin/python,python3)
RUFF ?= $(if $(wildcard .venv/bin/ruff),.venv/bin/ruff,ruff)
MYPY ?= $(if $(wildcard .venv/bin/mypy),.venv/bin/mypy,mypy)
PYTEST ?= $(if $(wildcard .venv/bin/pytest),.venv/bin/pytest,pytest)
VERSIONS ?= 3.12 3.13 3.14

.PHONY: check lint format typecheck test okf coverage check-all

check: lint typecheck test okf

lint:
	$(RUFF) check .
	$(RUFF) format --check .

format:
	$(RUFF) format .

typecheck:
	$(MYPY)

test:
	$(PYTEST)

okf:
	$(PYTHON) scripts/check-okf-docs.py

coverage:
	@$(PYTHON) -c 'import coverage' >/dev/null 2>&1 || { \
		echo "coverage is not installed. Run '$(PYTHON) -m pip install -e \".[dev]\"'."; \
		exit 127; \
	}
	$(PYTHON) -m coverage run -m pytest
	$(PYTHON) -m coverage report

check-all:
	@command -v uv >/dev/null 2>&1 || { \
		echo "check-all needs uv (https://docs.astral.sh/uv/). Install it, or run 'make check' per interpreter."; \
		exit 1; \
	}
	@for v in $(VERSIONS); do \
		echo "=== Python $$v ==="; \
		uv run --python $$v --extra dev --extra anthropic --extra openai -- ruff check . && \
		uv run --python $$v --extra dev --extra anthropic --extra openai -- ruff format --check . && \
		uv run --python $$v --extra dev --extra anthropic --extra openai -- mypy && \
		uv run --python $$v --extra dev --extra anthropic --extra openai -- pytest && \
		uv run --python $$v --extra dev --extra anthropic --extra openai -- python scripts/check-okf-docs.py || exit 1; \
	done
	@echo "All versions passed."
