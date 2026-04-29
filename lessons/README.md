# 🐻 The BareBear Course

**12 lessons. 12 concepts. Real models. No magic. Read the framework — it's the textbook.**

A free, drop-in course on agentic AI for sixth-form / A-level CS, AP CS, IB
Computer Science, intro university CS, and bootcamps. Every concept that
matters in modern agent design, taught against real LLMs from lesson one.

---

## Who this is for

- **Students** with Python basics (functions, dicts, classes) and no prior LLM
  experience. By the end, you will have built a working multi-agent system from
  first principles.
- **Teachers** looking for a 12-week module that drops into an existing CS
  syllabus. Each lesson is self-contained, has clear learning outcomes, and
  ships with a runnable notebook plus a written discussion.
- **Engineers** who want to understand what an "agent" actually is without
  reading 50,000 lines of framework code. The whole framework is ~1,500 lines.
  Open it. It's the textbook.

## The syllabus

Every lesson number below links straight to a Colab-runnable notebook. The
parallel `lesson.py` script for lessons 7–12 is in the same folder.

| Lesson  | Concept             | What you'll build                                                       |
|---------|---------------------|-------------------------------------------------------------------------|
| [**01**][l01] | What an LLM is      | A single chat-completion call. See tokens go in and out.                |
| [**02**][l02] | The agent loop      | A one-tool agent. Watch perceive → think → act → observe.               |
| [**03**][l03] | Tool design         | A multi-tool agent. Schemas, descriptions, when the model picks each.   |
| [**04**][l04] | State & memory      | Short-term (messages) vs long-term (`State` dict). Persist across runs. |
| [**05**][l05] | Budgets             | Add a runaway-loop bug; watch the budget save you.                      |
| [**06**][l06] | Policy & guardrails | Block a tool, classify side-effects, declare risk.                      |
| [**07**][l07] | Checkpoints         | An email-send agent that pauses for human approval.                     |
| [**08**][l08] | Planning            | `bear.plan()` before `bear.run()`. When each is the right move.         |
| [**09**][l09] | Reflection          | Self-critique loop with `Reflect` — agent reviews its own work.         |
| [**10**][l10] | Multi-agent         | A Bear that hires another Bear. Multi-agent in under 40 lines.          |
| [**11**][l11] | Evaluation          | Read a `Report`. Write tests for an agent.                              |
| [**12**][l12] | Honest uncertainty  | Make the agent flag what it does not know.                              |

[l01]: https://colab.research.google.com/github/richey-malhotra/barebear/blob/v0.2.2/lessons/01-first-llm-call/lesson.ipynb
[l02]: https://colab.research.google.com/github/richey-malhotra/barebear/blob/v0.2.2/lessons/02-the-agent-loop/lesson.ipynb
[l03]: https://colab.research.google.com/github/richey-malhotra/barebear/blob/v0.2.2/lessons/03-tool-design/lesson.ipynb
[l04]: https://colab.research.google.com/github/richey-malhotra/barebear/blob/v0.2.2/lessons/04-state-and-memory/lesson.ipynb
[l05]: https://colab.research.google.com/github/richey-malhotra/barebear/blob/v0.2.2/lessons/05-budgets/lesson.ipynb
[l06]: https://colab.research.google.com/github/richey-malhotra/barebear/blob/v0.2.2/lessons/06-policy-and-guardrails/lesson.ipynb
[l07]: https://colab.research.google.com/github/richey-malhotra/barebear/blob/v0.2.2/lessons/07-checkpoints/lesson.ipynb
[l08]: https://colab.research.google.com/github/richey-malhotra/barebear/blob/v0.2.2/lessons/08-planning/lesson.ipynb
[l09]: https://colab.research.google.com/github/richey-malhotra/barebear/blob/v0.2.2/lessons/09-reflection/lesson.ipynb
[l10]: https://colab.research.google.com/github/richey-malhotra/barebear/blob/v0.2.2/lessons/10-multi-agent/lesson.ipynb
[l11]: https://colab.research.google.com/github/richey-malhotra/barebear/blob/v0.2.2/lessons/11-evaluation/lesson.ipynb
[l12]: https://colab.research.google.com/github/richey-malhotra/barebear/blob/v0.2.2/lessons/12-honest-uncertainty/lesson.ipynb

All 12 lessons ship as Jupyter notebooks. Lessons 7–12 also ship as plain
Python scripts (`lesson.py` next to each `lesson.ipynb`) so students can
compare notebook prototyping with production-style code.

## How to use this course

### As a student

1. Open Lesson 1 in Colab — no setup, no API keys until you need one.
2. Work through the lessons in order. Each one builds on the last.
3. Do the exercise at the end of every lesson before moving on.

### As a teacher

1. Read [`docs/teaching/instructor-guide.md`](../docs/teaching/instructor-guide.md)
   for classroom setup, model recommendations, and pacing notes.
2. The 12 lessons map to a 12-week module (one lesson per week) or a 6-week
   intensive (two lessons per week).
3. Every lesson has explicit **Learning outcomes** so you can drop it into a
   scheme of work without rewriting.

## Setup (choose one)

### OpenRouter (recommended, no install)

```bash
pip install barebear
export OPENROUTER_API_KEY=sk-or-...   # free tier — get a key at https://openrouter.ai
```

If a free-tier model rotates off and a lesson cell errors with "model not available",
pin a different one with one shell export — every lesson respects it:

```bash
export BAREBEAR_MODEL=meta-llama/llama-3.2-3b-instruct:free
```

### Ollama (offline, local)

Install Ollama from <https://ollama.com>, then:

```bash
pip install barebear
ollama pull qwen2.5:3b
ollama serve
```

Every lesson notebook accepts both backends. Pick once at the top of the
notebook and forget about it.

## Prerequisites

- Python 3.9+
- Functions, dicts, lists, classes
- No prior LLM, ML, or AI experience required

## Licence and use in teaching

MIT. Use it in your classroom, edit the notebooks, fork the curriculum, ship
your own variant. If you do, [open an issue](https://github.com/richey-malhotra/barebear/issues)
or [star the repo](https://github.com/richey-malhotra/barebear) so others can
find it. If you teach a course with this, we'd love to hear about it.
