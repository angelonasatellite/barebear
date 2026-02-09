import pytest

from barebear import Budget, Policy
from barebear.exceptions import BudgetExceeded


def test_tracks_steps():
    b = Budget(Policy(max_steps=100))
    b.record_step()
    b.record_step()
    assert b.steps == 2


def test_tracks_tokens():
    b = Budget(Policy())
    b.record_tokens(100, 50, cost=0.01)
    assert b.prompt_tokens == 100
    assert b.completion_tokens == 50
    assert b.total_tokens == 150
    assert b.total_cost_usd == pytest.approx(0.01)


def test_tracks_tool_calls():
    b = Budget(Policy(max_tool_calls=100))
    b.record_tool_call()
    b.record_tool_call()
    assert b.tool_calls == 2


def test_step_limit_exceeded():
    b = Budget(Policy(max_steps=1))
    b.record_step()  # 1 — at limit
    with pytest.raises(BudgetExceeded, match="steps"):
        b.record_step()  # 2 — over limit, raises immediately


def test_tool_call_limit_exceeded():
    b = Budget(Policy(max_tool_calls=1))
    b.record_tool_call()
    with pytest.raises(BudgetExceeded, match="tool_calls"):
        b.record_tool_call()


def test_token_limit_exceeded():
    b = Budget(Policy(max_tokens=100))
    with pytest.raises(BudgetExceeded, match="tokens"):
        b.record_tokens(80, 30)


def test_cost_limit_exceeded():
    b = Budget(Policy(max_cost_usd=0.05))
    with pytest.raises(BudgetExceeded, match="cost_usd"):
        b.record_tokens(0, 0, cost=0.06)


def test_summary():
    b = Budget(Policy(max_steps=10, max_tool_calls=5, max_tokens=1000, max_cost_usd=1.0))
    b.record_step()
    b.record_tokens(50, 25, cost=0.005)
    b.record_tool_call()
    s = b.summary()
    assert s["steps"] == 1
    assert s["tool_calls"] == 1
    assert s["total_tokens"] == 75
    assert s["total_cost_usd"] == pytest.approx(0.005)
    assert s["limits"]["max_steps"] == 10


def test_check_passes_within_limits():
    b = Budget(Policy(max_steps=10))
    b.record_step()
    b.check()  # should not raise
