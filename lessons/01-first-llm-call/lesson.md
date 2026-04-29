# Lesson 1 — Your first LLM call

> **Learning outcomes**
> - Send a message to a real LLM and read its reply in code.
> - Explain the role of a *system prompt*, *user message*, and *assistant response*.
> - Describe what a *token* is and roughly how it is counted.

[Open this lesson in Colab →](https://colab.research.google.com/github/richey-malhotra/barebear/blob/main/lessons/01-first-llm-call/lesson.ipynb)

## The big idea

A Large Language Model (LLM) is a program that takes some text in and produces
some text out. That is the whole interface. When people talk about "AI agents",
they mean programs that wrap an LLM in a loop, give it tools, and let it act on
the world. Before any of that makes sense, you need to *use* an LLM directly.

So in Lesson 1 we use no framework at all. We send a message, we get a reply,
we look at what came back. Once that lands, every later lesson is just a
question of: *what wraps around this?*

## What you will build

A 10-line Python script that:

1. Connects to a real LLM through OpenRouter (free tier, no card required).
2. Sends a *system prompt* and a *user message*.
3. Prints the reply, the model name, and the token counts.

## Setup

You need exactly one thing: a free OpenRouter API key.

1. Go to <https://openrouter.ai>, sign in (GitHub or Google), open your dashboard.
2. Create a new key. The free tier requires no credit card.
3. Copy the key — it starts with `sk-or-`.

In Colab, paste the key when prompted. Locally:

```bash
export OPENROUTER_API_KEY=sk-or-...
```

## The code

```python
import os
from openai import OpenAI

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"],
)

response = client.chat.completions.create(
    model="meta-llama/llama-3.2-3b-instruct:free",
    messages=[
        {"role": "system", "content": "You are a helpful tutor. Keep answers short."},
        {"role": "user", "content": "What is a Large Language Model, in one sentence?"},
    ],
)

print(response.choices[0].message.content)
print("---")
print("model:", response.model)
print("prompt tokens:", response.usage.prompt_tokens)
print("completion tokens:", response.usage.completion_tokens)
```

## What just happened

- **`messages`** is the input — a list of role/content pairs. The `system`
  role tells the model who it is; the `user` role is what the user said.
- **`response.choices[0].message.content`** is the output — what the model
  said back.
- **`response.usage`** is the bill — how many tokens went in (`prompt_tokens`)
  and how many came out (`completion_tokens`). A token is roughly 3/4 of an
  English word. You pay (in money or rate-limit budget) per token in both
  directions.

That is the entire LLM API. Everything else — chat apps, agents, copilots,
search assistants — is built on top of these three things.

## The system prompt is the agent's personality

Try changing only the system prompt and re-running:

```python
"You are a Shakespearean poet. Answer only in iambic pentameter."
"You are a strict maths teacher. Demand the student show their working."
"You only respond in valid JSON."
```

Same model, same user message, totally different behaviour. The system prompt
is the closest thing an LLM has to a "personality" — and in later lessons,
when we build agents, we will be designing system prompts very deliberately.

## Exercise

Pick **one**:

1. Change the system prompt so the model behaves like a Year 12 / sophomore
   maths teacher walking a student through a quadratic equation.
2. Ask the same question with three different system prompts and compare the
   answers. Which prompt produced the most useful reply, and why?
3. Print the response with `response.usage.total_tokens`. Estimate the cost in
   tokens-per-character of the reply.

## Discussion

**Why did we not import barebear in Lesson 1?**
Because before you can understand what an *agent* is, you need to understand
what an *LLM call* is. An agent is just a program that calls the LLM in a
loop, gives it tools, and watches what it does. The framework comes in
Lesson 2.

**Why OpenRouter and not OpenAI / Anthropic / Google directly?**
OpenRouter is a single endpoint that routes to 200+ models, including free
ones. Same code, swap the model name, and you are talking to a different
provider. Less to set up, more flexibility for experimentation.

**What if the free model is unavailable?**
Free-tier models on OpenRouter rotate. If your call fails with "model not
available", swap `meta-llama/llama-3.2-3b-instruct:free` for any other
`*:free` model in the OpenRouter catalogue. The rest of the code is unchanged.

## What's next

[Lesson 2 — The agent loop →](../02-the-agent-loop/lesson.md)

In Lesson 2 we wrap this single call in a *loop* and give it a *tool*. That
is the moment a chat completion becomes an agent.
