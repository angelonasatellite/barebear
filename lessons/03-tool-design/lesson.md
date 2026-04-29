# Lesson 3 — Tool design

> **Learning outcomes**
> - Explain how an LLM "knows" what tools exist (the schema).
> - Predict which tool the model will pick for a given request.
> - Write a tool description that a model can use successfully.

> **Status:** notebook to follow. The lesson narrative below is complete.

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

## What's next

[Lesson 4 — State and memory →](../04-state-and-memory/lesson.md)
