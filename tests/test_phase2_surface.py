"""Tests for Phase 2 additions: trace mode, system_prompt, Reflect, bear-as-tool."""

import io

from barebear import Bear, Reflect, Reflection, Task, Tool
from barebear.models.base import ModelResponse
from barebear.testing import FakeModel


# ----------------- system_prompt on Task -----------------

def test_custom_system_prompt_replaces_default_persona():
    fake = FakeModel(mode="auto", final_text="Done.")
    bear = Bear(model=fake, tools=[])
    task = Task(goal="g", system_prompt="You are a Year 12 maths tutor.")
    bear.run(task)
    system_msg = bear._messages[0]
    assert system_msg["role"] == "system"
    assert "Year 12 maths tutor" in system_msg["content"]
    assert "You are a BareBear agent" not in system_msg["content"]


def test_no_system_prompt_uses_default_persona():
    fake = FakeModel(mode="auto", final_text="Done.")
    bear = Bear(model=fake, tools=[])
    bear.run(Task(goal="g"))
    system_msg = bear._messages[0]
    assert "You are a BareBear agent" in system_msg["content"]


# ----------------- Bear.run(trace=True) -----------------

def test_trace_mode_writes_to_stream():
    fake = FakeModel(mode="auto", final_text="All done.")
    search = Tool(name="search", fn=lambda query: "results", description="Search")
    bear = Bear(model=fake, tools=[search])
    buf = io.StringIO()
    bear.run(Task(goal="Find bears"), trace=True, trace_stream=buf)
    output = buf.getvalue()
    assert "BAREBEAR run" in output
    assert "turn 1" in output
    assert "search" in output
    assert "final answer" in output
    assert "status: completed" in output


def test_trace_off_writes_nothing():
    fake = FakeModel(mode="auto", final_text="Hi.")
    bear = Bear(model=fake, tools=[])
    buf = io.StringIO()
    bear.run(Task(goal="g"), trace=False, trace_stream=buf)
    assert buf.getvalue() == ""


# ----------------- Reflect -----------------

def test_reflect_critique_calls_model_once():
    fake = FakeModel(responses=[
        ModelResponse(content="Your answer is missing units.", prompt_tokens=10, completion_tokens=5),
    ])
    r = Reflect(model=fake)
    out = r.critique(goal="Compute area", answer="42")
    assert out == "Your answer is missing units."


def test_reflect_revise_calls_model_once():
    fake = FakeModel(responses=[
        ModelResponse(content="42 m^2", prompt_tokens=10, completion_tokens=3),
    ])
    r = Reflect(model=fake)
    out = r.revise(goal="Compute area", answer="42", critique="missing units")
    assert out == "42 m^2"


def test_reflect_run_returns_critique_and_revision():
    fake = FakeModel(responses=[
        ModelResponse(content="Missing units.", prompt_tokens=10, completion_tokens=5),
        ModelResponse(content="42 m^2", prompt_tokens=10, completion_tokens=3),
    ])
    r = Reflect(model=fake)
    result = r.run(goal="Compute area", answer="42")
    assert isinstance(result, Reflection)
    assert result.critique == "Missing units."
    assert result.revised == "42 m^2"
    assert result.critique_tokens == 15
    assert result.revision_tokens == 13


# ----------------- Bear.as_tool (multi-agent) -----------------

def test_bear_as_tool_returns_a_tool():
    fake = FakeModel(mode="auto", final_text="researched")
    inner = Bear(model=fake, tools=[])
    t = inner.as_tool(name="research", description="Research a topic")
    assert isinstance(t, Tool)
    assert t.name == "research"
    assert t.description == "Research a topic"


def test_bear_as_tool_invokes_inner_bear():
    inner_fake = FakeModel(mode="auto", final_text="climate facts gathered")
    inner = Bear(model=inner_fake, tools=[])
    research_tool = inner.as_tool(name="research", description="Research")

    outer_fake = FakeModel(mode="auto", final_text="report written")
    outer = Bear(model=outer_fake, tools=[research_tool])
    report = outer.run(Task(goal="Write a climate report"))

    assert report.status == "completed"
    tool_steps = [s for s in report.steps if s["type"] == "tool_call"]
    assert any(s["tool_name"] == "research" for s in tool_steps)
    assert any("climate facts gathered" in s.get("result", "") for s in tool_steps)


def test_bear_as_tool_isolates_state_across_calls():
    inner_fake = FakeModel(mode="auto", final_text="result-A")
    inner = Bear(model=inner_fake, tools=[])
    delegate = inner.as_tool(name="sub", description="Delegate")
    first = delegate.fn(goal="task A")
    inner_fake.reset()
    inner_fake._final_text = "result-B"
    second = delegate.fn(goal="task B")
    assert first == "result-A"
    assert second == "result-B"
