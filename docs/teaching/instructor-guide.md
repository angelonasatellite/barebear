# Instructor guide

This is a 12-lesson module on agentic AI, designed for sixth-form / A-level CS,
AP CS, IB Computer Science, intro university CS, and bootcamps. It is free to
use, free to adapt, and built to drop into an existing scheme of work without
rewriting.

## At a glance

- **Length:** 12 lessons. Pace one per week (12-week module) or two per week
  (6-week intensive).
- **Prerequisites:** Python basics — functions, dicts, lists, classes. No prior
  LLM, ML, or AI experience required.
- **Cost:** Free. Students use OpenRouter's free tier or local Ollama. No card
  required.
- **Format:** Each lesson ships as a Jupyter notebook plus a written narrative
  (`lesson.md`). Lessons 7–12 also ship as plain Python scripts.
- **Licence:** MIT. Adapt freely. We'd love to know if you teach with it.

## Recommended classroom setup

### Option A — OpenRouter (recommended)

- Each student creates a free OpenRouter account at <https://openrouter.ai>.
  GitHub or Google sign-in. No payment method required for the free tier.
- Students copy their key and paste it into the notebook when prompted. In
  Colab, the key is stored as a session secret.
- **Pros:** zero install, fast responses, real frontier-class models.
- **Cons:** requires internet; free-tier models can rotate (the lesson
  notebooks pin a default with a documented fallback).

### Option B — Ollama (offline)

- Pre-install Ollama on lab machines from <https://ollama.com>.
- Pull a small instruction-tuned model: `ollama pull qwen2.5:3b` (1.9 GB).
- Run `ollama serve` on each machine.
- **Pros:** fully offline; school IT departments tend to be more comfortable
  with local-only.
- **Cons:** small models tool-call less reliably than frontier hosted models;
  expect the occasional unresponsive lesson.

### Option C — Hybrid

Demo with OpenRouter on a projector, students experiment locally with Ollama.
Best of both, but doubles your setup overhead.

## Pacing notes

| Lesson | Difficulty | Notes |
|--------|------------|-------|
| 1 — First LLM call | Light | Use this to test the lab setup. If Lesson 1 doesn't run end-to-end for everyone, the rest is wasted. Allow extra time. |
| 2 — Agent loop | Light | The "aha" moment. Most students get the four-move loop after one trace. |
| 3 — Tool design | Medium | Spend time on tool descriptions; bad descriptions are the most common cause of agent misbehaviour. |
| 4 — State and memory | Light | Easy if Lessons 2–3 stuck. |
| 5 — Budgets | Medium | The runaway-loop demo lands hard if you set up the trap correctly. Don't skip it. |
| 6 — Policy | Medium | Pair this with a discussion of real-world incidents (autonomous email sends, runaway purchases). |
| 7 — Checkpoints | Heavier | First lesson with persistence between runs. Some students need help with the resume step. |
| 8 — Planning | Light | Pair this with a debate: when is plan-then-execute the right move? |
| 9 — Reflection | Light | Most students enjoy the recursive critique experiment. |
| 10 — Multi-agent | Heavier | Conceptually clean, mechanically subtle. Show `bear.as_tool()` source — it's tiny. |
| 11 — Evaluation | Medium | This is where students start writing tests over agent behaviour. Real engineering practice begins here. |
| 12 — Uncertainty | Light | Good capstone discussion lesson. |

## Common student pitfalls

- **Forgetting to set the API key.** Lesson 1 always seems to surface this.
  Make a slide showing exactly where to paste it.
- **Confusing the message list with `State`.** They look similar; they aren't.
  Lesson 4 hammers this home, but expect questions in Lessons 5–7.
- **Expecting the model to follow instructions perfectly.** It won't. That's
  the whole reason `Policy` and `Budget` exist. When a student says "but the
  model said it wouldn't…" — that's the Lesson 6 conversation in disguise.
- **Free-tier model rate limits.** During large class runs, you may hit them.
  Stagger student starts, or pre-cache responses for the demo.
- **Free-tier model rotation.** OpenRouter occasionally retires free models.
  If a lesson cell errors with "model not available", students can swap by
  exporting `BAREBEAR_MODEL=...` to any other `*:free` model at
  <https://openrouter.ai/models> — every lesson notebook reads the env var
  with no code change.

## Suggested assessments

- **Project (50%)** — a working agent solving a chosen real-world task,
  shipping with: tools, a `Policy`, a `Report` test suite, and a written
  reflection on its limitations.
- **Code review (25%)** — students review each other's agent design with
  attention to tool descriptions, policy choices, and budget settings.
- **Written piece (25%)** — short essay on a chosen topic: "the case for
  human-in-the-loop", "why the agent loop is just `while True:`", "what
  the framework chose not to include and why."

## Adapting the curriculum

The lessons are intentionally modular. Drop or reorder freely:

- **6-week intensive:** lessons 1–6 cover everything single-agent.
  Lessons 7–12 are an optional deepening.
- **3-week sprint:** lessons 1, 2, 5, 6, 11. The "minimum viable agent
  literacy" subset.
- **University intro AI module:** insert a lesson on token-level mechanics
  between Lesson 1 and Lesson 2 if your course requires it.

If you write your own lesson, please consider opening a PR — see
[CONTRIBUTING.md](../../CONTRIBUTING.md). New lessons are warmly welcomed.

## Telling us you used it

If you teach a course or club with BareBear:

- [Star the repo](https://github.com/richey-malhotra/barebear) so other
  teachers can find it.
- Add a comment on the pinned [Teaching with barebear](https://github.com/richey-malhotra/barebear/issues/1)
  thread. We'd love to know what worked, what didn't, and what you wish
  was different — short or long, all welcome.
