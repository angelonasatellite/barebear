# Quickstart

Get a BareBear agent running against a real LLM in under 5 minutes. No card,
no install of anything heavy.

## Installation

```bash
pip install barebear[openai]
```

The `[openai]` extra installs the OpenAI Python client, which BareBear uses to
talk to OpenAI itself, OpenRouter (default), and Ollama (local).

## Pick a backend

### OpenRouter (recommended — free tier, no install)

OpenRouter is one OpenAI-compatible endpoint that routes to hundreds of models,
including free ones.

1. Sign in at <https://openrouter.ai> (GitHub or Google).
2. Create a key. The free tier requires no payment method.
3. Export it:

```bash
export OPENROUTER_API_KEY="sk-or-..."
```

### Ollama (offline, local)

```bash
# from https://ollama.com — install the binary, then:
ollama pull qwen2.5:3b
ollama serve
```

No keys needed. Slower than hosted models, but fully offline.

## Your first bear

```python
from barebear import Bear, Task, Tool, OpenRouterModel

def greet(name: str) -> str:
    return f"Hello, {name}!"

bear = Bear(
    model=OpenRouterModel(),
    tools=[Tool(name="greet", fn=greet, description="Greet someone by name")],
)

result = bear.run(Task(goal="Greet a user named Alice"), trace=True)
print(result.summary())
```

`trace=True` streams every loop turn to stdout so you can watch the agent
think. Drop it for production.

To use Ollama instead, swap one line:

```python
from barebear import OllamaModel
bear = Bear(model=OllamaModel(), tools=[...])
```

## Add tools

Tools are plain Python functions wrapped with metadata:

```python
from barebear import Bear, Task, Tool, OpenRouterModel

def search(query: str) -> str:
    return f"Results for: {query}"

def summarize(text: str) -> str:
    return text[:100]

bear = Bear(
    model=OpenRouterModel(),
    tools=[
        Tool("search", fn=search, description="Search for information"),
        Tool("summarize", fn=summarize, description="Summarize text"),
    ],
)

result = bear.run(Task(goal="Search for Python frameworks and summarize"))
print(result.summary())
```

## Set policy

`Policy` defines the bounds your agent operates within:

```python
from barebear import Bear, Task, Tool, Policy, OpenRouterModel

policy = Policy(
    max_steps=5,
    max_cost_usd=0.10,
    max_tokens=10000,
    blocked_tools=["delete_account"],
    require_approval_for=["send_email"],
    allow_external_side_effects=False,
)

bear = Bear(
    model=OpenRouterModel(),
    tools=[
        Tool("draft", fn=lambda text: f"Draft: {text}", description="Draft text"),
        Tool("send_email", fn=lambda to, body: "sent", description="Send email",
             risk="high", side_effects="external", requires_approval=True),
    ],
    policy=policy,
)
```

When the agent tries to call `send_email`, policy pauses for approval before
the function executes.

## Read the receipt

Every `bear.run()` call returns a `Report`:

```python
result = bear.run(Task(goal="Draft a reply to the support ticket"))

print(result.summary())            # human-readable
print(result.status)               # "completed" | "paused" | "failed" | "budget_exceeded"
print(result.steps)                # list of every step
print(result.total_tokens)         # tokens consumed
print(result.total_cost_usd)       # cost in USD
print(result.assumptions)          # what the agent assumed
print(result.uncertainties)        # what it wasn't sure about

print(result.to_json())            # full trace, for logging or auditing
```

## Custom system prompt

```python
task = Task(
    goal="Plan a study schedule",
    system_prompt="You are a Year 12 study coach. Be encouraging but firm.",
)
bear.run(task)
```

## Reflection

Self-critique in three calls:

```python
from barebear import Reflect, OpenRouterModel

reflect = Reflect(model=OpenRouterModel())
out = reflect.run(goal="Define an LLM for a teen", answer="It's an AI thing.")
print(out.critique)
print(out.revised)
```

## Multi-agent

A Bear is callable as a Tool, so a Bear can call another Bear:

```python
researcher = Bear(model=OpenRouterModel(), tools=[search_tool])
writer = Bear(
    model=OpenRouterModel(),
    tools=[researcher.as_tool(name="research", description="Research a topic")],
)

writer.run(Task(goal="Write a brief on UK A-level CS reform."))
```

## Next steps

- Work through the [12-lesson course](../lessons/README.md). It assumes only
  Python basics and walks you from "what is an LLM?" to a working multi-agent
  system.
- Browse the [examples](../examples/) — fully worked agents you can run today.
- Read the [architecture](architecture.md) and the [manifesto](manifesto.md).
- The whole framework is ~1,500 lines of Python. [Read the source](../src/barebear/).
