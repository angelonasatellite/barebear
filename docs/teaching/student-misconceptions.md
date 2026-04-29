# Common student misconceptions

A reference for the questions students will actually ask in the first
six lessons, with plain-English re-framings that hold up under
follow-up. Use this to pre-load before a lesson, or to look up an
answer mid-class.

Each entry follows the same shape: **the question or claim**, **why
students arrive at it**, **what to say**, and a **one-line one-liner**
to use if you've got 30 seconds before the bell.

---

## "Is the AI thinking?"

**Why students ask it:** the model produces fluent, plausible text. It
sounds like thought.

**What to say:** an LLM is a very large pattern-matcher. It was trained
to predict the next token in a sequence based on every text it ever
saw. When it produces a sentence, it is doing extremely sophisticated
prediction — not reasoning the way you reason. The reason it *sounds*
like thought is that the text it learned from was written by people
thinking.

A useful comparison: a parrot can produce a perfect sentence it heard a
thousand times. The parrot is not thinking the sentence; it's producing
it. LLMs are like parrots with the entire internet in their head and
better fluency. Whether that ever counts as "thinking" is a real
philosophical question. In your classroom, treating it as "very fancy
prediction" is the safe and accurate frame.

**One-liner:** *"It's predicting, very well, what someone would say
next. That's it. Whether 'predicting very well' is 'thinking' is a
question for philosophy class."*

---

## "Why does it give me a different answer every time?"

**Why students ask it:** they expect computer programs to be
deterministic. Most code they've written is.

**What to say:** the model picks each word probabilistically. There's a
setting called *temperature* that controls how much randomness — at
high temperature it's more creative, at low temperature it's more
predictable. By default most providers use a temperature above zero, so
you get variation. This is *intentional*: it's part of why the same
prompt can produce different essays, different code, different ideas.

For agents, this matters: the same task run twice might use different
tools or take different numbers of steps. That's why we need
**budgets** (Lesson 5) and **policy** (Lesson 6) — to bound the
non-determinism.

**One-liner:** *"It picks words by rolling a weighted dice. Same prompt
≠ same answer."*

---

## "Did the agent really use the tool, or did it pretend?"

**Why students ask it:** the model can produce a sentence saying "I
called the function" without actually calling anything. Students
sometimes can't tell the difference.

**What to say:** the model can only *describe* what it would do; it
can't actually run code. The framework — barebear — is what reads the
model's response, sees a tool-call request, runs the actual Python
function, and feeds the result back. If the agent says "I searched the
database" but no `tool_call` step appears in the report, then no
search happened. The report is the truth; the model's narration is
just text.

This is why every barebear lesson stresses the `Report` and the trace.
**You audit the report, not the agent's words.**

**One-liner:** *"The agent's words are just words. The report is the
truth."*

---

## "What if the model lies?"

**Why students ask it:** they've seen an LLM produce confidently wrong
information. The technical term is *hallucination* — they may know it.

**What to say:** the model doesn't lie in the human sense, because
lying requires intent. It produces text that sounds plausible. When
the underlying training data didn't actually contain the information
needed, it produces plausible-sounding text anyway. It cannot
distinguish "I know this" from "I'm constructing this."

That's exactly why Lesson 12 — Honest Uncertainty — exists. We can
*ask* the model to flag what it's guessing. We can build the agent to
treat uncertainty as data. We can refuse to act on outputs the agent
admits it isn't sure about. Hallucination is real; engineering against
it is the response.

**One-liner:** *"The model doesn't know what it doesn't know. The
framework can. That's why uncertainty is a first-class output, not a
bug."*

---

## "Couldn't a really smart prompt make the AI safe?"

**Why students ask it:** prompt engineering content online is
optimistic. Students think the right prompt solves any safety
problem.

**What to say:** prompts are *requests* to the model. The model is
free to ignore them. Modern LLMs are pretty good at following
sensible instructions, but they're not guaranteed to. If you give a
model a `delete_account` tool and prompt it "never delete anything",
a confused or adversarial input can still cause it to call the
delete tool. **The prompt is not a security boundary.**

What *is* a security boundary: the framework. Policy checks the tool
*before* it runs. The model can want to delete; the framework refuses.

