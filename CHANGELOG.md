# Changelog

All notable changes to BareBear will be documented in this file.

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
- 83 passing tests
