from barebear.models.base import ModelResponse
from barebear.testing import FakeModel


def test_auto_mode_calls_tools_then_text():
    fake = FakeModel(mode="auto", final_text="Done.")
    tools = [{"function": {"name": "search", "description": "s", "parameters": {"type": "object", "properties": {}, "required": []}}}]

    r1 = fake.complete([], tools=tools)
    assert len(r1.tool_calls) == 1
    assert r1.tool_calls[0]["name"] == "search"

    r2 = fake.complete([], tools=tools)
    assert r2.content == "Done."
    assert r2.tool_calls == []


def test_auto_mode_no_tools_returns_text():
    fake = FakeModel(mode="auto", final_text="Nothing to do.")
    r = fake.complete([], tools=None)
    assert r.content == "Nothing to do."


def test_scripted_mode():
    fake = FakeModel(responses=[
        ModelResponse(content="first", prompt_tokens=5, completion_tokens=3),
        ModelResponse(content="second", prompt_tokens=5, completion_tokens=3),
    ])
    r1 = fake.complete([])
    r2 = fake.complete([])
    assert r1.content == "first"
    assert r2.content == "second"


def test_scripted_exhausted():
    fake = FakeModel(responses=[ModelResponse(content="only")])
    fake.complete([])
    r = fake.complete([])
    assert "No more scripted" in r.content


def test_reset_clears_state():
    fake = FakeModel(mode="auto", final_text="Done.")
    tools = [{"function": {"name": "t", "description": "", "parameters": {"type": "object", "properties": {}, "required": []}}}]
    fake.complete([], tools=tools)
    fake.reset()
    assert fake._call_count == 0
    assert fake._tools_called == []
    r = fake.complete([], tools=tools)
    assert len(r.tool_calls) == 1


def test_auto_with_multiple_tools():
    fake = FakeModel(mode="auto", final_text="All done.")
    tools = [
        {"function": {"name": "a", "description": "", "parameters": {"type": "object", "properties": {}, "required": []}}},
        {"function": {"name": "b", "description": "", "parameters": {"type": "object", "properties": {}, "required": []}}},
    ]
    r1 = fake.complete([], tools=tools)
    assert r1.tool_calls[0]["name"] == "a"
    r2 = fake.complete([], tools=tools)
    assert r2.tool_calls[0]["name"] == "b"
    r3 = fake.complete([], tools=tools)
    assert r3.content == "All done."
