# Changelog

All notable changes to BareBear will be documented in this file.

## 0.1.1 (2026-03-16)

### Fixed

- `tool.to_openai_schema()` now maps Python type annotations to correct JSON Schema types instead of defaulting everything to `"string"`
- Mock model schema validation no longer marks all parameters as required
- Uncertainty extraction is now wired into the agent loop — model-response text is scanned for hedging language and assumptions are tracked automatically
- Resolved all pyright strict-mode type errors in `bear.py`

### Changed

- Test suite expanded from 83 to 86 tests

## 0.1.0 (2026-03-15)

First public release.

### Added

- Core primitives: Bear, Task, State, Tool, Policy, Checkpoint, Report
- Model adapters: OpenAI, Mock
- Policy-first tool execution with pre-call enforcement
- Budget tracking (steps, tool calls, tokens, cost)
- Checkpoint/approval system for high-risk actions
- Side-effect declarations on tools (`none`, `internal`, `external`)
- Run receipts with full step traces, assumptions, and uncertainties
- Honest uncertainty tracking (missing information, confidence, assumptions)
- 4 runnable examples: research assistant, email approval, file patcher, ticket triage
- 86 passing tests
