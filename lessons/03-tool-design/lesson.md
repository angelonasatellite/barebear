# Lesson 3 — Tool design

> **Learning outcomes**
> - Explain how an LLM "knows" what tools exist (the schema).
> - Predict which tool the model will pick for a given request.
> - Write a tool description that a model can use successfully.

**Pace:** about 60 minutes. The schema-printing step alone is worth 10 minutes of class discussion — let students predict what the schema will contain before you reveal it.

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/richey-malhotra/barebear/blob/main/lessons/03-tool-design/lesson.ipynb)

## The big idea

You handed the agent a tool in Lesson 2. The agent picked it. How did the
model know it existed?

It didn't, until you told it. Every tool gets converted into a *schema* — a
small JSON object that names the function, describes what it does, and lists
its parameters with types. That schema is sent to the model on every turn
alongside the messages. The model reads it and decides: "do I want to call
this tool, and if so, with what arguments?"

The lesson here is that **tool descriptions are part of the prompt.** If the
description is vague, the model picks the wrong tool. If the parameter names
are confusing, the model fills them with garbage. Tool design is prompt
engineering wearing a different hat.

## What you will build

An agent with three tools that look superficially similar:

```python
def search_web(query: str) -> str: ...
def search_docs(query: str) -> str: ...
def search_database(query: str) -> str: ...
```

You'll start with all three having the same description ("Search for things")
and watch the model flounder. Then you'll fix the descriptions and watch it
pick the right tool every time.

## Exercise

1. Add a `summarize(text)` tool. Write its description three different ways:
   one cryptic, one verbose, one Goldilocks. Which produces the best behaviour?
2. Look at the JSON schema BareBear generates for one of your tools:
   `print(my_tool.to_openai_schema())`. Where do the parameter types come
   from? (Hint: type annotations.)

## Homework

Take the three-tool agent from this lesson (`search_web`, `search_docs`,
`search_database`). **Run it three times** with the same task —
*"Find the API spec for the /users endpoint"* — but each time, swap one
tool's description for one of these three styles:

1. **Cryptic:** *"Look stuff up."*
2. **Verbose:** four full sentences explaining when to use it, what it
   returns, what its limits are, and an example query.
3. **Goldilocks:** the description you originally wrote.

For each run, capture which tool the agent picked. Bring the three
runs (and the descriptions) to the next lesson — we'll discuss which
description style won and why.

```python
# Sketch:
my_descriptions = {"cryptic": "Look stuff up.", "verbose": "...", "goldilocks": "..."}
for label, desc in my_descriptions.items():
    tools = [
        Tool(name="search_docs", fn=search_docs, description=desc),
        # ... the other two unchanged ...
    ]
    bear = Bear(model=OpenRouterModel(), tools=tools)
    report = bear.run(Task(goal="Find the API spec for the /users endpoint."))
    picked = [s["tool_name"] for s in report.steps if s["type"] == "tool_call"]
    print(f"{label}: {picked}")
```

## What's next

[Lesson 4 — State and memory →](../04-state-and-memory/lesson.md)
