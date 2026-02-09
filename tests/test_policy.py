from barebear import Policy, Tool


def test_default_values():
    p = Policy()
    assert p.max_steps == 20
    assert p.max_tool_calls == 10
    assert p.max_cost_usd == 1.0
    assert p.max_tokens == 50000
    assert p.blocked_tools == []
    assert p.require_approval_for == []
    assert p.allow_external_side_effects is False


def test_check_tool_allowed():
    p = Policy()
    t = Tool(name="search", fn=lambda: None, description="search")
    allowed, reason = p.check_tool(t)
    assert allowed is True
    assert reason == "allowed"


def test_check_tool_blocked():
    p = Policy(blocked_tools=["danger"])
    t = Tool(name="danger", fn=lambda: None)
    allowed, reason = p.check_tool(t)
    assert allowed is False
    assert "blocked" in reason


def test_check_tool_needs_approval_by_name():
    p = Policy(require_approval_for=["deploy"])
    t = Tool(name="deploy", fn=lambda: None)
    allowed, reason = p.check_tool(t)
    assert allowed is False
    assert "requires approval" in reason


def test_check_tool_needs_approval_by_flag():
    p = Policy()
    t = Tool(name="deploy", fn=lambda: None, requires_approval=True)
    allowed, reason = p.check_tool(t)
    assert allowed is False
    assert "requires approval" in reason


def test_external_side_effects_blocked():
    p = Policy(allow_external_side_effects=False)
    t = Tool(name="email", fn=lambda: None, side_effects="external")
    allowed, reason = p.check_tool(t)
    assert allowed is False
    assert "side effects" in reason


def test_external_side_effects_allowed():
    p = Policy(allow_external_side_effects=True)
    t = Tool(name="email", fn=lambda: None, side_effects="external")
    allowed, reason = p.check_tool(t)
    assert allowed is True


def test_is_blocked():
    p = Policy(blocked_tools=["bad"])
    assert p.is_blocked(Tool(name="bad", fn=lambda: None)) is True
    assert p.is_blocked(Tool(name="good", fn=lambda: None)) is False


def test_needs_approval():
    p = Policy(require_approval_for=["deploy"])
    assert p.needs_approval(Tool(name="deploy", fn=lambda: None)) is True
    assert p.needs_approval(Tool(name="search", fn=lambda: None)) is False


def test_to_prompt_text():
    p = Policy(max_steps=5, blocked_tools=["rm"], require_approval_for=["deploy"])
    text = p.to_prompt_text()
    assert "Max steps: 5" in text
    assert "rm" in text
    assert "deploy" in text
    assert "External side effects are NOT allowed" in text


def test_to_dict():
    p = Policy(max_steps=3)
    d = p.to_dict()
    assert d["max_steps"] == 3
    assert isinstance(d["blocked_tools"], list)