This is the central design lesson of the course: **trust the layer
that the model can't override**.

**One-liner:** *"A prompt is a polite request. A policy is a refusal.
Use the right tool for the right level of trust."*

---

## "Why isn't the agent just one big prompt?"

**Why students ask it:** they've seen "prompt engineering" frameworks
that are essentially long instruction text. They wonder why we need a
loop and tools at all.

**What to say:** an LLM call returns text. If you want the agent to
*do* something — search a database, send an email, write a file —
text isn't enough. You need to read the text, understand the model
wants to do an action, run the action, get the result, and feed it
back to the model so it can decide the next step. That's the loop.
Without it, you have a chatbot. With it, you have an agent.

**One-liner:** *"A prompt is a chat. A loop is an agent."*

---

## "If we can budget the agent, why does this need a whole framework?"

**Why students ask it:** budgets sound trivial — a counter and a
limit. Why isn't this 20 lines of code?

**What to say:** budgets are one piece. The framework also needs to
handle: tool schema generation, policy enforcement before each tool
call, checkpoint creation when approval is needed, full state
reconstruction on resume, report assembly with assumptions and
uncertainties extracted from text, multiple model adapters, and so
on. Each piece is small. Together they make a system you can deploy
without nightmares. **Read the source — every primitive is small
enough to grasp in a sitting.**

**One-liner:** *"Each piece is small. The system is the point."*

---

## "But everyone uses LangChain / CrewAI / AutoGen — why a different framework?"

**Why students ask it:** they've seen the bigger frameworks named in
podcasts, blog posts, YouTube tutorials.

**What to say:** those frameworks are powerful and used in production
in many places. They're also large — tens of thousands of lines, deep
inheritance trees, lots of magic. They're hard to read end-to-end.
For *learning* what an agent is, you want something small enough to
read every line of. That's barebear's deliberate scope. After this
course, students who pick up a bigger framework can recognise its
primitives because they've built the simpler version themselves.

**One-liner:** *"Big frameworks are for shipping. Small frameworks are
for understanding. Understand first, ship second."*

---

## "Is using AI cheating?"

**Why students ask it:** schools, exam boards, and parents have all
been talking about it. They want a real answer.

**What to say:** this is a course about *building* AI systems, not
using AI to do their schoolwork for them. Building an agent that can
do something is a deeply educational activity. Using ChatGPT to write
their History essay is a separate question, with separate answers,
and your school's academic-integrity policy probably already covers
it.

There's a genuine distinction worth surfacing: **using AI as a
collaborator while you do the thinking** is closer to using a
calculator. **Asking AI to think for you so you don't have to** is
closer to copying. The difference is whether you remain the author of
your own decisions.

**One-liner:** *"Using a calculator isn't cheating at maths. Letting
the calculator decide what to compute might be."*

---

## "Won't AI take all the programming jobs?"

**Why students ask it:** they've seen the headlines. It's a real
worry, especially in Year 12 deciding whether to study CS at
university.

**What to say:** the people who understand how these systems *work*
— how to design tools for them, when to use plan-then-execute, how
to set policy, how to evaluate them in production — are the people
this technology empowers, not replaces. Building agents requires
understanding software engineering, distributed systems, security,
ethics, and human factors. None of that is going away. By the time
you graduate, the demand for people who can *engineer* AI systems
will be larger than today, not smaller.

It's also fair to say: nobody knows for sure. But every previous
wave (compilers, frameworks, cloud, IDEs) made programming *more*
common, not less. The bet you make in Year 12 is on *understanding*,
not on a specific job title.

**One-liner:** *"The people who understand how these systems work
are the ones the technology empowers, not replaces. That's you, if
you keep going."*

---

## When you don't know the answer

Honest in front of a class beats faking it. *"Good question. Let's
investigate together."* Then run an experiment in the notebook. The
notebook is right there on the projector — modify a cell, run it, see
what happens. Modelling that genuine curiosity is more pedagogically
valuable than pretending omniscience.

If you're stuck and want a sounding board, the [pinned classroom
thread](https://github.com/richey-malhotra/barebear/issues/1) is the
right place to surface it — your question almost certainly helps the
next teacher too.
