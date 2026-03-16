<div align="center">
<img alt="BareBear" src="https://raw.githubusercontent.com/richey-malhotra/barebear/v0.1.1/assets/logo.png" width="320">
<br>
<strong>Every step leaves a print.</strong>
<br><br>
Minimal agent framework. Explicit state, policy-first tools, honest uncertainty.
<br><br>
<a href="https://github.com/richey-malhotra/barebear/actions"><img src="https://img.shields.io/github/actions/workflow/status/richey-malhotra/barebear/tests.yml?branch=main" alt="Tests"></a>
<a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="License: MIT"></a>
<img src="https://img.shields.io/badge/python-3.9+-blue.svg" alt="Python 3.9+">
<a href="https://pypi.org/project/barebear/"><img src="https://img.shields.io/pypi/v/barebear.svg?v=0.1.1" alt="PyPI"></a>
<br><br>
<img src="https://raw.githubusercontent.com/richey-malhotra/barebear/v0.1.1/demo.gif" alt="BareBear demo" width="700">
</div>

---

## What is BareBear?

BareBear is a Python framework for building LLM agents that you can actually trust in production. It gives you 7 primitives, a policy engine, and a run receipt — nothing else. Every tool call is checked against policy before execution. Every run produces a traceable report. The agent knows what it doesn't know, and tells you.

## Why?

Most agent frameworks give you magic orchestration, invisible state, and tools that fire without guardrails. That works great in demos. It falls apart when a customer asks why the agent sent that email, or when your bill spikes because the loop ran 200 steps.

BareBear is built on different assumptions:

- **Tools are dangerous.** Every tool declares its risk level and side effects. Policy checks happen *before* execution, not after.
- **State should be visible.** No hidden memory, no magic context. State is a dict you can inspect, snapshot, and diff.
- **Autonomy needs bounds.** Step limits, cost caps, token budgets, approval gates — all declared upfront in policy.
- **Runs should be receipts.** Every run produces a `Report` with steps, costs, assumptions, and uncertainties. You can audit it, log it, replay it.
- **Uncertainty is data, not a bug.** If the agent isn't sure, it says so. Assumptions are tracked explicitly.

## Quickstart

```bash
pip install barebear
```

```python
from barebear import Bear, Task, Policy, Tool, MockModel

def greet(name: str) -> str:
    return f"Hello, {name}!"

bear = Bear(
    model=MockModel(),
    tools=[Tool("greet", fn=greet, description="Greet someone by name")],
    policy=Policy(max_steps=5, max_cost_usd=0.05),
)

result = bear.run(Task(goal="Greet the user Alice"))
print(result.summary())
```

```text
==================================================
  BAREBEAR RUN REPORT
==================================================
  Task ID:    a1b2c3d4
  Status:     completed
  Steps:      2
  Tokens:     160
  Cost:       $0.0000
  Duration:   0.00s
--------------------------------------------------
  STEPS:
    1. [tool_call] Called greet (tool: greet)
    2. [response] Task completed successfully.
--------------------------------------------------
==================================================
```

No API key needed — `MockModel` auto-calls available tools and produces a final response. Swap in `OpenAIModel("gpt-4o-mini")` or `OpenRouterModel("meta-llama/llama-4-scout")` when you're ready for the real thing.

## The 7 Primitives

| Primitive | What it does |
| --- | --- |
| **Bear** | The agent. Holds model, tools, policy, state. Runs tasks. |
| **Task** | A unit of work: a goal string, input dict, optional context. |
| **State** | Explicit key-value store with snapshot history and change tracking. |
| **Tool** | A callable with declared risk, side effects, and approval requirements. |
| **Policy** | Constraints: step limits, cost caps, blocked tools, approval lists. |
| **Checkpoint** | A saved pause-point for human approval before high-risk actions. |
| **Report** | The run receipt: every step, token count, cost, assumptions, uncertainties. |

That's it. No chains, no graphs, no planners, no routers. Just the bones.

## Features

### Policy-first tool execution

Every tool call passes through policy before it runs. Block tools, require approval, or reject external side effects — all in one declaration.

