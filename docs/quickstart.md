# Quickstart

Get a BareBear agent running in under 5 minutes.

## Installation

```bash
pip install barebear
```

For OpenAI support:

```bash
pip install barebear[openai]
```

## Your first bear

The simplest possible agent — no API keys, no tools, just a mock model:

```python
from barebear import Bear, Task, MockModel

bear = Bear(model=MockModel())
result = bear.run(Task(goal="Say hello"))
print(result.summary())
```

`MockModel` simulates model responses locally. It auto-calls available tools and produces a final text response — perfect for development and testing.

## Adding tools

Tools are plain Python functions wrapped with metadata:

```python
from barebear import Bear, Task, Tool, MockModel

def search(query: str) -> str:
    return f"Results for: {query}"

def summarize(text: str) -> str:
    return text[:100]

bear = Bear(
    model=MockModel(),
    tools=[
        Tool("search", fn=search, description="Search for information"),
        Tool("summarize", fn=summarize, description="Summarize text"),
    ],
)

result = bear.run(Task(goal="Search for Python frameworks and summarize"))
print(result.summary())
```

The mock model will call each tool in order, then return a final response. The report shows exactly what happened.

## Setting policy

Policy defines the bounds your agent operates within:

```python
from barebear import Bear, Task, Tool, Policy, MockModel

policy = Policy(
    max_steps=5,              # stop after 5 steps
    max_cost_usd=0.10,        # hard cost cap
    max_tokens=10000,          # token budget
    blocked_tools=["rm_rf"],   # never allow this tool
    require_approval_for=["send_email"],  # pause for human approval
    allow_external_side_effects=False,    # block tools with external side effects
)

bear = Bear(
    model=MockModel(),
    tools=[
        Tool("draft", fn=lambda text: f"Draft: {text}", description="Draft text"),
        Tool("send_email", fn=lambda to, body: "sent", description="Send email",
             risk="high", side_effects="external", requires_approval=True),
    ],
    policy=policy,
)
```

When the agent tries to call `send_email`, policy blocks it (or pauses for approval) before the function executes.

## Running and reading the receipt

Every `bear.run()` call returns a `Report`:

```python
result = bear.run(Task(goal="Draft a reply to the support ticket"))

# Human-readable summary
print(result.summary())

# Programmatic access
print(result.status)          # "completed", "paused", "failed", "budget_exceeded"
print(result.steps)           # list of step dicts
print(result.total_tokens)    # total tokens used
print(result.total_cost_usd)  # total cost in USD
print(result.assumptions)     # what the agent assumed
print(result.uncertainties)   # what it wasn't sure about

# Full JSON trace for logging/auditing
print(result.to_json())
```

## Using with OpenAI

Swap `MockModel` for `OpenAIModel` when you're ready to use real models:

```python
from barebear import Bear, Task, Tool, Policy
from barebear.models import OpenAIModel

bear = Bear(
    model=OpenAIModel("gpt-4o-mini"),  # uses OPENAI_API_KEY env var
    tools=[
        Tool("search", fn=my_search_fn, description="Search the web"),
    ],
    policy=Policy(max_steps=10, max_cost_usd=0.50),
)

result = bear.run(Task(goal="Research recent developments in Rust web frameworks"))
print(result.summary())
```

You can also pass `api_key` and `base_url` directly:

```python
model = OpenAIModel("gpt-4o-mini", api_key="sk-...", base_url="https://...")
```

## Using with OpenRouter

[OpenRouter](https://openrouter.ai) gives you access to hundreds of models (including free ones) through a single API:

```python
from barebear import Bear, Task, Tool, Policy
from barebear.models import OpenRouterModel

bear = Bear(
    model=OpenRouterModel("meta-llama/llama-4-scout"),  # uses OPENROUTER_API_KEY env var
    tools=[
        Tool("search", fn=my_search_fn, description="Search the web"),
    ],
    policy=Policy(max_steps=10, max_cost_usd=0.50),
)

result = bear.run(Task(goal="Research recent developments in Rust web frameworks"))
print(result.summary())
```

Any model on OpenRouter that supports tool calling will work. Set your key:

```bash
export OPENROUTER_API_KEY="sk-or-..."
```

## Next steps

- Browse the [examples](../examples/) — all run locally with `MockModel`
- Read the [architecture](architecture.md) to understand the run loop
- Read the [manifesto](manifesto.md) for the design philosophy
- Check the [README](../README.md) for the full feature overview
