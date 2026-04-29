"""Generate lesson notebooks (and scripts for advanced lessons) from a single
source of truth. Re-run any time a lesson's content changes:

    python3 scripts/build_lessons.py
"""

from __future__ import annotations

import json
from pathlib import Path
from textwrap import dedent

ROOT = Path(__file__).resolve().parents[1]
LESSONS_DIR = ROOT / "lessons"

REPO = "richey-malhotra/barebear"
COLAB_BASE = f"https://colab.research.google.com/github/{REPO}/blob/main/lessons"


# ---------------------------------------------------------------------------
# Notebook helpers
# ---------------------------------------------------------------------------

def _split(text: str) -> list[str]:
    text = dedent(text).lstrip("\n").rstrip()
    if not text:
        return [""]
    lines = text.split("\n")
    return [line + ("\n" if i < len(lines) - 1 else "") for i, line in enumerate(lines)]


def md(text: str) -> dict:
    return {"cell_type": "markdown", "metadata": {}, "source": _split(text)}


def code(text: str) -> dict:
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": _split(text),
    }


def notebook(cells: list[dict]) -> dict:
    return {
        "cells": cells,
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python", "version": "3.9"},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }


# Setup cells used by every lesson 2-12 notebook.

SETUP_INSTALL = code('%pip install -q "barebear[openai]"')

SETUP_KEY = code("""
import os
from getpass import getpass

if not os.environ.get("OPENROUTER_API_KEY"):
    os.environ["OPENROUTER_API_KEY"] = getpass("Paste your OpenRouter key (sk-or-...): ")

# Optional: pin a specific free-tier model. If unset, barebear uses its default.
# Free-tier model availability rotates — swap here if a lesson cell errors with
# "model not available". Any *:free model on https://openrouter.ai/models works.
# os.environ["BAREBEAR_MODEL"] = "meta-llama/llama-3.2-3b-instruct:free"

print("Key set. First 8 characters:", os.environ["OPENROUTER_API_KEY"][:8] + "...")
print("Model:", os.environ.get("BAREBEAR_MODEL", "(framework default)"))
""")


def header(num: int, title: str, summary: str, slug: str) -> dict:
    return md(f"""
# Lesson {num} — {title}

{summary}

[Open in Colab]({COLAB_BASE}/{slug}/lesson.ipynb)
[Read the lesson narrative](./lesson.md)
[Back to syllabus](../README.md)
""")


def setup_section() -> list[dict]:
    return [
        md("## Setup\n\nRun the next two cells once per session. They install barebear and set your OpenRouter key (free tier — get one at <https://openrouter.ai>)."),
        SETUP_INSTALL,
        SETUP_KEY,
    ]


def whats_next(num: int, next_slug: str | None) -> dict:
    if next_slug is None:
        return md("## You're done\n\nYou've worked through all 12 lessons. The framework is now an open book — read it, modify it, build with it. If you teach with this, [let us know](https://github.com/richey-malhotra/barebear/issues).")
    return md(f"## What's next\n\n[Lesson {num + 1} →](../{next_slug}/lesson.ipynb)")


# ---------------------------------------------------------------------------
# Per-lesson definitions
# ---------------------------------------------------------------------------

def lesson_02() -> list[dict]:
    return [
        header(2, "The agent loop",
               "**You will:** wrap an LLM call in a loop, give it a tool, and watch the four-move agent loop happen turn by turn.", "02-the-agent-loop"),
        md("## The big idea\n\nIn Lesson 1 you sent one message to an LLM and got one reply. That's a chat completion. An **agent** is what you get when you wrap that call in a loop and let the model *act* on the world between turns.\n\nEvery agent loop, in every framework, has the same four moves: **perceive → think → act → observe**. The loop ends when the model returns plain text instead of asking for another tool call. That's it. That's the whole secret."),
        *setup_section(),
        md("## Your first agent\n\nA one-tool agent. You give it `greet(name)`, then ask it to greet a user. Pass `trace=True` so you can watch the loop happen."),
        code("""
from barebear import Bear, Task, Tool, OpenRouterModel

def greet(name: str) -> str:
    return f"Hello, {name}!"

bear = Bear(
    model=OpenRouterModel(),
    tools=[Tool(name="greet", fn=greet, description="Greet someone by name")],
)

report = bear.run(Task(goal="Greet a user named Alice"), trace=True)
print(report.summary())
"""),
        md("""## What just happened

You should have seen something like:

```
─── turn 1 ───
> calling model with 2 messages, 1 tools available
< tool call: greet(name="Alice")
→ greet returned: Hello, Alice!

─── turn 2 ───
< final answer: Hello, Alice! How can I help you today?
```

Two turns. **Turn 1**: the model picked the tool. The framework ran the function. The result went back in the messages. **Turn 2**: with the tool result in context, the model decided no more tool calls were needed and produced a final answer.

That's the agent loop. Everything fancy in agentic AI is variations on this."""),
        md("## Exercise\n\nAdd a second tool — `farewell(name)` — and run the agent with the goal *\"Greet Alice and then say goodbye to her.\"* How many turns does it take?"),
        code("""
def farewell(name: str) -> str:
    return f"Goodbye, {name}!"

# Build a new bear with both tools and run it.
"""),
        md("## Read the source\n\nThe agent loop is about 30 lines of Python. Open [`src/barebear/bear.py`](https://github.com/richey-malhotra/barebear/blob/main/src/barebear/bear.py) and find the `_run_loop` method. Trace the four moves directly in the code."),
        whats_next(2, "03-tool-design"),
    ]


def lesson_03() -> list[dict]:
    return [
        header(3, "Tool design",
               "**You will:** see how an LLM 'knows' which tool to call, and learn that tool descriptions are part of the prompt.", "03-tool-design"),
        md("## The big idea\n\nYou handed the agent a tool in Lesson 2. The agent picked it. *How did the model know it existed?*\n\nIt didn't, until you told it. Every tool gets converted into a *schema* — a small JSON object describing the function and its parameters. That schema goes to the model on every turn. The model reads it and decides whether to call the tool.\n\n**Tool descriptions are part of the prompt.** Vague descriptions confuse the model. Confusing parameter names cause garbage arguments. Tool design is prompt engineering wearing a different hat."),
        *setup_section(),
        md("## Three confusable tools\n\nFirst, three tools with the same vague description. Watch the model flounder."),
        code("""
from barebear import Bear, Task, Tool, OpenRouterModel

def search_web(query: str) -> str:
    return f"Web results for '{query}': [recent news, blog posts, reddit threads]"

def search_docs(query: str) -> str:
    return f"Docs results for '{query}': [API reference, guides, examples]"

def search_database(query: str) -> str:
    return f"DB results for '{query}': [10 rows from products table]"

bad_tools = [
    Tool(name="search_web", fn=search_web, description="Search for things"),
    Tool(name="search_docs", fn=search_docs, description="Search for things"),
    Tool(name="search_database", fn=search_database, description="Search for things"),
]

bear = Bear(model=OpenRouterModel(), tools=bad_tools)
bear.run(Task(goal="Find the API spec for the /users endpoint."), trace=True)
"""),
        md("## Now write decent descriptions"),
        code("""
good_tools = [
    Tool(name="search_web", fn=search_web,
         description="Search the public web (news, blogs, social media). Use for current events or external opinions."),
    Tool(name="search_docs", fn=search_docs,
         description="Search internal API and developer documentation. Use for technical references and code examples."),
    Tool(name="search_database", fn=search_database,
         description="Query the application's product database. Use for facts about products, customers, or orders."),
]

bear = Bear(model=OpenRouterModel(), tools=good_tools)
bear.run(Task(goal="Find the API spec for the /users endpoint."), trace=True)
"""),
        md("## See the schema\n\nBareBear converts each tool into a JSON schema before sending it to the model. Run the cell to see one."),
        code("""
import json

t = good_tools[1]   # search_docs
print(json.dumps(t.to_openai_schema(), indent=2))
"""),
        md("## Exercise\n\nAdd a `summarize(text)` tool. Write its description three different ways: cryptic, verbose, and Goldilocks. Which version produces the most reliable behaviour when the agent has all four tools?"),
        code("""
def summarize(text: str) -> str:
    return text[:200]

# Try three different descriptions and compare.
"""),
        whats_next(3, "04-state-and-memory"),
    ]


def lesson_04() -> list[dict]:
    return [
        header(4, "State and memory",
               "**You will:** distinguish short-term memory (the messages list) from long-term state (the `State` dict), and persist information across runs.", "04-state-and-memory"),
        md("## The big idea\n\nLLMs have no memory of their own. Every call is fresh. The only way an agent 'remembers' is because *you* hand it the same messages back next turn.\n\nWithin one `bear.run()`, the messages list grows turn by turn — that's short-term memory. Across runs, you need something else: an explicit, inspectable, snapshotable dict that the agent can read and write. BareBear calls it `State`.\n\n**Most 'magic memory' features in agent frameworks are just a dict.** Once you've seen the dict, the magic disappears."),
        *setup_section(),
        md("## A note-taker that survives between conversations"),
        code("""
from barebear import Bear, Task, Tool, State, OpenRouterModel

state = State({"notes": []})

def add_note(text: str) -> str:
    state.set("notes", state.get("notes") + [text])
    return f"Stored. {len(state.get('notes'))} note(s) total."

def list_notes() -> str:
    notes = state.get("notes")
    if not notes:
        return "No notes."
    return "\\n".join(f"- {n}" for n in notes)

tools = [
    Tool(name="add_note", fn=add_note, description="Add a note to long-term memory."),
    Tool(name="list_notes", fn=list_notes, description="List all stored notes."),
]

bear = Bear(model=OpenRouterModel(), tools=tools, state=state)

print("--- run 1: tell it something to remember ---")
bear.run(Task(goal="Remember that I like Earl Grey tea."))

print("\\n--- run 2: a fresh agent loop, but state persists ---")
bear.run(Task(goal="What do I like to drink?"), trace=True)

print("\\n--- final state ---")
print(state.snapshot())
"""),
        md("## What just happened\n\nThe second `bear.run()` is a totally fresh agent loop with no message history from the first run. But the *state* persisted. So the agent could call `list_notes()` and find what you told it before.\n\nThis is the entire pattern. Long-term memory in agents is just: store things in a dict, give the agent a tool to read/write it."),
        md("## Exercise\n\n1. Add a `delete_note(index)` tool. Verify the agent uses it when asked.\n2. Use `state.snapshot()` between runs and look at the diff. Read [`src/barebear/state.py`](https://github.com/richey-malhotra/barebear/blob/main/src/barebear/state.py) — about 60 lines."),
        code("""
def delete_note(index: int) -> str:
    notes = state.get("notes")
    if 0 <= index < len(notes):
        removed = notes.pop(index)
        state.set("notes", notes)
        return f"Removed: {removed}"
    return f"No note at index {index}."

# Build a new bear with the delete tool and try it.
"""),
        whats_next(4, "05-budgets"),
    ]


def lesson_05() -> list[dict]:
    return [
        header(5, "Budgets",
               "**You will:** see why an unbounded agent is dangerous, then watch a budget save it.", "05-budgets"),
        md("## The big idea\n\nAn agent loop has no natural stopping point. The model decides when to stop by emitting a final text response. A confused, broken, or adversarially-prompted model can keep calling tools forever. Without bounds, it can:\n\n- Burn through your API credits in minutes.\n- Hammer external services.\n- Hang your application indefinitely.\n\n**Set bounds in advance.** Step limits, tool-call limits, token limits, dollar limits. When any limit is hit, the run stops cleanly with `status='budget_exceeded'`."),
        *setup_section(),
        md("## A trap: a tool that never finds anything\n\nThis tool always says 'try again'. Without a budget, the agent could call it forever. Watch the budget catch it."),
        code("""
from barebear import Bear, Task, Tool, Policy, OpenRouterModel

def keep_searching(query: str) -> str:
    return "Found nothing useful. Try a different search."   # the trap

tight_policy = Policy(max_steps=4, max_cost_usd=0.01)

bear = Bear(
    model=OpenRouterModel(),
    tools=[Tool(name="keep_searching", fn=keep_searching, description="Search the web")],
    policy=tight_policy,
)

report = bear.run(Task(goal="Find the answer to a hard, ambiguous question."), trace=True)
print()
print("status:", report.status)         # almost certainly 'budget_exceeded'
print("steps used:", len(report.steps))
print("cost:", report.total_cost_usd)
"""),
        md("""## Read the receipt

The run stopped. Cleanly. No infinite loop. The `Report` tells you *exactly* how much it consumed:

```python
print(report.summary())
```

Production agents need this. You set the budget *before* the run, and the framework holds the line."""),
        code("print(report.summary())"),
        md("## Exercise\n\n1. Comment out the `Policy` argument and re-run. **Don't leave it running** — interrupt the cell after 30 seconds.\n2. Add `max_tool_calls=2` while keeping `max_steps=4`. Predict which limit trips first."),
        code("# Your turn — edit and run."),
        whats_next(5, "06-policy-and-guardrails"),
    ]


def lesson_06() -> list[dict]:
    return [
        header(6, "Policy and guardrails",
               "**You will:** classify tools by risk and side effects, block dangerous ones, and require approval for risky ones.", "06-policy-and-guardrails"),
        md("## The big idea\n\nAn LLM will happily call any tool you give it. If you give an agent a `delete_user_account` tool, you cannot rely on the model to decide *not* to call it. Safety has to live somewhere the model cannot override.\n\nIn BareBear, that's **`Policy`**. Every tool call passes through policy *before* it runs. The mental model: a tool is a *capability*, policy is the *permission system*."),
        *setup_section(),
        md("## A blocked tool the model wants to call"),
        code("""
from barebear import Bear, Task, Tool, Policy, OpenRouterModel

def delete_everything() -> str:
    # This function will NOT run — policy blocks the call before execution.
    return "Deleted."

policy = Policy(blocked_tools=["delete_everything"])

bear = Bear(
    model=OpenRouterModel(),
    tools=[Tool(name="delete_everything", fn=delete_everything,
                description="Delete all user data. High risk.", risk="high")],
    policy=policy,
)

report = bear.run(Task(goal="Reset the system to factory state."), trace=True)
print()
print(report.summary())
"""),
        md("## What just happened\n\nLook at the trace: you'll see the model *requested* the dangerous tool, but the framework recorded a `policy_block` step instead of executing it. The function `delete_everything` was never called. The agent then either continued without that capability or returned a final answer.\n\nThis is the safety pattern: **the model can want anything; policy decides what it can do.**"),
        md("## Side effects\n\nTools declare their `side_effects` as `none`, `internal`, or `external`. Policy can reject any tool with external side effects:"),
        code("""
def hit_external_api(endpoint: str) -> str:
    return f"(would call {endpoint})"

strict = Policy(allow_external_side_effects=False)

bear = Bear(
    model=OpenRouterModel(),
    tools=[Tool(name="hit_external_api", fn=hit_external_api,
                description="Call an external service",
                side_effects="external")],
    policy=strict,
)

report = bear.run(Task(goal="Trigger the deploy webhook."))
print(report.summary())
"""),
        md("## Exercise\n\n1. Switch `blocked_tools=[\"delete_everything\"]` for `require_approval_for=[\"delete_everything\"]`. Run again. The agent should pause with `status='paused'`. (Lesson 7 covers what to do then.)\n2. Add a tool with `risk='high'` and `side_effects='external'`. Configure a policy that allows it only with approval."),
        whats_next(6, "07-checkpoints"),
    ]


def lesson_07() -> list[dict]:
    return [
        header(7, "Checkpoints",
               "**You will:** pause an agent run for human approval, then resume it. Build an email-reply agent that drafts but won't send.", "07-checkpoints"),
        md("## The big idea\n\nSome actions are too consequential to be fully autonomous. Sending an email. Approving a refund. Deploying code. For these, you want the agent to do the *work* (read the ticket, draft the reply) — but stop, hand control to a human, and only proceed if approved.\n\nThat's a **checkpoint**. When the agent tries to call a tool that requires approval, the run pauses cleanly. A `Checkpoint` object captures everything needed to resume. Later, a human approves or rejects, and you call `bear.resume()` to continue.\n\nThis is the pattern for *trustworthy* agentic systems in production. Agent does 90%. Human signs off on the 10% that matters."),
        *setup_section(),
        md("## An email-reply agent that pauses before sending"),
        code("""
from barebear import Bear, Task, Tool, Policy, OpenRouterModel

def read_ticket(ticket_id: str) -> str:
    return f"Ticket {ticket_id} from dana@example.com: 'Reset link expired, locked out, deadline in 2 hours, please help.'"

def draft_email(to: str, subject: str, body: str) -> str:
    return f"DRAFT:\\n  To: {to}\\n  Subject: {subject}\\n  Body: {body[:200]}..."

def send_email(to: str, subject: str, body: str) -> str:
    return f"Email sent to {to}."

bear = Bear(
    model=OpenRouterModel(),
    tools=[
        Tool(name="read_ticket", fn=read_ticket, description="Read a support ticket by ID"),
        Tool(name="draft_email", fn=draft_email, description="Draft an email (no side effects)"),
        Tool(name="send_email", fn=send_email, description="Send an email to a customer",
             requires_approval=True, side_effects="external", risk="high"),
    ],
    policy=Policy(require_approval_for=["send_email"]),
)

report = bear.run(Task(goal="Read ticket TK-42 and reply with help."), trace=True)
print()
print("status:", report.status)
print("checkpoint id:", report.checkpoint_id)
"""),
        md("## Inspect the checkpoint\n\nThe run paused. Now you can read what the agent *wanted* to do, decide whether you'd approve, and resume."),
        code("""
cp = bear.checkpoints.get(report.checkpoint_id)
print("pending action:", cp.pending_action)
"""),
        md("## Approve and resume"),
        code("""
final = bear.resume(cp, approved=True)
print(final.summary())
"""),
        md("## Reject and resume\n\nIn a fresh run, try rejecting instead. The agent finishes with `status='failed'` and an error noting the rejection."),
        code("""
report2 = bear.run(Task(goal="Read ticket TK-42 and reply with help."))
if report2.status == "paused":
    cp2 = bear.checkpoints.get(report2.checkpoint_id)
    final2 = bear.resume(cp2, approved=False)
    print(final2.summary())
"""),
        md("## Exercise\n\n1. Serialise a checkpoint to JSON between pause and resume — `cp.to_dict()` if available, otherwise inspect the fields manually. Confirm you could reconstruct the run from disk after a long delay.\n2. Build an agent with **two** approval-required tools (`send_email` and `issue_refund`). Watch the order of pauses."),
        whats_next(7, "08-planning"),
    ]


def lesson_08() -> list[dict]:
    return [
        header(8, "Planning",
               "**You will:** preview what the agent intends to do before letting it act. Decide when plan-then-execute beats act-and-react.", "08-planning"),
        md("## The big idea\n\nTwo strategies for multi-step tasks:\n\n1. **Act-and-react** — the agent picks a tool, runs it, observes, picks the next. One step at a time. This is what `bear.run()` does.\n2. **Plan-then-execute** — the agent first writes down a plain-language plan *without* calling tools. You read the plan. If you like it, you execute. If you don't, you adjust.\n\nPlan-then-execute is slower and less flexible, but it gives you a *preview*. For high-stakes tasks (refactoring code, scheduling meetings, making purchases), the preview is invaluable. For exploratory tasks, it's overhead.\n\nThe skill: knowing which to use, when."),
        *setup_section(),
        md("## Plan first, then decide"),
        code("""
from barebear import Bear, Task, Tool, OpenRouterModel

def read_file(path: str) -> str:
    return f"# fake contents of {path}\\nimport flask\\napp = flask.Flask(__name__)"

def edit_file(path: str, change: str) -> str:
    return f"applied: {change}"

bear = Bear(
    model=OpenRouterModel(),
    tools=[
        Tool(name="read_file", fn=read_file, description="Read a source file"),
        Tool(name="edit_file", fn=edit_file, description="Apply a change to a file"),
    ],
)

task = Task(goal="Refactor the auth module to use dependency injection.")

plan = bear.plan(task)
print("--- plan (model wrote, no tools called) ---")
print(plan["plan"])
print()
print(f"plan cost in tokens: {plan['prompt_tokens'] + plan['completion_tokens']}")
"""),
        md("## Now decide whether to execute\n\nIn a real workflow you'd let a human approve. Here, run the cell to execute."),
        code("""
report = bear.run(task)
print(report.summary())
"""),
        md("## Exercise\n\n1. Plan the same task **three times** with different system prompts (set `Task.system_prompt`). Do the plans differ? Why?\n2. Compare token cost: `bear.plan()` vs `bear.run()` for the same task. Which is cheaper, by how much?"),
        whats_next(8, "09-reflection"),
    ]


def lesson_09() -> list[dict]:
    return [
        header(9, "Reflection",
               "**You will:** make an agent critique and revise its own answer using `Reflect`.", "09-reflection"),
        md("## The big idea\n\nLLMs are surprisingly good at *finding flaws* in answers — including their own. They are less good at producing flawless answers on the first try. **Reflection** exploits this asymmetry:\n\n1. Generate an answer.\n2. Ask the model 'what's wrong with this?'\n3. Ask the model to revise based on the critique.\n\nThat's it. BareBear ships this as a three-method helper called `Reflect`, because once you can *name* the pattern, you stop being surprised by it."),
        *setup_section(),
        md("## A weak summary, then critique, then revise"),
        code("""
from barebear import Reflect, OpenRouterModel

reflect = Reflect(model=OpenRouterModel())

original = "LLMs are AI things that make text."   # weak summary
goal = "Write a one-sentence definition of an LLM that a Year 12 student would understand."

result = reflect.run(goal=goal, answer=original)

print("--- critique ---")
print(result.critique)
print()
print("--- revised answer ---")
print(result.revised)
print()
print(f"tokens — critique: {result.critique_tokens}, revision: {result.revision_tokens}")
"""),
        md("## Use the methods individually\n\n`Reflect.run()` is critique + revise in one. You can also call them separately if you want to inspect the critique before deciding to revise:"),
        code("""
critique = reflect.critique(goal=goal, answer=original)
print("critique:", critique)

if "fine" not in critique.lower():
    revised = reflect.revise(goal=goal, answer=original, critique=critique)
    print("revised:", revised)
"""),
        md("## Exercise\n\n1. Read the source: [`src/barebear/reflect.py`](https://github.com/richey-malhotra/barebear/blob/main/src/barebear/reflect.py) — about 100 lines. Find the prompt that asks for the critique. What would you change?\n2. Make reflection iterative — critique, revise, critique again, revise again. Does the answer keep improving, or plateau? After how many rounds?"),
        whats_next(9, "10-multi-agent"),
    ]


def lesson_10() -> list[dict]:
    return [
        header(10, "Multi-agent",
               "**You will:** build a research-then-write pipeline where one agent calls another as a tool.", "10-multi-agent"),
        md("## The big idea\n\nMany real tasks are better modelled as a *team*: a researcher gathers information, a writer composes the report, a reviewer checks the writing.\n\nMulti-agent isn't a new framework feature — it's a tiny composition trick. A `Bear` produces an answer from a task. A `Tool` produces a result from arguments. **Therefore: a Bear is a Tool.** BareBear ships this as one method:\n\n```python\nresearch_tool = researcher.as_tool(name=\"research\", description=\"Research a topic\")\n```\n\nForty lines of Python and you have multi-agent."),
        *setup_section(),
        md("## A two-agent pipeline: researcher → writer"),
        code("""
from barebear import Bear, Task, Tool, OpenRouterModel

# fake search — replace with a real one in production
def search_web(query: str) -> str:
    facts = {
        "a-level cs": "UK A-level CS reform under consultation 2025: increased focus on AI ethics and software engineering.",
        "ib": "IB Computer Science: now includes a 'Computational Solutions' option.",
    }
    for k, v in facts.items():
        if k in query.lower():
            return v
    return "No specific findings."

researcher = Bear(
    model=OpenRouterModel(),
    tools=[Tool(name="search_web", fn=search_web, description="Search the web; returns a brief summary")],
)

writer = Bear(
    model=OpenRouterModel(),
    tools=[
        researcher.as_tool(
            name="research",
            description="Research a topic. Returns a brief synthesis. Use this whenever you need facts.",
        ),
    ],
)

report = writer.run(
    Task(goal="Write a short paragraph on UK A-level CS syllabus reform."),
    trace=True,
)
print()
print(report.final_output)
"""),
        md("## What just happened\n\n- The **writer** doesn't know how to search. It only has one tool: `research`.\n- When the writer calls `research`, the **researcher** runs a complete sub-task with its own tool (`search_web`).\n- The researcher returns its final answer as a string. The writer treats it as a tool result and continues.\n\nEach agent has clear responsibility. Each is testable in isolation. You can swap models between them: a cheap fast model for research, a smarter model for writing."),
        md("## Exercise\n\n1. Add a third agent — a `reviewer` Bear — that takes the writer's output, critiques it, and returns a revised version. Hint: it's `Reflect` with extra steps.\n2. Trace both bears with `trace=True`. How many total LLM calls did the pipeline take? Compare with a single-agent version."),
        whats_next(10, "11-evaluation"),
    ]


def lesson_11() -> list[dict]:
    return [
        header(11, "Evaluation",
               "**You will:** read a `Report` to understand what an agent did, then write tests for an agent.", "11-evaluation"),
        md("## The big idea\n\nYou cannot improve what you cannot measure. Every BareBear run produces a **`Report`** — a structured trace of every step, every tool call, every token, every dollar. The report is not optional debug logging; it is *the output* of running an agent. The final answer is just one field on it.\n\nReports unlock three things:\n\n1. **Audit** — exactly what tools did the agent call, with what arguments, in what order?\n2. **Cost analysis** — token counts and dollar costs are tracked, not estimated.\n3. **Testing** — you can write assertions over reports."),
        *setup_section(),
        md("## A small test suite for an email-reply agent"),
        code("""
from barebear import Bear, Task, Tool, Policy, OpenRouterModel

def read_ticket(ticket_id: str) -> str:
    return f"Ticket {ticket_id}: customer locked out."

def draft_email(to: str, subject: str, body: str) -> str:
    return f"DRAFT to {to}: {subject}"

def send_email(to: str, subject: str, body: str) -> str:
    return f"Email sent to {to}"


def build_email_agent():
    return Bear(
        model=OpenRouterModel(),
        tools=[
            Tool(name="read_ticket", fn=read_ticket, description="Read a ticket"),
            Tool(name="draft_email", fn=draft_email, description="Draft an email"),
            Tool(name="send_email", fn=send_email, description="Send an email",
                 requires_approval=True, side_effects="external"),
        ],
        policy=Policy(require_approval_for=["send_email"], max_cost_usd=0.05),
    )


def test_agent_drafts_before_sending():
    bear = build_email_agent()
    report = bear.run(Task(goal="Reply to ticket TK-42"))

    tool_steps = [s for s in report.steps if s["type"] == "tool_call"]
    tool_names = [s["tool_name"] for s in tool_steps]

    assert "read_ticket" in tool_names, "should read the ticket"
    assert "draft_email" in tool_names, "should draft before pause"
    print("PASS: agent drafted before sending")


def test_agent_pauses_for_send_approval():
    bear = build_email_agent()
    report = bear.run(Task(goal="Reply to ticket TK-42"))
    assert report.status == "paused", f"expected paused, got {report.status}"
    assert report.checkpoint_id is not None
    print("PASS: agent paused for approval")


test_agent_drafts_before_sending()
test_agent_pauses_for_send_approval()
"""),
        md("## What's interesting here\n\nThese assertions pin down the **behaviour** — the pattern of tool calls, the safety pause — independent of whatever text the model happened to produce that day. That's the only kind of test that survives across model versions."),
        md("## Exercise\n\n1. Add a budget assertion: `assert report.total_cost_usd < 0.02`. Find a sensible threshold by running the test three times.\n2. Two prompts, one task: which costs less, and which is faster? Build a tiny eval harness that runs both five times and reports averages."),
        whats_next(11, "12-honest-uncertainty"),
    ]


def lesson_12() -> list[dict]:
    return [
        header(12, "Honest uncertainty",
               "**You will:** make an agent flag what it doesn't know, and use that data downstream.", "12-honest-uncertainty"),
        md("## The big idea\n\nLLMs are trained to sound confident. They will state the wrong year for a historical event in the same tone they state the right one. For a chat toy, that's annoying. For an agent making decisions, it's a hazard.\n\nThe fix isn't 'make the model more accurate' — that's an entire research field. The fix is to make the agent **say what it doesn't know**. BareBear treats uncertainty as data: *assumptions* the agent had to make, and *missing information* it couldn't find. Both are surfaced in the `Report` as plain lists you can read, log, or branch on."),
        *setup_section(),
        md("## A research agent that has to admit defeat"),
        code("""
from barebear import Bear, Task, Tool, OpenRouterModel

def search_db(query: str) -> str:
    return "No matching records."   # the trap — agent must admit it can't find anything

system_prompt = (
    "You are a research assistant. ALWAYS state your assumptions explicitly. "
    "If you cannot verify something, say 'I could not confirm X' clearly. "
    "It is better to say you don't know than to guess confidently."
)

bear = Bear(
    model=OpenRouterModel(),
    tools=[Tool(name="search_db", fn=search_db, description="Search internal records")],
)

task = Task(
    goal="Find the lifetime value of customer Acme Corp.",
    system_prompt=system_prompt,
)

report = bear.run(task, trace=True)
print()
print("--- final answer ---")
print(report.final_output)
print()
print("--- assumptions ---")
for a in report.assumptions:
    print(" •", a)
print()
print("--- uncertainties ---")
for u in report.uncertainties:
    print(" •", u)
"""),
        md("## What to do with uncertainty data\n\nProduction code branches on these lists. For example:\n\n```python\nif report.uncertainties:\n    escalate_to_human(report)\nelse:\n    auto_approve(report)\n```\n\nThe agent is no longer a black box that 'sounds confident' — it's a system that tells you when it's guessing."),
        md("## Exercise\n\n1. Read the `_extract_uncertainty` method in [`src/barebear/bear.py`](https://github.com/richey-malhotra/barebear/blob/main/src/barebear/bear.py). It uses keyword matching. What are its weaknesses?\n2. Compare the assumptions extracted *with* and *without* the explicit system prompt above. Does prompting for honesty produce richer uncertainty data?"),
        md("""## You're done

You've built every core agentic pattern from first principles:

| #  | Concept               | Built                |
|----|-----------------------|----------------------|
| 1  | What an LLM is        | direct call          |
| 2  | The agent loop        | one-tool agent       |
| 3  | Tool design           | three-tool agent     |
| 4  | State and memory      | note-taker           |
| 5  | Budgets               | runaway-loop trap    |
| 6  | Policy                | blocked tool         |
| 7  | Checkpoints           | email-approval flow  |
| 8  | Planning              | code-refactor preview|
| 9  | Reflection            | critique-and-revise  |
| 10 | Multi-agent           | research-then-write  |
| 11 | Evaluation            | agent test suite     |
| 12 | Honest uncertainty    | flagged assumptions  |

The framework is open. Read it. Modify it. Break it. Submit a lesson.

[Back to the syllabus](../README.md)"""),
        whats_next(12, None),
    ]


LESSONS: dict[str, callable] = {
    "02-the-agent-loop": lesson_02,
    "03-tool-design": lesson_03,
    "04-state-and-memory": lesson_04,
    "05-budgets": lesson_05,
    "06-policy-and-guardrails": lesson_06,
    "07-checkpoints": lesson_07,
    "08-planning": lesson_08,
    "09-reflection": lesson_09,
    "10-multi-agent": lesson_10,
    "11-evaluation": lesson_11,
    "12-honest-uncertainty": lesson_12,
}

# Lessons that ship a parallel script (lessons 7-12 per the curriculum design).
SCRIPT_LESSONS = {
    "07-checkpoints",
    "08-planning",
    "09-reflection",
    "10-multi-agent",
    "11-evaluation",
    "12-honest-uncertainty",
}


# ---------------------------------------------------------------------------
# Script generation — derive a runnable .py from the notebook code cells
# ---------------------------------------------------------------------------

def script_for(slug: str, cells: list[dict]) -> str:
    """Concatenate code cells from a notebook into a single runnable script.

    Strips the per-notebook setup cells (install + getpass key prompt) and
    expects OPENROUTER_API_KEY to already be set in the environment.
    """
    code_cells = [c for c in cells if c["cell_type"] == "code"]
    # Drop the install cell and the getpass cell (they're notebook-only).
    code_cells = [c for c in code_cells if not _is_setup_cell(c)]

    lesson_num = int(slug.split("-")[0])
    title = slug.split("-", 1)[1].replace("-", " ").title()

    header_lines = [
        f'"""Lesson {lesson_num} — {title} (script form).',
        "",
        f"Mirrors lessons/{slug}/lesson.ipynb. Run with:",
        "",
        f"    export OPENROUTER_API_KEY=sk-or-...",
        f"    python lessons/{slug}/lesson.py",
        '"""',
        "",
        "from __future__ import annotations",
        "",
        "import os",
        "",
        'if not os.environ.get("OPENROUTER_API_KEY"):',
        '    raise SystemExit(',
        '        "OPENROUTER_API_KEY is not set. Get a free key at https://openrouter.ai "',
        '        "and export it before running this script."',
        '    )',
        "",
        "",
    ]

    body: list[str] = []
    for cell in code_cells:
        src = "".join(cell["source"]).strip()
        if not src:
            continue
        body.append(src)
        body.append("")  # blank line between cells

    return "\n".join(header_lines) + "\n".join(body) + "\n"


def _is_setup_cell(cell: dict) -> bool:
    src = "".join(cell.get("source", []))
    return "%pip install" in src or "OPENROUTER_API_KEY" in src and "getpass" in src


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------

def main() -> None:
    notebooks_written = 0
    scripts_written = 0
    for slug, builder in LESSONS.items():
        cells = builder()
        nb_path = LESSONS_DIR / slug / "lesson.ipynb"
        nb_path.parent.mkdir(parents=True, exist_ok=True)
        nb_path.write_text(json.dumps(notebook(cells), indent=1))
        notebooks_written += 1
        print(f"wrote {nb_path.relative_to(ROOT)}")

        if slug in SCRIPT_LESSONS:
            sc_path = LESSONS_DIR / slug / "lesson.py"
            sc_path.write_text(script_for(slug, cells))
            scripts_written += 1
            print(f"wrote {sc_path.relative_to(ROOT)}")

    print(f"\n{notebooks_written} notebooks, {scripts_written} scripts")


if __name__ == "__main__":
    main()
