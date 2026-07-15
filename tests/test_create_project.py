"""Smoke tests for scripts/create-project.

The script is the deterministic path agents and humans run to stamp this
template into a new project, so its contract is guarded here: extraction from
the committed tree, rename, .gitignore merge, collision refusal, uv setup,
and removal of the single-use scripts. CI exercises the complete uv and pip
paths against a generated project.
"""

import os
import shutil
import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent


def _require_git_checkout() -> None:
    if shutil.which("git") is None or not (REPO_ROOT / ".git").exists():
        pytest.skip("not a git checkout")


def _create(
    target: Path,
    dist: str,
    *,
    skip_venv: bool = True,
    env: dict[str, str] | None = None,
) -> subprocess.CompletedProcess[str]:
    command = [
        "bash",
        str(REPO_ROOT / "scripts" / "create-project"),
        str(target),
        dist,
    ]
    if skip_venv:
        command.append("--skip-venv")
    command.append("--no-kit")
    return subprocess.run(
        command,
        capture_output=True,
        text=True,
        check=False,
        env=env,
    )


def test_creates_renamed_project_from_committed_tree(tmp_path: Path) -> None:
    _require_git_checkout()
    target = tmp_path / "new-proj"

    result = _create(target, "sample-tool")

    assert result.returncode == 0, result.stderr
    assert (target / "src" / "sample_tool" / "cli.py").is_file()
    assert (target / ".git").is_dir()
    leftovers = [
        path
        for path in target.rglob("*")
        if path.is_file()
        and ".git" not in path.parts
        and any(
            token in path.read_text(encoding="utf-8", errors="ignore")
            for token in ("skeleton_cli", "skeleton-cli", "SKELETON_CLI")
        )
    ]
    assert not leftovers, f"skeleton tokens survived in: {leftovers}"


def test_removes_single_use_scripts_from_target(tmp_path: Path) -> None:
    _require_git_checkout()
    target = tmp_path / "new-proj"

    _create(target, "sample-tool")

    assert not (target / "scripts" / "rename-project").exists()
    assert not (target / "scripts" / "create-project").exists()
    assert not (target / "tests" / "test_create_project.py").exists()
    assert (target / "scripts" / "check-okf-docs.py").is_file()


def test_prefers_uv_and_writes_project_lock(tmp_path: Path) -> None:
    _require_git_checkout()
    target = tmp_path / "new-proj"
    fake_bin = tmp_path / "bin"
    fake_bin.mkdir()
    fake_uv = fake_bin / "uv"
    fake_uv.write_text(
        """#!/bin/sh
case "$1" in
  sync)
    mkdir -p .venv/bin
    printf 'version = 1\\n' > uv.lock
    ;;
  run)
    ;;
  *)
    exit 2
    ;;
esac
""",
        encoding="utf-8",
    )
    fake_uv.chmod(0o755)
    env = os.environ.copy()
    env["PATH"] = f"{fake_bin}{os.pathsep}{env['PATH']}"

    result = _create(target, "sample-tool", skip_venv=False, env=env)

    assert result.returncode == 0, result.stderr
    assert (target / ".venv").is_dir()
    assert (target / "uv.lock").read_text(encoding="utf-8") == "version = 1\n"
    assert "uv synced all extras; uv.lock created; make check passed" in result.stdout


def test_merges_existing_gitignore_and_keeps_goal(tmp_path: Path) -> None:
    _require_git_checkout()
    target = tmp_path / "goal-only"
    (target / "docs").mkdir(parents=True)
    (target / "docs" / "GOAL.md").write_text("# Goal\n", encoding="utf-8")
    (target / ".gitignore").write_text("my-custom-entry\n", encoding="utf-8")

    result = _create(target, "sample-tool")

    assert result.returncode == 0, result.stderr
    assert (target / "docs" / "GOAL.md").read_text(encoding="utf-8") == "# Goal\n"
    gitignore = (target / ".gitignore").read_text(encoding="utf-8")
    assert "my-custom-entry" in gitignore
    assert ".venv/" in gitignore


def test_refuses_colliding_target_files(tmp_path: Path) -> None:
    _require_git_checkout()
    target = tmp_path / "occupied"
    target.mkdir()
    (target / "Makefile").write_text("all:\n", encoding="utf-8")

    result = _create(target, "sample-tool")

    assert result.returncode == 1
    assert "Makefile" in result.stderr
    assert not (target / "pyproject.toml").exists()


def test_refuses_target_inside_template_without_creating_it() -> None:
    _require_git_checkout()
    target = REPO_ROOT / "qa-inside-target"

    result = _create(target, "sample-tool")

    assert result.returncode == 1
    assert "inside the template checkout" in result.stderr
    assert not target.exists(), "refusal must not leave a stray directory behind"


def test_rejects_invalid_dist_name(tmp_path: Path) -> None:
    _require_git_checkout()

    result = _create(tmp_path / "x", "Bad_Name")

    assert result.returncode == 2
    assert "Invalid dist name" in result.stderr
