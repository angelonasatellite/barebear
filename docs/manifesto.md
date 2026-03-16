# The BareBear Manifesto

Most agent frameworks optimise for demos. BareBear optimises for reality.

---

We built BareBear because we kept seeing the same failure mode: an agent that looks magical in a notebook and terrifying in production. The demo works. The deploy doesn't. The gap is always the same — invisible state, unchecked tools, unbounded loops, and no way to answer "why did it do that?"

BareBear is built on seven beliefs:

**1. Tools are permissions, not features.**
A tool that can send email is not the same as a tool that can read a file. The framework should know the difference and enforce it before execution, not after the damage is done.

**2. State must be visible.**
If you can't inspect the agent's state at any point in a run, you can't debug it, audit it, or trust it. Hidden memory is technical debt with compound interest.

**3. Autonomy needs bounds.**
An agent without limits is a while-True loop with a credit card. Step limits, token budgets, cost caps, and approval gates aren't restrictions — they're the reason you can deploy with confidence.

**4. Every run is a receipt.**
When something goes wrong (it will), you need to know exactly what happened: which tools were called, in what order, with what arguments, at what cost, and whether any assumptions were made. Reports aren't a nice-to-have. They're the product.

**5. Uncertainty is data.**
"I don't know" is more valuable than a confident hallucination. The framework should track what it's guessing, what information is missing, and what it can't verify. Epistemic honesty isn't a feature — it's a responsibility.

**6. One bear first.**
Don't start with a multi-agent system. Start with one agent that does one thing well, with clear policy and traceable behaviour. Add complexity only when you've proven the simple version isn't enough. Most of the time, it is.

**7. No orchestration theatre.**
No invisible planners. No magic routers. No auto-generated chains. If the system does something, you should be able to point to the line of code that decided to do it. Explicitness isn't a burden — it's the whole point.

---

## What this means in practice

- Every tool declares its risk level and side effects.
- Policy is checked before every tool execution.
- Runs have budgets. When the budget runs out, the run stops.
- High-risk actions create checkpoints. Humans approve or reject.
- Reports capture steps, costs, tokens, assumptions, and uncertainties.
- State is a dictionary. You can snapshot it, diff it, serialise it.
- The agent tells you what it doesn't know.

### What this doesn't mean

- It doesn't mean agents can't be powerful. It means power should be earned, not assumed.
- It doesn't mean no abstraction. It means abstractions should be thin, obvious, and removable.
- It doesn't mean no autonomy. It means autonomy within declared bounds.

---

BareBear won't generate a landing page for your startup in one prompt. It will help you build an agent that your team can deploy, debug, audit, and sleep soundly after shipping.

Strong bones. Nothing extra.
