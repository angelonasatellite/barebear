# BareBear Examples

Each example runs with `MockModel` by default — no API keys needed.
Pass `--live` to use OpenAI, and `--verbose` for a full JSON trace.

```bash
export PYTHONPATH=src
```

## Research Assistant

Searches for information and synthesizes findings into a summary.

```bash
python examples/research_assistant/run.py
python examples/research_assistant/run.py --live --verbose
```

## Email Approval

Drafts a reply to a support ticket, then hits an approval gate when it tries to send.
Demonstrates `requires_approval` and checkpoint handling.

```bash
python examples/email_approval/run.py
python examples/email_approval/run.py --verbose
```

## File Patcher

Proposes code patches without applying them. The agent can read and propose,
but `apply_patch` is blocked by policy — side-effect staging in action.

```bash
python examples/file_patcher/run.py
python examples/file_patcher/run.py --verbose
```

## Ticket Triage

Classifies and routes a batch of support tickets. Shows budget tracking
across multiple tool calls.

```bash
python examples/ticket_triage/run.py
python examples/ticket_triage/run.py --verbose
```
