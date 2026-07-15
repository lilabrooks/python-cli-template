# python-cli-template

A walking skeleton for Python 3.12+ command-line tools: a minimal working CLI
(`skeleton-cli`) that already passes a production-grade quality gate, so a new
project starts at "green" instead of at "empty directory".

This is a **stack template** — it carries toolchain decisions, not process.
It pairs with (but does not require)
[claude-okf-repo-kit](https://github.com/lilabrooks/claude-okf-repo-kit),
which layers the operating contract — goal file, specs/ADRs, source-to-knowledge
mapping, session hooks — on top of whatever stack exists. Template first, kit
second, then the goal loop builds your actual tool.

## What you get

- **A real CLI, not stubs.** `skeleton-cli hello`, `ask`, and `providers`
  work out of the box; the template's own CI keeps every piece green, so the
  chassis cannot rot silently.
- **The quality gate.** ruff (lint + format), mypy `strict`, pytest with a
  70% branch-coverage floor, and docs validation — one `make check`, mirrored
  by three GitHub Actions workflows across Python 3.12–3.14.
- **Repository-health tests.** The repo tests itself: the version must agree
  across `pyproject.toml`, the package, `CHANGELOG.md`, and docs; no tracked
  file may match `.gitignore`; `requirements.txt` must mirror the optional
  extras; a second agent's config mirror (if you add one) must stay in parity.
- **An optional model-provider layer** (deletable, see below): the one-method
  `LanguageModel` protocol, a registry with `echo`/`anthropic`/`openai`
  adapters, environment-only settings, and safe-by-default file writes.
  Zero runtime dependencies — vendor SDKs are opt-in extras with deferred
  imports, so the CLI works offline and credential-free by default.

The chassis was extracted one time from
[spec-agent-cli](https://github.com/lilabrooks/spec-agent-cli), where each
piece shipped and was hardened in real use; this template's own CI keeps it
honest from here.

## Using the template

**Preferred path — one command from a template checkout.** Deterministic and
agent-neutral (plain bash; equally runnable by a human, Claude Code, or
Codex), so no session re-derives the sequence:

```bash
bash scripts/create-project /path/to/your-tool your-tool-name
```

It extracts this template's committed tree into the target (a fresh directory,
or an existing repo that only carries goal-shaped content like `docs/GOAL.md`
— colliding files are refused, an existing `.gitignore` is merged), renames
the skeleton, git-inits if needed, creates a venv and runs `make check`,
installs [claude-okf-repo-kit](https://github.com/lilabrooks/claude-okf-repo-kit)
when a clone is available (`--kit /path`, auto-detected as a sibling, or
`--no-kit`), removes the template-side tooling from the target, and prints the
judgment steps that remain: project README and CHANGELOG, the goal, the
playbook brackets. Its contract is guarded by `tests/test_create_project.py`
in this repo's own CI.

**Manual path** (the same sequence, step by step):

1. **Create your repo from this one** (GitHub "Use this template", or clone
   and re-init).
2. **Rename the skeleton** (single-use, then delete the script):

   ```bash
   bash scripts/rename-project your-tool-name
   ```

   This rewrites the package (`skeleton_cli`), distribution (`skeleton-cli`),
   and env-var prefix (`SKELETON_CLI`) everywhere, moves the source directory,
   and substitutes your `git config user.name` as owner in the docs.
3. **Verify the gate:**

   ```bash
   python3 -m venv .venv
   .venv/bin/pip install -e ".[dev,anthropic,openai]"
   make check
   ```

4. **Optionally install the kit on top** for the goal loop and knowledge
   discipline:

   ```bash
   bash /path/to/claude-okf-repo-kit/scripts/update-existing-repo .
   ```

5. Replace the `hello` command with your tool's real surface and start
   building. The README you are reading describes the template — rewrite it
   for your project.

## The walking skeleton

```bash
$ skeleton-cli hello
Hello, world!

$ skeleton-cli ask "ping"          # echo provider: offline, no credentials
Echo provider received: ping

$ skeleton-cli providers
anthropic
echo
openai

$ skeleton-cli ask "ping" -p anthropic   # real vendor: needs the extra + key
```

## Deleting the model-provider layer

If your CLI does not call language models, remove in one commit: the
`agents/`, `config/`, `core/`, `providers/`, and `runtime/` packages under
`src/`, their tests (`test_agent`, `test_factory`, `test_settings`,
`test_fileset`, `test_*_provider`), the `ask`/`providers` commands in
`cli.py`, the `anthropic`/`openai` extras in `pyproject.toml` and their
mirror lines in `requirements.txt`, the extras in the workflows and
`Makefile check-all`, and `.env.example`. Run `make check`; the gate tells
you what you missed.

## Layout

```
├── .github/workflows/   # quality, tests, coverage — Python 3.12–3.14 matrix
├── docs/                # knowledge bundle root (starts empty by design)
├── scripts/
│   ├── check-okf-docs.py   # stdlib-only docs validator, wired into make check
│   └── rename-project      # single-use parameterization, delete after use
├── src/skeleton_cli/    # the walking skeleton
└── tests/               # CLI, provider-layer, and repository-health tests
```
