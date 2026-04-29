# Contributing to BareBear

Thanks for considering a contribution. BareBear is small by design, and we'd like to keep it that way.

## Setup

```bash
git clone https://github.com/richey-malhotra/barebear.git
cd barebear
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Running tests

```bash
PYTHONPATH=src pytest
```

All 97 tests should pass. If you're adding a feature, add tests for it.

To run with coverage:

```bash
PYTHONPATH=src pytest --cov=barebear --cov-report=term-missing
```

## Code style

We use [ruff](https://docs.astral.sh/ruff/) for linting and formatting.

```bash
ruff check src/ tests/
ruff format src/ tests/
```

Line length is 100. Target Python version is 3.9.

## Submitting a PR

1. Fork the repo and create a branch from `main`.
2. Make your changes. Keep them focused — one PR, one concern.
3. Add or update tests to cover your changes.
4. Run `ruff check` and `ruff format`. Fix any issues.
5. Run the full test suite. Make sure everything passes.
6. Write a clear PR description: what you changed and why.

### What we're looking for

- Bug fixes with a test that reproduces the bug.
- New model adapters (local models, niche providers, etc.).
- Documentation improvements.
- New examples that show real use cases.
- **Lesson contributions.** If you teach with BareBear and have built a
  lesson, exercise, or worked example you'd like to share, open a PR
  against `lessons/`. See [`lessons/README.md`](lessons/README.md) for
  the existing structure. New lessons must include a `lesson.md`
  narrative; a runnable notebook is encouraged. Pace, tone, and
  difficulty should match the surrounding lessons.

### What we'll probably say no to

- Major new abstractions or "framework features" without prior discussion.
- Dependencies beyond the standard library for the core package.
- Changes that break the existing API without strong justification.

If you're unsure whether something fits, open an issue first. We'd rather discuss the idea before you write the code.

## Reporting issues

When filing a bug report, include:

- Python version
- BareBear version (`python -c "import barebear; print(barebear.__version__)"`)
- Minimal reproduction code
- Expected vs. actual behaviour
- Full traceback if applicable

For feature requests, describe the use case. "I want X because Y" is more useful than "please add X."

## Code of conduct

Be kind, be direct, be helpful. We don't have a formal CoC document yet, but the standard applies: no harassment, no discrimination, no bad faith. Treat others the way you'd want to be treated in a code review.

## License

By contributing, you agree that your contributions will be licensed under the [MIT License](LICENSE).
