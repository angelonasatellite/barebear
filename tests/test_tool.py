import pytest

from barebear import Tool, ToolRegistry


def test_tool_creation():
    t = Tool(name="t", fn=lambda: None, description="desc", risk="low")
    assert t.name == "t"
    assert t.description == "desc"
    assert t.risk == "low"


def test_tool_execution():
    t = Tool(name="add", fn=lambda a, b: int(a) + int(b), description="add")
    assert t.fn(a="2", b="3") == 5


def test_to_openai_schema():
    t = Tool(name="search", fn=lambda query: query, description="Search things")
    schema = t.to_openai_schema()
    assert schema["type"] == "function"
    func = schema["function"]
    assert func["name"] == "search"
    assert func["description"] == "Search things"
    assert "query" in func["parameters"]["properties"]
    assert "query" in func["parameters"]["required"]


def test_schema_preserves_type_annotations():
    def calc(count: int, ratio: float, active: bool, name: str) -> str:
        return ""

    t = Tool(name="calc", fn=calc, description="Calculate")
    schema = t.to_openai_schema()
    props = schema["function"]["parameters"]["properties"]
    assert props["count"]["type"] == "integer"
    assert props["ratio"]["type"] == "number"
    assert props["active"]["type"] == "boolean"
    assert props["name"]["type"] == "string"


def test_to_schema():
    t = Tool(name="t", fn=lambda: None, description="d", risk="high", side_effects="external")
    s = t.to_schema()
    assert s["name"] == "t"
    assert s["risk"] == "high"
    assert s["side_effects"] == "external"


# --------------- ToolRegistry ---------------

class TestToolRegistry:
    def test_register_and_get(self):
        reg = ToolRegistry()
        t = Tool(name="x", fn=lambda: None)
        reg.register(t)
        assert reg.get("x") is t

    def test_contains(self):
        reg = ToolRegistry()
        reg.register(Tool(name="x", fn=lambda: None))
        assert "x" in reg
        assert "y" not in reg

    def test_list_tools(self):
        reg = ToolRegistry()
        reg.register(Tool(name="a", fn=lambda: None))
        reg.register(Tool(name="b", fn=lambda: None))
        assert len(reg.list_tools()) == 2

    def test_duplicate_raises(self):
        reg = ToolRegistry()
        reg.register(Tool(name="x", fn=lambda: None))
        with pytest.raises(ValueError, match="already registered"):
            reg.register(Tool(name="x", fn=lambda: None))

    def test_get_missing_raises(self):
        reg = ToolRegistry()
        with pytest.raises(KeyError, match="not found"):
            reg.get("nope")

    def test_len(self):
        reg = ToolRegistry()
        assert len(reg) == 0
        reg.register(Tool(name="a", fn=lambda: None))
        assert len(reg) == 1

    def test_names(self):
        reg = ToolRegistry()
        reg.register(Tool(name="a", fn=lambda: None))
        reg.register(Tool(name="b", fn=lambda: None))
        assert set(reg.names()) == {"a", "b"}