```python
policy = Policy(
    max_steps=10,
    blocked_tools=["delete_account"],
    require_approval_for=["send_email"],
    allow_external_side_effects=False,
)
```

### Budget tracking

Step counts, tool calls, token usage, and dollar cost — all tracked against limits you set. If a run hits its budget, it stops cleanly with a `budget_exceeded` status.

```python
policy = Policy(max_steps=8, max_cost_usd=0.10, max_tokens=50000)
```

### Checkpoint / approval gates

High-risk tools pause the run and create a `Checkpoint`. You approve or reject, then resume.

```python
bear = Bear(
    model=model,
    tools=[
        Tool("send_email", fn=send_email, risk="high",
             side_effects="external", requires_approval=True),
    ],
    policy=Policy(require_approval_for=["send_email"]),
)

result = bear.run(task)

if result.status == "paused":
    checkpoint = bear.checkpoints.get(result.checkpoint_id)
    result = bear.resume(checkpoint, approved=True)
```

### Side-effect staging

Tools declare `side_effects="none"`, `"internal"`, or `"external"`. Policy can block external side effects entirely, so your agent can *propose* actions without executing them.

```python
Tool("propose_patch", fn=propose, description="Suggest a code change",
     side_effects="none")
Tool("apply_patch", fn=apply, description="Apply the change",
     side_effects="external")
```

### Run receipts

Every `bear.run()` returns a `Report` — a full trace you can print, serialise to JSON, or store for auditing.

```python
result = bear.run(task)

print(result.summary())       # human-readable receipt
print(result.to_json())       # full JSON trace
print(result.total_cost_usd)  # what it cost
print(result.steps)            # list of every step taken
```

### Honest uncertainty

Bears track what they don't know. Assumptions and missing information are first-class data in the report, not buried in log noise.

```python
result = bear.run(task)
print(result.assumptions)     # ["Customer tier assumed from email domain"]
print(result.uncertainties)   # ["Could not verify account status"]
```

## Examples

All examples run with `MockModel` by default — no API keys needed. Pass `--live` to use OpenAI.

```bash
export PYTHONPATH=src
```

| Example | What it shows | Run it |
| --- | --- | --- |
| **Research Assistant** | Tool use, multi-step reasoning, report generation | `python examples/research_assistant/run.py` |
| **Email Approval** | `requires_approval`, checkpoint gates, side-effect policy | `python examples/email_approval/run.py` |
| **File Patcher** | Side-effect staging (propose allowed, apply blocked) | `python examples/file_patcher/run.py` |
| **Ticket Triage** | Multi-step classification, budget tracking across calls | `python examples/ticket_triage/run.py` |

## Architecture

```text
┌─────────────────────────────────────────────────┐
│                   bear.run(task)                 │
├─────────────────────────────────────────────────┤
│                                                 │
│   Task ──► System Prompt + User Message         │
│                     │                           │
│                     ▼                           │
│              ┌─────────────┐                    │
│              │  Run Loop   │◄── Budget check    │
│              └──────┬──────┘    each step       │
│                     │                           │
│          ┌──────────┴──────────┐                │
│          ▼                     ▼                │
│     Text response         Tool calls            │
│     ──► Report            ──► Policy check      │
│                               │                 │
│                    ┌──────────┼──────────┐      │
│                    ▼          ▼          ▼      │
│                 Allowed    Blocked    Approval   │
│                 ──► Execute ──► Skip  ──► Pause  │
│                     │                    │      │
│                     ▼                    ▼      │
│                Tool result          Checkpoint   │
│                ──► Loop              (resume)    │
│                                                 │
├─────────────────────────────────────────────────┤
│  State (explicit, snapshotable, diffable)       │
│  Budget (steps, tokens, cost — all tracked)     │
│  Report (full receipt of everything that happened)│
└─────────────────────────────────────────────────┘
```

See [docs/architecture.md](docs/architecture.md) for the full breakdown.

## Philosophy

> Most frameworks optimise for demos. BareBear optimises for reality.

Read the [manifesto](docs/manifesto.md).

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). We welcome PRs, bug reports, and honest feedback.

## License

[MIT](LICENSE) — Richey Malhotra, 2026.
