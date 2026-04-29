"""barebear command-line entry point.

Subcommands:

    barebear preflight   — verify the local environment is ready to run
                            lessons (Python version, package install,
                            API key presence, network reachability).
    barebear lessons     — list the bundled course; copy lessons to a
                            working directory.
    barebear examples    — list the bundled worked examples; copy them.
    barebear docs        — list the bundled teaching documents.

Designed for teachers to run before a lesson and for students to copy
the course locally without cloning git.
"""

from __future__ import annotations

import argparse
import os
import shutil
import sys
import time
from dataclasses import dataclass
from pathlib import Path
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


# ---------------------------------------------------------------------------
# Bundled-content access (lessons / examples / docs/teaching ship inside the
# wheel via [tool.hatch.build.targets.wheel.force-include] in pyproject.toml).
# ---------------------------------------------------------------------------

def _bundle_root() -> Path:
    """Root of the bundled teaching content inside the installed package."""
    return Path(__file__).parent / "_bundled"


def _list_dir(path: Path) -> List[Path]:
    if not path.exists():
        return []
    return sorted(p for p in path.iterdir() if not p.name.startswith("."))


def _read_first_line(path: Path, prefix: str = "# ") -> str:
    try:
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.startswith(prefix):
                return line[len(prefix):].strip()
    except OSError:
        pass
    return path.stem


def _copy_tree(src: Path, dst: Path) -> int:
    """Copy a directory tree, returning the number of files copied."""
    count = 0
    for source_path in src.rglob("*"):
        if source_path.is_dir():
            continue
        rel = source_path.relative_to(src)
        target = dst / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_path, target)
        count += 1
    return count


def run_lessons(args: argparse.Namespace) -> int:
    """`barebear lessons` — list and/or copy the bundled course."""
    root = _bundle_root() / "lessons"
    if not root.exists():
        print(
            "No bundled lessons found. This installation of barebear does "
            "not include the course content. Try `pip install --upgrade "
            "barebear`, or read the lessons online at "
            "https://github.com/richey-malhotra/barebear/tree/main/lessons",
            file=sys.stderr,
        )
        return 1

    lesson_dirs = [p for p in _list_dir(root) if p.is_dir()]

    if args.lesson is not None:
        match = [p for p in lesson_dirs if p.name.startswith(f"{args.lesson:02d}-")]
        if not match:
            print(f"No lesson {args.lesson:02d} found.", file=sys.stderr)
            return 1
        lesson_dirs = match

    if args.copy:
        dst = Path(args.copy).expanduser().resolve()
        dst.mkdir(parents=True, exist_ok=True)
        total = 0
        for lesson in lesson_dirs:
            target = dst / lesson.name
            target.mkdir(parents=True, exist_ok=True)
            total += _copy_tree(lesson, target)
        which = (
            f"lesson {args.lesson:02d}" if args.lesson is not None else f"all {len(lesson_dirs)} lessons"
        )
        print(f"Copied {which} ({total} files) to {dst}")
        return 0

    print("The BareBear course — bundled with this install:\n")
    for lesson in lesson_dirs:
        title = _read_first_line(lesson / "lesson.md")
        ipynb = "notebook" if (lesson / "lesson.ipynb").exists() else "—"
        py = "script" if (lesson / "lesson.py").exists() else "—"
        print(f"  {lesson.name}")
        print(f"    {title}")
        print(f"    formats: {ipynb}, {py}")
        print()
    print("To copy the lessons to a working directory:")
    print("  barebear lessons --copy ./my-classroom/")
    print("\nTo copy a single lesson:")
    print("  barebear lessons 1 --copy ./my-classroom/")
    return 0


def run_examples(args: argparse.Namespace) -> int:
    """`barebear examples` — list and/or copy bundled worked examples."""
    root = _bundle_root() / "examples"
    if not root.exists():
        print(
            "No bundled examples found. Read them online at "
            "https://github.com/richey-malhotra/barebear/tree/main/examples",
            file=sys.stderr,
        )
        return 1

    example_dirs = [p for p in _list_dir(root) if p.is_dir()]

    if args.copy:
        dst = Path(args.copy).expanduser().resolve()
        dst.mkdir(parents=True, exist_ok=True)
        total = 0
        for ex in example_dirs:
            target = dst / ex.name
            target.mkdir(parents=True, exist_ok=True)
            total += _copy_tree(ex, target)
        # Also copy the examples README if present
        readme = root / "README.md"
        if readme.exists():
            shutil.copy2(readme, dst / "README.md")
            total += 1
        print(f"Copied {len(example_dirs)} example(s) ({total} files) to {dst}")
        return 0

    print("Worked examples bundled with this install:\n")
    for ex in example_dirs:
        run_py = ex / "run.py"
        first = _read_first_line(run_py, prefix='"""') if run_py.exists() else ex.name
        print(f"  {ex.name}: {first}")
    print("\nTo copy them to a working directory:")
    print("  barebear examples --copy ./my-examples/")
    return 0


def run_docs(args: argparse.Namespace) -> int:
    """`barebear docs` — list bundled teaching documents."""
    root = _bundle_root() / "teaching"
    if not root.exists():
        print(
            "No bundled teaching docs found. Read them online at "
            "https://github.com/richey-malhotra/barebear/tree/main/docs/teaching",
            file=sys.stderr,
        )
        return 1

    docs = sorted(root.glob("*.md"))
    print("Teaching docs bundled with this install:\n")
    for d in docs:
        title = _read_first_line(d)
        print(f"  {d.name}")
        print(f"    {title}")
        print(f"    path: {d}")
        print()
    print("Open any of these in your editor or print them directly.")
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

    lessons = sub.add_parser(
        "lessons",
        help="list or copy the bundled 13-lesson course",
    )
    lessons.add_argument(
        "lesson",
        nargs="?",
        type=int,
        default=None,
        help="show or copy a specific lesson number (1..13)",
    )
    lessons.add_argument(
        "--copy",
        metavar="DIR",
        help="copy lessons to DIR (created if missing)",
    )

    examples = sub.add_parser(
        "examples",
        help="list or copy the bundled worked examples",
    )
    examples.add_argument(
        "--copy",
        metavar="DIR",
        help="copy examples to DIR (created if missing)",
    )

    sub.add_parser(
        "docs",
        help="list bundled teaching documents and their installed paths",
    )

    args = parser.parse_args(argv)

    if args.command == "preflight":
        return run_preflight(skip_network=args.skip_network)
    if args.command == "lessons":
        return run_lessons(args)
    if args.command == "examples":
        return run_examples(args)
    if args.command == "docs":
        return run_docs(args)

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
