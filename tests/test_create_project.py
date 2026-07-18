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
import tomllib
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
    kit: Path | None = None,
) -> subprocess.CompletedProcess[str]:
    command = [
        "bash",
        str(REPO_ROOT / "scripts" / "create-project"),
        str(target),
        dist,
    ]
    if skip_venv:
        command.append("--skip-venv")
    if kit is None:
        command.append("--no-kit")
    else:
        command.extend(["--kit", str(kit)])
    return subprocess.run(
        command,
        capture_output=True,
        text=True,
        check=False,
        env=env,
    )


def test_create_project_help_lists_supported_options() -> None:
    result = subprocess.run(
        ["bash", str(REPO_ROOT / "scripts" / "create-project"), "--help"],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    assert result.stdout.startswith("Usage:\n")
    for option in ("--kit DIR", "--no-kit", "--pip", "--skip-venv"):
        assert option in result.stdout
    assert result.stderr == ""


def test_rename_project_usage_is_stable() -> None:
    result = subprocess.run(
        ["bash", str(REPO_ROOT / "scripts" / "rename-project")],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 2
    assert result.stderr.startswith("Usage:\n")
    assert "DIST must use lowercase letters" in result.stderr
    assert result.stdout == ""


def test_creates_renamed_project_from_committed_tree(tmp_path: Path) -> None:
    _require_git_checkout()
    target = tmp_path / "new-proj"

    result = _create(target, "sample-tool")

    assert result.returncode == 0, result.stderr
    assert (target / "src" / "sample_tool" / "cli.py").is_file()
    assert (target / ".git").is_dir()
    metadata = tomllib.loads((target / "pyproject.toml").read_text(encoding="utf-8"))
    assert metadata["project"]["version"] == "0.1.0"
    assert '__version__ = "0.1.0"' in (target / "src" / "sample_tool" / "__init__.py").read_text(
        encoding="utf-8"
    )
    changelog = (target / "CHANGELOG.md").read_text(encoding="utf-8")
    assert "## 0.1.0 -" in changelog
    assert "python-cli-template/compare" not in changelog
    docs_log = (target / "docs" / "log.md").read_text(encoding="utf-8")
    assert "Started the project documentation bundle" in docs_log
    assert "file-sync damage" not in docs_log
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
    result = subprocess.run(
        ["make", "shell"],
        cwd=target,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr


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
    gitignore_lines = (target / ".gitignore").read_text(encoding="utf-8").splitlines()
    assert "my-custom-entry" in gitignore_lines
    assert ".venv" in gitignore_lines
    assert ".venv.nosync/" in gitignore_lines


def test_keeps_existing_git_worktree(tmp_path: Path) -> None:
    _require_git_checkout()
    parent = tmp_path / "parent"
    target = tmp_path / "worktree"
    subprocess.run(["git", "init", "-q", str(parent)], check=True)
    subprocess.run(["git", "-C", str(parent), "config", "user.name", "Template Test"], check=True)
    subprocess.run(
        ["git", "-C", str(parent), "config", "user.email", "template@example.invalid"],
        check=True,
    )
    subprocess.run(
        ["git", "-C", str(parent), "commit", "--allow-empty", "-qm", "initial"], check=True
    )
    subprocess.run(
        ["git", "-C", str(parent), "worktree", "add", "-qb", "generated", str(target)],
        check=True,
    )

    result = _create(target, "sample-tool")

    assert result.returncode == 0, result.stderr
    assert (target / ".git").is_file()
    assert "kept the existing git repository" in result.stdout
    assert "template@example.invalid" in (target / "SECURITY.md").read_text(encoding="utf-8")
    assert "template@example.invalid" in (target / "CODE_OF_CONDUCT.md").read_text(encoding="utf-8")


def test_reruns_gate_after_kit_install(tmp_path: Path) -> None:
    _require_git_checkout()
    target = tmp_path / "new-proj"
    fake_bin = tmp_path / "bin"
    fake_bin.mkdir()
    run_log = tmp_path / "uv-runs"
    fake_uv = fake_bin / "uv"
    fake_uv.write_text(
        """#!/bin/sh
case "$1" in
  sync)
    mkdir -p .venv/bin
    printf 'version = 1\\n' > uv.lock
    ;;
  run)
    printf 'run\\n' >> "$RUN_LOG"
    ;;
  *)
    exit 2
    ;;
esac
""",
        encoding="utf-8",
    )
    fake_uv.chmod(0o755)
    kit = tmp_path / "kit"
    (kit / "scripts").mkdir(parents=True)
    (kit / "scripts" / "update-existing-repo").write_text(
        '#!/bin/sh\ntouch "$1/KIT_INSTALLED"\n',
        encoding="utf-8",
    )
    env = os.environ.copy()
    env["PATH"] = f"{fake_bin}{os.pathsep}{env['PATH']}"
    env["RUN_LOG"] = str(run_log)

    result = _create(target, "sample-tool", skip_venv=False, env=env, kit=kit)

    assert result.returncode == 0, result.stderr
    assert run_log.read_text(encoding="utf-8").splitlines() == ["run", "run"]
    assert (target / "KIT_INSTALLED").is_file()
    assert "post-kit make check passed" in result.stdout


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


def test_rejects_hash_in_target_before_creating_it(tmp_path: Path) -> None:
    _require_git_checkout()
    target = tmp_path / "project#copy"

    result = _create(target, "sample-tool")

    assert result.returncode == 2
    assert "console-script shebangs" in result.stderr
    assert not target.exists()
