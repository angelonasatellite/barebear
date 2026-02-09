from barebear import MockModel
from barebear.models.base import ModelResponse


def test_auto_mode_calls_tools_then_text():
    mock = MockModel(mode="auto", final_text="Done.")
    tools = [{"function": {"name": "search", "description": "s", "parameters": {"type": "object", "properties": {}, "required": []}}}]

    # First call should produce a tool call
    r1 = mock.complete([], tools=tools)
    assert len(r1.tool_calls) == 1
    assert r1.tool_calls[0]["name"] == "search"

    # Second call: all tools called, should return text
    r2 = mock.complete([], tools=tools)
    assert r2.content == "Done."
    assert r2.tool_calls == []


def test_auto_mode_no_tools_returns_text():
    mock = MockModel(mode="auto", final_text="Nothing to do.")
    r = mock.complete([], tools=None)
    assert r.content == "Nothing to do."


def test_scripted_mode():
    mock = MockModel(responses=[
        ModelResponse(content="first", prompt_tokens=5, completion_tokens=3),
        ModelResponse(content="second", prompt_tokens=5, completion_tokens=3),
    ])
    r1 = mock.complete([])
    r2 = mock.complete([])
    assert r1.content == "first"
    assert r2.content == "second"


def test_scripted_exhausted():
    mock = MockModel(responses=[ModelResponse(content="only")])
    mock.complete([])
    r = mock.complete([])
    assert "No more scripted" in r.content


def test_reset_clears_state():
    mock = MockModel(mode="auto", final_text="Done.")
    tools = [{"function": {"name": "t", "description": "", "parameters": {"type": "object", "properties": {}, "required": []}}}]
    mock.complete([], tools=tools)  # calls tool "t"
    mock.reset()
    assert mock._call_count == 0
    assert mock._tools_called == []
    # After reset, should try tool again
    r = mock.complete([], tools=tools)
    assert len(r.tool_calls) == 1


def test_auto_with_multiple_tools():
    mock = MockModel(mode="auto", final_text="All done.")
    tools = [
        {"function": {"name": "a", "description": "", "parameters": {"type": "object", "properties": {}, "required": []}}},
        {"function": {"name": "b", "description": "", "parameters": {"type": "object", "properties": {}, "required": []}}},
    ]
    r1 = mock.complete([], tools=tools)
    assert r1.tool_calls[0]["name"] == "a"
    r2 = mock.complete([], tools=tools)
    assert r2.tool_calls[0]["name"] == "b"
    r3 = mock.complete([], tools=tools)
    assert r3.content == "All done."
