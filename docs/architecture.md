# Architecture

BareBear has a deliberately simple architecture. The goal is few moving parts, each doing one thing.

## Layers

### Layer 1: Core runtime (shipped)

The 7 primitives and the run loop. This is what exists today.

```text
Bear ── Task ── State ── Tool ── Policy ── Checkpoint ── Report
```

- **Bear**: holds model, tools, policy, state. Executes the run loop.
- **Task**: goal + input + optional context. Immutable once created.
- **State**: key-value store with snapshot history and change tracking.
- **Tool**: callable function with risk/side-effect metadata.
- **Policy**: constraints checked before every tool execution.
- **Checkpoint**: pause-point for human approval workflows.
- **Report**: full trace of a run — steps, costs, tokens, uncertainties.

Supporting classes:

- **Budget**: tracks resource consumption against policy limits.
- **Uncertainty**: records missing information (assumptions, confidence, unknowns).
- **ToolRegistry**: holds tools by name, enforces uniqueness.
- **CheckpointManager**: stores and manages checkpoints.

### Layer 2: Model adapters (shipped)

Thin wrappers over LLM APIs. Each adapter implements `ModelAdapter.complete()`.

| Adapter | Status | Notes |
| --- | --- | --- |
| `OpenAIModel` | Shipped | OpenAI chat completions with tool use. |
| `OpenRouterModel` | Shipped | Hundreds of models via a single OpenAI-compatible endpoint. Free tier available. |
| `OllamaModel` | Shipped | Local Ollama server (OpenAI-compatible at `localhost:11434/v1`). Offline-friendly. |
| `barebear.testing.FakeModel` | Internal | Deterministic stand-in for the framework's own tests. Not for student use. |

Adding an adapter means implementing one method:

```python
class ModelAdapter(ABC):
    @abstractmethod
    def complete(self, messages: list[dict], tools: list[dict] | None = None) -> ModelResponse:
        ...
```

### Layer 3: Patterns (planned)

Common agent patterns built on the primitives. These won't be magic — just pre-wired configurations.

- **Pipelines**: chain multiple bears sequentially, output of one feeds the next.
- **Map-reduce**: fan out work across bears, collect and merge results.
- **Supervisor**: one bear delegates to others, reviews their output.

The rule: one bear first. Patterns only when the single-bear approach hits its limit.

### Layer 4: Control plane (planned)

Operational layer for production deployments:

- Run persistence (save/load checkpoints across restarts)
- Webhook-based approval workflows
- Observability hooks (OpenTelemetry spans)
- Rate limiting and queue management

## The run loop

This is the core of BareBear. Here's what happens when you call `bear.run(task)`:

```text
1. Init
   ├── Create Budget from Policy
   ├── Create empty Report
   ├── Build system prompt (includes tool schemas + policy text)
   └── Build user message from Task goal + input

2. Loop (until text response or budget exceeded)
   ├── Budget.record_step() — increment step counter
   ├── Budget.check() — raise BudgetExceeded if any limit hit
   ├── Model.complete(messages, tools) — call the LLM
   ├── Budget.record_tokens() — track token usage and cost
   │
   ├── If text response (no tool calls):
   │   ├── Record in Report
   │   └── Break — run is done
   │
   └── If tool calls:
       └── For each tool call:
           ├── Tool exists? → No → record error, continue
           ├── Policy.is_blocked(tool)? → Yes → record block, continue
           ├── Policy.needs_approval(tool)? → Yes → create Checkpoint, raise
           ├── Budget.record_tool_call()
           ├── Execute tool function
           ├── Record result in messages and Report
           └── Continue loop

3. Finalize
   ├── Set Report duration, token totals, cost
   ├── Copy uncertainties and assumptions into Report
   └── Return Report
```

## Policy enforcement

Policy is checked at two points:

**Before each step**: Budget limits (steps, tokens, cost) are verified. If any limit is exceeded, the run halts with `budget_exceeded` status.

**Before each tool call**: The tool is checked against:

1. `blocked_tools` — is this tool explicitly forbidden? → skip with `policy_block`
2. `allow_external_side_effects` — does this tool have external side effects when policy disallows them? → skip with `policy_block`
3. `require_approval_for` / `requires_approval` — does this tool need human sign-off? → create checkpoint, pause run

Policy never fires *after* a tool runs. The check always happens before execution. This is a deliberate design choice — you can't un-send an email.

## State management

State is explicit. It's a dictionary with three extras:

- **`set(key, value)`**: records the change with timestamp and old value
- **`snapshot()`**: deep-copies current state, adds it to history
- **`changes()`**: returns the full list of individual mutations

This means you can always answer: "what did the agent change, and when?"

## Report structure

Every run produces a Report with:

```json
{
    "task_id": "a1b2c3d4",
    "status": "completed",           # completed | failed | paused | budget_exceeded
    "steps": [...],                   # ordered list of step dicts
    "total_tokens": 450,
    "total_cost_usd": 0.0012,
    "duration_seconds": 1.34,
    "assumptions": ["..."],           # what the agent assumed
    "uncertainties": ["..."],         # what it wasn't sure about
    "final_output": "...",            # the agent's final text response
    "error": null,                    # error message if failed
    "checkpoint_id": null             # checkpoint ID if paused
}
```

Each step captures:

- Step number, type (`tool_call`, `response`, `policy_block`, `checkpoint`, `error`)
- Summary text
- Tool name and arguments (if applicable)
- Tool result (if applicable)
- Error details (if applicable)
