# Changelog

All notable changes to BareBear will be documented in this file.

## 0.4.1 (2026-04-29)

Documentation-only patch. Fixes broken in-repo links on the PyPI
project page.

### Fixed

- README's links to teacher resources, syllabus, instructor guide,
  manifesto, architecture, contributing guide, licence, and source
  tree were relative paths. Relative paths render correctly on GitHub
  but break on PyPI's project page (PyPI doesn't have access to the
  repo's directory tree). All in-repo links converted to absolute
  `https://github.com/richey-malhotra/barebear/blob/v0.4.1/...` URLs
  pinned to the matching tag.
- Image and Colab refs bumped from `v0.4.0` to `v0.4.1`.

No code changes; 128 tests still pass.

## 0.4.0 (2026-04-29)

A "classroom in a box" release. The wheel now ships the full course —
13 lessons (notebooks + scripts), 4 worked examples, and the 5
teaching documents — bundled inside the package itself. A teacher who
runs `pip install barebear` no longer needs to clone git to access any
of the curriculum.

### Added

- **Lesson, example, and teaching-doc bundling.** The wheel includes
  `barebear/_bundled/lessons/`, `_bundled/examples/`, and
  `_bundled/teaching/` via `[tool.hatch.build.targets.wheel.force-include]`.
  Wheel grew from 31 KB to ~123 KB; sdist from 27 KB to ~79 KB.
- **`barebear lessons`** — list the bundled syllabus with title and
  available formats (notebook / script).
- **`barebear lessons N`** — show details for one lesson.
- **`barebear lessons --copy DIR`** — copy all lessons (or a specific
  one with `barebear lessons N --copy DIR`) to a working directory.
  Teachers can spin up a classroom workspace in one command without
  cloning git.
- **`barebear examples`** and **`barebear examples --copy DIR`** —
  same pattern for the four worked examples.
- **`barebear docs`** — list the bundled teaching docs and the absolute
  paths inside the install where they live, so a teacher can open them
  in their editor or pipe them to `cat`.
- 10 new tests covering the bundled-content commands, using a fake
  bundle directory so the tests don't depend on packaging. 128 tests
  passing total.

### Changed

- pyproject `[tool.hatch.build.targets.sdist]` now includes `lessons/`,
  `examples/`, and `docs/teaching/` alongside the source. Carousel and
  marketing assets remain excluded.

### Notes

- Public Python API unchanged from 0.3.x. Adding new CLI subcommands is
  additive; the `preflight` command still works as before.

## 0.3.0 (2026-04-29)

A teacher-experience release. The framework is unchanged; everything
around it is.

### Added

- **`barebear preflight` CLI** — verifies Python version, package
  install, OpenRouter key presence and format, and (optionally) live
  model reachability. New `[project.scripts]` entry installs `barebear`
  on the user's PATH. `--skip-network` runs offline. 11 new tests, 118
  passing total.
- **Lesson 13 — capstone project pack** at `lessons/13-capstone/` with
  a project brief (5 starter ideas, requirements, suggested timeline)
  and a 100-point marking rubric across six aspects.
- **Per-lesson Pace and Homework sections** on every lesson 02–12.
  Each lesson.md now has a one-line time estimate and a concrete
  between-lessons exercise — homework prompts require students to
  actually run barebear (build agents, capture reports, write Policy
  instantiations), not paper-only reflection.
- **Lesson 1 ends with a "preview through barebear" pair of cells.**
  After the raw OpenAI-SDK call that introduces the LLM, students see
  the same call routed through `OpenRouterModel().complete(...)` —
  closing the loop between *"what is an LLM"* and *"barebear is that
  call plus a loop"*.
- **`docs/teaching/spec-mapping.md`** — maps every lesson onto AQA
  A-level, OCR A-level, OCR GCSE, AP CSP, AP CS A, and IB CS specs.
- **`docs/teaching/teacher-quickstart.md`** — onboarding for CS
  teachers who haven't installed a Python framework before. Browser-
  only path, plain English, no terminal required.
- **`docs/teaching/student-misconceptions.md`** — plain-English
  re-framings of the ten questions students will actually ask
  ("Is the AI thinking?", "Why different answers each time?", etc.)
  with one-liners for use in class.
- **`docs/teaching/it-brief.md`** — one-page summary teachers can
  email to their school IT department. Endpoints, data flows, licence,
  cost, plus a copy-paste email template.

### Changed

- **`lessons/README.md`** updated: capstone added to the syllabus,
  teacher-supporting docs surfaced explicitly.
- **Main README** updated: teacher resources block now lists every
  supporting document, and mentions the `barebear preflight` command.

### Notes

- No breaking changes; the framework public API is identical to 0.2.2.
- The new CLI surface justifies a minor bump (0.2.x → 0.3.0) under
  semver: it's additive, but it's a new public entry point installed
  on the user's PATH.

## 0.2.2 (2026-04-29)

Two small refinements driven by feedback after the 0.2.1 launch.

### Changed

