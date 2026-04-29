"""Tests for the bundled-content CLI subcommands: lessons, examples, docs.

These tests stand up a synthetic _bundled/ tree inside a temp directory and
monkeypatch _bundle_root() to point at it. That way they don't depend on the
real bundle being present (which it isn't until the package is built and
installed via the wheel)."""

import io
from contextlib import redirect_stdout, redirect_stderr

import pytest

from barebear import cli


@pytest.fixture
def fake_bundle(tmp_path, monkeypatch):
    """Create a minimal _bundled tree under tmp_path and route the CLI to it."""
    root = tmp_path / "_bundled"
    (root / "lessons" / "01-first-llm-call").mkdir(parents=True)
    (root / "lessons" / "01-first-llm-call" / "lesson.md").write_text(
        "# Lesson 1 — First call\n\nbody\n", encoding="utf-8"
    )
    (root / "lessons" / "01-first-llm-call" / "lesson.ipynb").write_text("{}\n", encoding="utf-8")
    (root / "lessons" / "13-capstone").mkdir(parents=True)
    (root / "lessons" / "13-capstone" / "lesson.md").write_text(
        "# Lesson 13 — Capstone project\n", encoding="utf-8"
    )
    (root / "examples" / "research").mkdir(parents=True)
    (root / "examples" / "research" / "run.py").write_text(
        '"""Research example: a worked agent."""\n\nprint("hi")\n', encoding="utf-8"
    )
    (root / "teaching").mkdir(parents=True)
    (root / "teaching" / "spec-mapping.md").write_text(
        "# Exam-spec mapping\n\nbody\n", encoding="utf-8"
    )
    monkeypatch.setattr(cli, "_bundle_root", lambda: root)
    return root


def test_lessons_listing(fake_bundle):
    buf = io.StringIO()
    with redirect_stdout(buf):
        rc = cli.main(["lessons"])
    assert rc == 0
    out = buf.getvalue()
    assert "01-first-llm-call" in out
    assert "Lesson 1 — First call" in out
    assert "13-capstone" in out
    assert "barebear lessons --copy" in out


def test_lessons_copy_all(fake_bundle, tmp_path):
    dst = tmp_path / "classroom"
    buf = io.StringIO()
    with redirect_stdout(buf):
        rc = cli.main(["lessons", "--copy", str(dst)])
    assert rc == 0
    assert (dst / "01-first-llm-call" / "lesson.md").exists()
    assert (dst / "01-first-llm-call" / "lesson.ipynb").exists()
    assert (dst / "13-capstone" / "lesson.md").exists()
    out = buf.getvalue()
    assert "Copied" in out
    assert str(dst) in out


def test_lessons_copy_single(fake_bundle, tmp_path):
    dst = tmp_path / "single"
    rc = cli.main(["lessons", "1", "--copy", str(dst)])
    assert rc == 0
    assert (dst / "01-first-llm-call" / "lesson.md").exists()
    assert not (dst / "13-capstone").exists()


def test_lessons_unknown_number(fake_bundle):
    buf = io.StringIO()
    with redirect_stderr(buf):
        rc = cli.main(["lessons", "99"])
    assert rc == 1
    assert "No lesson 99" in buf.getvalue()


def test_lessons_when_no_bundle(monkeypatch, tmp_path):
    monkeypatch.setattr(cli, "_bundle_root", lambda: tmp_path / "missing")
    buf = io.StringIO()
    with redirect_stderr(buf):
        rc = cli.main(["lessons"])
    assert rc == 1
    assert "No bundled lessons found" in buf.getvalue()


def test_examples_listing(fake_bundle):
    buf = io.StringIO()
    with redirect_stdout(buf):
        rc = cli.main(["examples"])
    assert rc == 0
    out = buf.getvalue()
    assert "research" in out
    assert "barebear examples --copy" in out


def test_examples_copy(fake_bundle, tmp_path):
    dst = tmp_path / "ex"
    rc = cli.main(["examples", "--copy", str(dst)])
    assert rc == 0
    assert (dst / "research" / "run.py").exists()


def test_docs_listing(fake_bundle):
    buf = io.StringIO()
    with redirect_stdout(buf):
        rc = cli.main(["docs"])
    assert rc == 0
    out = buf.getvalue()
    assert "spec-mapping.md" in out
    assert "Exam-spec mapping" in out


def test_docs_when_no_bundle(monkeypatch, tmp_path):
    monkeypatch.setattr(cli, "_bundle_root", lambda: tmp_path / "missing")
    buf = io.StringIO()
    with redirect_stderr(buf):
        rc = cli.main(["docs"])
    assert rc == 1
    assert "No bundled teaching docs" in buf.getvalue()


def test_main_dispatches_each_subcommand(fake_bundle):
    """Smoke-test that each known subcommand resolves to a working handler."""
    for argv in (["lessons"], ["examples"], ["docs"]):
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = cli.main(argv)
        assert rc == 0, f"{argv} returned {rc}"
