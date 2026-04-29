# Lesson 13 — Capstone project

> **Learning outcomes**
> - Design and build a complete agent solving a real problem of your
>   choosing.
> - Apply policy, budgets, checkpoints, reflection, or multi-agent
>   composition where they fit.
> - Document and demonstrate the agent's behaviour with a `Report`.

**Time:** allow 2–4 lessons (4–8 hours of student time). The first
half is design; the second half is build, test, and write-up.

This isn't a notebook. It's a project. By Lesson 12 you've seen every
primitive in the framework. The capstone is where you combine them on a
problem you actually care about.

## What you build

A working agent that solves one specific, scoped problem. It must:

- Use **at least three tools** that you defined.
- Be wrapped in a **`Policy`** with at least one budget and one
  policy-level constraint that's actually enforced (a `blocked_tool` or
  `require_approval_for`).
- Produce a **`Report`** that demonstrates the agent did what you
  intended.
- Be small enough that you can explain every line to a classmate in
  five minutes.

You don't need to invent something nobody has done before. You need to
build something *you* understand end-to-end.

## Five starter ideas

If you're stuck for a topic, pick one of these. They've been chosen
because they fit comfortably in a sixth-form scope and use real
tools.

### 1. Homework helper

An agent that takes a topic from a school subject (history, biology,
literature) and helps a student revise. Tools: `lookup_topic`,
`generate_quiz`, `mark_answer`, `give_hint`. Policy: `require_approval_for=["mark_answer"]`
so a human checks before the agent confidently asserts a wrong answer.
Ship the report so a teacher can see exactly what was asked and what
the agent said.

### 2. Class librarian

An agent that helps students borrow and return library books from a
small JSON-based "library" you create. Tools: `search_books`,
`reserve_book`, `confirm_return`, `report_lost`. Policy: `report_lost`
requires approval; budget: `max_steps=8`. The exercise is in modelling
real-world library workflow as agent tools.

### 3. Plant-care planner

An agent that takes the names of plants a student owns and produces a
weekly care schedule. Tools: `lookup_plant_needs`, `read_user_calendar`,
`schedule_watering`, `add_reminder`. Use `State` to track which plants
are registered. Policy: external side effects (writing to the calendar)
require approval.

### 4. Code-review buddy

An agent that takes a small Python file (one a student wrote earlier
in the year) and produces a review with concrete suggestions. Tools:
`read_file`, `lint_check`, `propose_fix`, `apply_fix`. Critically:
`apply_fix` is policy-blocked — the agent can only *propose*. This
demonstrates side-effect staging from Lesson 6 in production.

### 5. Revision-schedule reflector

A multi-agent system. Agent 1 (researcher) takes the student's exam
dates and subjects and produces a draft revision schedule. Agent 2
(critic) uses `Reflect` to point out gaps. Agent 3 (writer) produces
the final schedule. Use `bear.as_tool()` (Lesson 10) to wire them up.

You can adapt any of these, or invent your own. Run the idea past your
teacher before you spend more than 30 minutes on it.

## Project requirements

Your submission must include:

1. **A working agent** in a single Python file or notebook. Runs
   end-to-end against OpenRouter (or Ollama) without errors.
2. **A short README** (about 300 words) explaining what the agent does,
   why you picked the tools you picked, and the trade-offs you faced.
3. **A `Report` from one successful run**, saved as JSON
   (`report.to_json()`). This is your evidence of behaviour.
4. **A `Report` from one *failed* or *paused* run** — where the agent
   hit a budget, was blocked by policy, or paused for a checkpoint.
   Failure modes are part of the design; show you've tested them.
5. **Two behavioural tests** in pytest (Lesson 11 style). Tests that
   pass should pass; tests that should fail should fail. Include the
   pytest output.

This is the same artefact set a software engineer would produce for a
production agent, scaled to a sixth-form project.

## Marking rubric

See [`rubric.md`](rubric.md) for the suggested grading criteria. The
short version:

| Aspect | Points |
|---|---|
| Functionality (the agent does what the README says) | 25 |
| Tool design (clear schemas, sensible names, descriptions) | 15 |
| Policy and safety (right constraints chosen and enforced) | 20 |
| Reports and tests (behavioural evidence, not just text output) | 15 |
| Honest uncertainty (the agent flags what it doesn't know) | 10 |
| Write-up (clarity, trade-offs surfaced, design decisions justified) | 15 |
| **Total** | **100** |

## What we're looking for

- **Right-sized scope.** A small agent done well beats an ambitious one
  that doesn't run. If your README says "the agent does five things",
  every one of those five things must work.
- **Deliberate policy choices.** A policy with `max_steps=10` and
  nothing else is an admission you didn't think about safety. Pick at
  least one constraint that *says something* about your agent's
  behaviour.
- **Reports that prove what you claim.** Don't tell us your agent
  does X. Show us a report where it did X.
- **Honesty about limitations.** The strongest write-ups are the ones
  that say "I tried Y, it didn't work, I switched to Z because..."
  Defending a design that worked-against-the-odds beats faking
  inevitability.

## A worked timeline

For a typical 2-week (4-lesson) capstone:

| Session | Activity |
|---|---|
| Lesson 13a | Pick an idea, sketch the tools and policy on paper, get teacher sign-off. No code. |
| Lesson 13b | Implement the tools and a minimal `Bear` configuration. Get one happy-path run working end-to-end. |
| Lesson 13c | Write the policy, exercise it (force a budget exhaustion or a policy block), capture the report. |
| Lesson 13d | Write the README, the two pytest assertions, polish, submit. |

If your students have more or less time, scale to fit — but the four
phases (design, happy path, edge cases, write-up) are the right shape.

## What's next

You've finished the course. The next 12 lessons are the ones you
write yourself, on your own projects, in your own life. The framework
is yours. Open the source. Modify it. Break it. If you fix something
or add a lesson others would benefit from, [contributions are welcome](../../CONTRIBUTING.md).

[Back to the syllabus →](../README.md)
