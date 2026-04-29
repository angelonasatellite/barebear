# The BareBear Manifesto

Most agent frameworks optimise for demos. We optimise for understanding.

---

In 2026, every CS department on earth is scrambling to teach AI, and the
curriculum doesn't yet exist. Teachers are improvising slide decks the night
before. Students are reading 50,000 lines of magic, getting confused, and
giving up — or worse, *not* getting confused, and shipping things they don't
understand.

BareBear is a small Python framework. It is also a course. The two are the
same thing on purpose: the framework is small enough that **a sixth-form CS
student can read every line of it in one sitting** and end up understanding
what an "agent" actually is. No magic, no orchestration theatre, no hidden
state.

Seven beliefs hold it together.

**1. Tools are permissions, not features.**
A tool that can send email is not the same as a tool that can read a file.
The framework should know the difference and enforce it before execution,
not after the damage is done.

**2. State must be visible.**
If you can't inspect the agent's state at any point in a run, you can't
debug it, audit it, or trust it. Hidden memory is technical debt with
compound interest.

**3. Autonomy needs bounds.**
An agent without limits is a `while True:` loop with a credit card. Step
limits, token budgets, cost caps, and approval gates aren't restrictions —
they're the reason you can deploy with confidence.

**4. Every run is a receipt.**
When something goes wrong (it will), you need to know exactly what happened:
which tools were called, in what order, with what arguments, at what cost,
and whether any assumptions were made. Reports aren't a nice-to-have. They
are the product.

**5. Uncertainty is data.**
"I don't know" is more valuable than a confident hallucination. The
framework should track what it's guessing, what information is missing, and
what it can't verify. Epistemic honesty isn't a feature — it's a
responsibility.

**6. One bear first.**
Don't start with a multi-agent system. Start with one agent that does one
thing well, with clear policy and traceable behaviour. Add complexity only
when you've proven the simple version isn't enough. Most of the time, it is.

**7. Read the framework. Don't just import it.**
A framework you can't read is a framework you can't reason about. We have
deliberately kept BareBear small enough to fit in a student's head — about
1,500 lines of Python, no clever metaprogramming, no inheritance trees, no
DSLs. If you can read Python, you can read BareBear. Open it. It's the
textbook.

---

## What this means in practice

- Every tool declares its risk level and side effects.
- Policy is checked before every tool execution.
- Runs have budgets. When the budget runs out, the run stops.
- High-risk actions create checkpoints. Humans approve or reject.
- Reports capture steps, costs, tokens, assumptions, and uncertainties.
- State is a dictionary. You can snapshot it, diff it, serialise it.
- The agent tells you what it doesn't know.
- Lessons run against real LLMs from day one. No fake models in the public
  surface — students learn against the real thing or not at all.

### What this doesn't mean

- It doesn't mean agents can't be powerful. It means power should be
  earned, not assumed.
- It doesn't mean no abstraction. It means abstractions should be thin,
  obvious, and removable.
- It doesn't mean no autonomy. It means autonomy within declared bounds.
- It doesn't mean only beginners use it. The same primitives that let a
  student understand the agent loop in twenty minutes let an engineer
  ship an auditable agent in an afternoon.

---

BareBear won't generate a landing page for your startup in one prompt. It
will help a student understand what an agent is — and help an engineer
build one their team can deploy, debug, audit, and sleep soundly after
shipping.

Strong bones. Nothing extra.
