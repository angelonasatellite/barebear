"""barebear command-line entry point.

Currently exposes one subcommand:

    barebear preflight   — checks the local environment is ready to run
                            lessons (Python version, package install,
                            API key presence, network reachability,
                            chosen model responsiveness).

Designed for teachers to run before a lesson and for students to run
when something feels off.
"""

from __future__ import annotations

import argparse
import os
import sys
import time
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class CheckResult:
    name: str
    ok: bool
    detail: str

    def render(self) -> str:
        mark = "PASS" if self.ok else "FAIL"
        return f"  [{mark}] {self.name}: {self.detail}"


def check_python_version() -> CheckResult:
    major, minor = sys.version_info[:2]
    if (major, minor) >= (3, 9):
        return CheckResult(
            "python version",
            True,
            f"Python {major}.{minor} (>= 3.9 required)",
        )
    return CheckResult(
        "python version",
        False,
        f"Python {major}.{minor} is too old (need >= 3.9). "
        f"Update Python via python.org or your school's IT department.",
    )


def check_barebear_installed() -> CheckResult:
    try:
        import barebear  # noqa: F401
        version = getattr(barebear, "__version__", "unknown")
        return CheckResult("barebear installed", True, f"version {version}")
    except ImportError:
        return CheckResult(
            "barebear installed",
            False,
            "barebear is not importable. Try: pip install --upgrade barebear",
        )


def check_openai_sdk_installed() -> CheckResult:
    try:
        import openai  # noqa: F401
        return CheckResult(
            "openai SDK installed",
            True,
            "the OpenAI Python client is available",
        )
    except ImportError:
        return CheckResult(
            "openai SDK installed",
            False,
            "openai is not installed. Try: pip install \"barebear[openai]\"",
        )


def check_openrouter_key() -> CheckResult:
    key = os.environ.get("OPENROUTER_API_KEY", "").strip()
    if not key:
        return CheckResult(
            "OPENROUTER_API_KEY set",
            False,
            "no key in environment. Set it with: "
            "export OPENROUTER_API_KEY=sk-or-... (free key at openrouter.ai)",
        )
    if not key.startswith("sk-or-"):
        return CheckResult(
            "OPENROUTER_API_KEY format",
            False,
            "the key doesn't start with 'sk-or-'. Re-copy from openrouter.ai.",
        )
    masked = key[:8] + "..." + key[-4:] if len(key) > 12 else "set"
    return CheckResult(
        "OPENROUTER_API_KEY set",
        True,
        f"key present ({masked})",
    )


def check_model_call(timeout: float = 10.0) -> CheckResult:
    """Issue one minimal chat completion to verify the chosen model works."""
    try:
        from barebear import OpenRouterModel
    except ImportError as exc:
        return CheckResult(
            "model reachable",
            False,
            f"could not import OpenRouterModel: {exc}",
        )
    try:
        m = OpenRouterModel(timeout=timeout)
    except Exception as exc:
        return CheckResult(
            "model reachable",
            False,
            f"could not construct OpenRouterModel: {exc}",
        )
    model_name = m._model
    start = time.monotonic()
    try:
        response = m.complete(
            messages=[
                {"role": "user", "content": "Reply with exactly: OK"},
            ],
        )
    except Exception as exc:
        return CheckResult(
            "model reachable",
            False,
            f"call to '{model_name}' failed: {exc}. "
            f"Try setting BAREBEAR_MODEL to a different *:free model "
            f"from openrouter.ai/models.",
        )
    elapsed = time.monotonic() - start
    content = (response.content or "").strip()
    if not content:
        return CheckResult(
            "model reachable",
            False,
            f"'{model_name}' returned an empty response in {elapsed:.1f}s. "
            f"Try a different model.",
        )
    return CheckResult(
        "model reachable",
        True,
        f"'{model_name}' responded in {elapsed:.1f}s",
    )


def run_preflight(skip_network: bool = False) -> int:
    """Run all preflight checks. Returns a process exit code (0 = OK)."""
    print("barebear preflight — verifying lesson environment\n")

    checks: List[CheckResult] = [
        check_python_version(),
        check_barebear_installed(),
        check_openai_sdk_installed(),
        check_openrouter_key(),
    ]

    if not skip_network and all(c.ok for c in checks):
        checks.append(check_model_call())

    for c in checks:
        print(c.render())

    print()
    failures = [c for c in checks if not c.ok]
    if failures:
        print(f"{len(failures)} check(s) failed. Fix the items marked FAIL "
              "above before running a lesson.\n")
        return 1
    print("all checks passed. You're ready to run lessons.\n")
    return 0


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        prog="barebear",
        description="barebear — agent framework command line",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    preflight = sub.add_parser(
        "preflight",
        help="verify the local environment is ready to run lessons",
    )
    preflight.add_argument(
        "--skip-network",
        action="store_true",
        help="skip the live model-call check (offline preflight)",
    )

    args = parser.parse_args(argv)

    if args.command == "preflight":
        return run_preflight(skip_network=args.skip_network)

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
