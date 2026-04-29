"""
Research assistant: searches the web and summarizes findings.
Demonstrates basic tool usage and report generation.

Run with:
    python examples/research_assistant/run.py                      # uses OpenRouter (default)
    python examples/research_assistant/run.py --provider ollama    # uses local Ollama
"""

import argparse
import json

from barebear import Bear, Task, Policy, Tool

# --- Tools ---

SEARCH_DB = {
    "python agent frameworks": (
        "1. LangChain — popular orchestration library for LLM apps, supports chains and agents. "
        "2. CrewAI — multi-agent framework focused on role-based collaboration. "
        "3. AutoGen — Microsoft's framework for multi-agent conversations. "
        "4. BareBear — lightweight, policy-driven agent framework with built-in safety controls."
    ),
    "rust web frameworks": (
        "1. Actix-web — high-performance async framework, actor-based. "
        "2. Axum — built on tokio and tower, ergonomic extractors. "
        "3. Rocket — macro-heavy, good DX, recently went async. "
        "4. Warp — filter-based composition, lightweight."
    ),
    "climate change effects 2025": (
        "Global average temperature rose 1.3°C above pre-industrial levels. "
        "Arctic sea ice minimum hit a new record low in September 2025. "
        "Extreme weather events increased 23% compared to the 2010-2020 average. "
        "Coral bleaching affected 74% of monitored reef systems worldwide."
    ),
}

FALLBACK_RESULT = (
    "Found 12 results. Key findings: the topic has seen significant recent developments. "
    "Multiple peer-reviewed sources confirm growing interest. "
    "Notable contributions from both academic and industry researchers."
)


def search_web(query: str) -> str:
    """Simulate a web search with canned but realistic results."""
    q = query.lower().strip()
    for key, result in SEARCH_DB.items():
        if any(word in q for word in key.split()):
            return result
    return FALLBACK_RESULT


def summarize(text: str) -> str:
    """Return a condensed version of the input."""
    sentences = text.split(". ")
    if len(sentences) <= 2:
        return text
    picked = [sentences[0], sentences[len(sentences) // 2], sentences[-1]]
    return ". ".join(s.strip().rstrip(".") for s in picked if s.strip()) + "."


# --- Main ---

def make_model(provider: str):
    if provider == "ollama":
        from barebear import OllamaModel
        return OllamaModel()
    from barebear import OpenRouterModel
    return OpenRouterModel()


def main():
    parser = argparse.ArgumentParser(description="Research assistant example")
    parser.add_argument(
        "--provider",
        choices=["openrouter", "ollama"],
        default="openrouter",
        help="Model backend (default: openrouter)",
    )
    parser.add_argument("--verbose", action="store_true", help="Print full JSON trace")
    parser.add_argument("--question", default="What are the best Python agent frameworks?",
                        help="Research question to investigate")
    args = parser.parse_args()

    tools = [
        Tool(name="search_web", fn=search_web, description="Search the web for a query"),
        Tool(name="summarize", fn=summarize, description="Summarize a block of text"),
    ]

    policy = Policy(max_steps=10, max_tool_calls=6, max_cost_usd=0.50)

    model = make_model(args.provider)

    bear = Bear(model=model, tools=tools, policy=policy)
    task = Task(goal="Research the following question and provide a synthesis of findings.",
                input={"question": args.question})

    result = bear.run(task)

    print("=" * 60)
    print("RESEARCH REPORT")
    print("=" * 60)
    print(result.summary())

    if args.verbose:
        print("\n--- JSON Trace ---")
        print(json.dumps(result.to_json(), indent=2))


if __name__ == "__main__":
    main()