- **`Task.system_prompt` now fully replaces the system message.** Previously
  setting `system_prompt` swapped the persona block but the framework still
  appended its policy text, tool list, state, and instructions to the system
  message. As of 0.2.2 the user's `system_prompt` is the entire system role.
  Tool schemas continue to reach the model through the `tools=` parameter on
  `model.complete()`, so tool calling still works as before. This makes
  `bear.plan()` honour custom personas correctly (Lesson 8's exercise).
- **`OpenRouterModel` and `OllamaModel` now respect `BAREBEAR_MODEL` env var.**
  Resolution order: explicit `model=` argument → `BAREBEAR_MODEL` env →
  class-level `DEFAULT_MODEL`. Lets every lesson notebook switch backend with
  one shell-level export when a free-tier model rotates.

### Added

- `OpenRouterModel.DEFAULT_MODEL` and `OllamaModel.DEFAULT_MODEL` are now
  documented class attributes (still `stepfun/step-3.5-flash:free` and
  `qwen2.5:3b` respectively).

### Tests

- 10 new tests; 107 passing total.

### Note for users

The `system_prompt` change is technically a behaviour change. Existing code
that *both* set a custom `system_prompt` *and* relied on the framework's
appended tool list / policy / state in the system message will see those
sections disappear. The model still receives tool schemas via the `tools=`
parameter, so tool calling is unaffected. To restore the previous behaviour,
omit `system_prompt` (or include the policy / tool descriptions in the
custom prompt yourself).

## 0.2.1 (2026-04-29)

Packaging hygiene only. No code changes.

### Fixed

- The 0.2.0 sdist accidentally bundled unrelated repo content
  (large media files plus a leftover root `demo.gif`), inflating the
  source distribution. The wheel was always clean.
- Added explicit `[tool.hatch.build.targets.sdist]` include list so the
  sdist now contains only `src/`, `pyproject.toml`, `README.md`, `LICENSE`,
  and `CHANGELOG.md`.
- Removed the leftover root `demo.gif`; the canonical asset lives at
  `assets/demo.gif`.

0.2.0 has been yanked. Use 0.2.1.

## 0.2.0 (2026-04-29)

Pivot release. BareBear is now positioned as the free agentic AI course —
a 12-lesson curriculum that uses the framework as its textbook. The primitives
are unchanged; the audience and the surface around them are.

### Added

- **`OllamaModel`** adapter for local Ollama servers (OpenAI-compatible endpoint
  at `http://localhost:11434/v1`). Default model: `qwen2.5:3b`.
- **`Task.system_prompt`** — first-class field for overriding the agent persona
  per task. Backwards compatible: when unset, the framework default applies.
- **`Bear.run(task, trace=True)`** — streams a learner-friendly narration of
  every loop turn to stdout (or a custom stream). For lesson notebooks and
  live debugging.
- **`Reflect`** helper — three small methods (`critique`, `revise`, `run`) for
  self-critique loops. Surfaces the reflection pattern as a named primitive.
- **`Bear.as_tool(name, description)`** — wraps a Bear so another Bear can call
  it as a Tool. Multi-agent in one line.
- **`lessons/`** — a 12-lesson curriculum: full Lesson 1 (notebook, Colab
  badge, written narrative) plus written narratives for lessons 2–12.
  Notebooks for 2–6 to follow; notebooks and scripts for 7–12 after that.
- **`docs/teaching/instructor-guide.md`** — classroom setup, per-lesson pacing,
  pitfalls, assessments, and 3-/6-/12-week curriculum subsets.
- **PyPI download badges** (pepy.tech, total + monthly) and GitHub stars badge
  in the README.
- `Topic :: Education` and `Intended Audience :: Education` PyPI classifiers.

### Changed

- **`MockModel` removed from the public API.** It now lives at
  `barebear.testing.FakeModel` and is used only by the framework's own tests.
  Lessons and examples always run against a real model.
- All examples now default to **OpenRouter** and accept
  `--provider {openrouter,ollama}`. The `--live` flag is gone — every run is
  live.
- README, manifesto, and quickstart rewritten for the educational positioning.
  Lead with the curriculum, the three-door first-60-seconds layout, the Colab
  badge for Lesson 1.
- Project description and keywords updated for educational discoverability.
- Unused `anthropic` optional dependency removed (no AnthropicModel ships).
- `docs/architecture.md` adapter table updated: `MockModel` and the planned
  `AnthropicModel` are gone; `OpenRouterModel`, `OllamaModel`, and the
  internal `barebear.testing.FakeModel` are in.

### Breaking

- `from barebear import MockModel` → `from barebear.testing import FakeModel`.
- Examples: `--live` flag replaced by `--provider {openrouter,ollama}`.
- `Task.to_dict()` now includes a `system_prompt` key (always present, may
  be `None`).

## 0.1.1 (2026-03-16)

### Added

- OpenRouter quickstart guide in docs
- OpenRouter model mentioned in README quickstart

### Changed

- New bear mascot logo
- README images now use release-safe absolute URLs so the PyPI project page renders correctly
- GitHub and PyPI package metadata are aligned on version `0.1.1`

## 0.1.0 (2026-03-15)

First public release.

### Added

- Core primitives: Bear, Task, State, Tool, Policy, Checkpoint, Report
- Model adapters: OpenAI, OpenRouter, Mock
- Policy-first tool execution with pre-call enforcement
- Budget tracking (steps, tool calls, tokens, cost)
- Checkpoint/approval system for high-risk actions
- Side-effect declarations on tools (`none`, `internal`, `external`)
- Run receipts with full step traces, assumptions, and uncertainties
- Honest uncertainty tracking with automatic extraction from model responses
- Tool schema introspection from Python type annotations
- Configurable timeouts on model adapters
- 4 runnable examples: research assistant, email approval, file patcher, ticket triage
- 86 passing tests, zero pyright strict-mode errors
