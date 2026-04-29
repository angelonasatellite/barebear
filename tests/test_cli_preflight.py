"""Tests for the barebear preflight CLI."""

import io
from contextlib import redirect_stdout

import pytest

from barebear.cli import (
    check_barebear_installed,
    check_openai_sdk_installed,
    check_openrouter_key,
    check_python_version,
    main,
    run_preflight,
)


def test_python_version_check_passes_on_supported_python():
    r = check_python_version()
    assert r.ok is True
    assert "Python" in r.detail


def test_barebear_installed_check_passes():
    r = check_barebear_installed()
    assert r.ok is True
    assert "version" in r.detail.lower()


def test_openai_sdk_check_passes_when_installed():
    r = check_openai_sdk_installed()
    # We have openai installed in dev extras, so this should pass.
    assert r.ok is True


def test_openrouter_key_missing(monkeypatch):
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)
    r = check_openrouter_key()
    assert r.ok is False
    assert "no key" in r.detail.lower()


def test_openrouter_key_wrong_format(monkeypatch):
    monkeypatch.setenv("OPENROUTER_API_KEY", "wrong-format-12345")
    r = check_openrouter_key()
    assert r.ok is False
    assert "sk-or-" in r.detail


def test_openrouter_key_correct_format(monkeypatch):
    monkeypatch.setenv("OPENROUTER_API_KEY", "sk-or-abcdef123456")
    r = check_openrouter_key()
    assert r.ok is True
    assert "sk-or-ab" in r.detail


def test_run_preflight_skip_network_returns_nonzero_on_missing_key(monkeypatch):
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)
    buf = io.StringIO()
    with redirect_stdout(buf):
        rc = run_preflight(skip_network=True)
    assert rc == 1
    out = buf.getvalue()
    assert "OPENROUTER_API_KEY set" in out
    assert "FAIL" in out


def test_run_preflight_skip_network_returns_zero_when_key_present(monkeypatch):
    monkeypatch.setenv("OPENROUTER_API_KEY", "sk-or-abcdef123456")
    buf = io.StringIO()
    with redirect_stdout(buf):
        rc = run_preflight(skip_network=True)
    assert rc == 0
    out = buf.getvalue()
    assert "all checks passed" in out


def test_main_dispatches_preflight(monkeypatch):
    monkeypatch.setenv("OPENROUTER_API_KEY", "sk-or-abcdef123456")
    buf = io.StringIO()
    with redirect_stdout(buf):
        rc = main(["preflight", "--skip-network"])
    assert rc == 0


def test_main_no_subcommand_errors():
    with pytest.raises(SystemExit):
        main([])


def test_check_model_call_handles_construction_failure(monkeypatch):
    """If OPENROUTER_API_KEY is missing, OpenRouterModel raises ValueError;
    the check should report that gracefully, not propagate the exception."""
    from barebear.cli import check_model_call
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)
    r = check_model_call(timeout=1.0)
    assert r.ok is False
    assert "could not construct" in r.detail
