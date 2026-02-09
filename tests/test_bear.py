import pytest

from barebear import Bear, MockModel, Policy, Task, Tool
from barebear.models.base import ModelResponse


def test_basic_run_completes():
    mock = MockModel(mode="auto", final_text="Hello!")
    bear = Bear(model=mock, tools=[])
    report = bear.run(Task(goal="Say hi"))
    assert report.status == "completed"
    assert report.final_output == "Hello!"


def test_run_with_tool_calls():
    search = Tool(name="search", fn=lambda query: f"results for {query}", description="Search")
    mock = MockModel(mode="auto", final_text="Found it.")
    bear = Bear(model=mock, tools=[search])
    report = bear.run(Task(goal="Find bears"))
    assert report.status == "completed"
    # Should have a tool_call step and a final response step
    types = [s["type"] for s in report.steps]
    assert "tool_call" in types
    assert "response" in types


def test_policy_blocks_tool():
    bad_tool = Tool(name="danger", fn=lambda: "boom", description="dangerous")
    mock = MockModel(mode="auto", final_text="Ok.")
    policy = Policy(blocked_tools=["danger"])
    bear = Bear(model=mock, tools=[bad_tool], policy=policy)
    report = bear.run(Task(goal="Do something"))
    # The model will try to call the blocked tool, get blocked, then return text
    types = [s["type"] for s in report.steps]
    assert "policy_block" in types
    assert report.status == "completed"


def test_budget_exceeded_stops_run():
    mock = MockModel(mode="auto", final_text="Done.")
    policy = Policy(max_steps=1)
    search = Tool(name="search", fn=lambda query: "results", description="Search")
    bear = Bear(model=mock, tools=[search], policy=policy)
    report = bear.run(Task(goal="Too many steps"))
    assert report.status == "budget_exceeded"


def test_approval_pauses_run():
    email_tool = Tool(name="send_email", fn=lambda to, body: "sent", description="Send email")
    mock = MockModel(mode="auto", final_text="Done.")
    policy = Policy(require_approval_for=["send_email"])
    bear = Bear(model=mock, tools=[email_tool], policy=policy)
    report = bear.run(Task(goal="Send an email"))
    assert report.status == "paused"
    assert report.checkpoint_id is not None
    # Checkpoint should exist in manager
    cp = bear.checkpoints.get(report.checkpoint_id)
    assert cp.status == "pending"


def test_plan_mode():
    mock = MockModel(mode="auto", final_text="Plan: step 1, step 2")
    bear = Bear(model=mock, tools=[])
    plan = bear.plan(Task(goal="Plan something"))
    assert "task_id" in plan
    assert "plan" in plan
    assert isinstance(plan["plan"], str)


def test_report_receipt_generated():
    mock = MockModel(mode="auto", final_text="Done.")
    bear = Bear(model=mock, tools=[])
    report = bear.run(Task(goal="Quick task"))
    text = report.summary()
    assert "BAREBEAR RUN REPORT" in text
    assert "completed" in text


def test_multiple_tools_called_in_sequence():
    tool_a = Tool(name="step_one", fn=lambda: "a done", description="First step")
    tool_b = Tool(name="step_two", fn=lambda: "b done", description="Second step")
    mock = MockModel(mode="auto", final_text="All done.")
    bear = Bear(model=mock, tools=[tool_a, tool_b])
    report = bear.run(Task(goal="Do two things"))
    assert report.status == "completed"
    tool_steps = [s for s in report.steps if s["type"] == "tool_call"]
    tool_names = [s["tool_name"] for s in tool_steps]
    assert "step_one" in tool_names
    assert "step_two" in tool_names


def test_run_with_scripted_model():
    mock = MockModel(responses=[
        ModelResponse(content="All done.", prompt_tokens=10, completion_tokens=5),
    ])
    bear = Bear(model=mock, tools=[])
    report = bear.run(Task(goal="Simple"))
    assert report.status == "completed"
    assert report.final_output == "All done."


def test_bear_has_checkpoint_manager():
    bear = Bear(model=MockModel(mode="auto"), tools=[])
    assert bear.checkpoints is not None
    assert len(bear.checkpoints.all()) == 0


def test_state_accessible():
    bear = Bear(model=MockModel(mode="auto"), tools=[])
    bear.state.set("greeting", "hi")
    assert bear.state.get("greeting") == "hi"


def test_custom_bear_id():
    bear = Bear(model=MockModel(mode="auto"), tools=[], bear_id="bear-42")
    assert bear.bear_id == "bear-42"
