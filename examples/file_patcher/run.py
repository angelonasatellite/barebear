"""
File patcher: proposes code edits without applying them.
Demonstrates side-effect staging — propose_patch is allowed, apply_patch is blocked.

Run with:
    python examples/file_patcher/run.py                      # uses OpenRouter (default)
    python examples/file_patcher/run.py --provider ollama    # uses local Ollama
"""

import argparse
import json

from barebear import Bear, Task, Policy, Tool

# --- Sample file content the agent "reads" ---

SAMPLE_FILES = {
    "app/server.py": (
        "import flask\n"
        "\n"
        "app = flask.Flask(__name__)\n"
        "\n"
        "@ app.route('/health')\n"
        "def health():\n"
        "    return 'ok'\n"
        "\n"
        "@ app.route('/users')\n"
        "def get_users():\n"
        "    users = db.query('SELECT * FROM users')\n"
        "    return flask.jsonify(users)\n"
        "\n"
        "if __name__ == '__main__':\n"
        "    app.run(debug=True)\n"
    ),
    "app/utils.py": (
        "import os\n"
        "\n"
        "def load_config():\n"
        "    path = os.environ.get('CONFIG_PATH', 'config.yaml')\n"
        "    with open(path) as f:\n"
        "        return f.read()\n"
    ),
}

# Collects proposed patches so we can display them at the end
proposed_patches = []

# --- Tools ---


def read_file(path: str) -> str:
    content = SAMPLE_FILES.get(path)
    if content is None:
        return f"File not found: {path}"
    return content


def propose_patch(path: str, original: str, replacement: str) -> str:
    proposed_patches.append({"path": path, "original": original, "replacement": replacement})
    return f"Patch #{len(proposed_patches)} staged for {path} (not yet applied)."


def apply_patch(path: str, original: str, replacement: str) -> str:
    # Would write to disk in real usage. Policy blocks it in this example.
    return f"Applied patch to {path}."


def make_model(provider: str):
    if provider == "ollama":
        from barebear import OllamaModel
        return OllamaModel()
    from barebear import OpenRouterModel
    return OpenRouterModel()


def main():
    parser = argparse.ArgumentParser(description="File patcher (side-effect staging)")
    parser.add_argument(
        "--provider",
        choices=["openrouter", "ollama"],
        default="openrouter",
        help="Model backend (default: openrouter)",
    )
    parser.add_argument("--verbose", action="store_true", help="Print full JSON trace")
    args = parser.parse_args()

    tools = [
        Tool(name="read_file", fn=read_file,
             description="Read source file contents"),
        Tool(name="propose_patch", fn=propose_patch,
             description="Propose a patch (staged, not applied)"),
        Tool(name="apply_patch", fn=apply_patch,
             description="Apply a patch to disk",
             risk="high", side_effects="filesystem", requires_approval=True),
    ]

    policy = Policy(
        max_steps=12,
        max_tool_calls=10,
        max_cost_usd=0.50,
        blocked_tools=["apply_patch"],
        allow_external_side_effects=False,
    )

    model = make_model(args.provider)

    bear = Bear(model=model, tools=tools, policy=policy)
    task = Task(
        goal=(
            "Review app/server.py for issues. "
            "Propose patches for any problems you find (SQL injection, debug mode, etc). "
            "Do NOT apply them — only propose."
        ),
        input={"files": list(SAMPLE_FILES.keys())},
    )

    result = bear.run(task)

    print("=" * 60)
    print("FILE PATCHER REPORT")
    print("=" * 60)
    print(result.summary())

    if proposed_patches:
        print(f"\n--- {len(proposed_patches)} Proposed Patch(es) ---")
        for i, patch in enumerate(proposed_patches, 1):
            print(f"\nPatch #{i} — {patch['path']}")
            print(f"  - original:    {patch['original'][:80]}{'...' if len(patch['original']) > 80 else ''}")
            print(f"  + replacement: {patch['replacement'][:80]}{'...' if len(patch['replacement']) > 80 else ''}")
    else:
        print("\nNo patches were proposed.")

    if args.verbose:
        print("\n--- JSON Trace ---")
        print(json.dumps(result.to_json(), indent=2))


if __name__ == "__main__":
    main()
