import json

from barebear import Report


def test_report_defaults():
    r = Report(task_id="abc")
    assert r.task_id == "abc"
    assert r.status == "completed"
    assert r.steps == []


def test_add_step():
    r = Report(task_id="abc")
    r.add_step("tool_call", "called search", tool_name="search", result="ok")
    assert len(r.steps) == 1
    assert r.steps[0]["step_number"] == 1
    assert r.steps[0]["type"] == "tool_call"
    assert r.steps[0]["tool_name"] == "search"
    assert r.steps[0]["result"] == "ok"


def test_step_numbering():
    r = Report(task_id="t")
    r.add_step("a", "first")
    r.add_step("b", "second")
    assert r.steps[0]["step_number"] == 1
    assert r.steps[1]["step_number"] == 2


def test_to_dict():
    r = Report(task_id="t", status="failed", error="boom")
    d = r.to_dict()
    assert d["task_id"] == "t"
    assert d["status"] == "failed"
    assert d["error"] == "boom"


def test_to_json():
    r = Report(task_id="t")
    j = r.to_json()
    parsed = json.loads(j)
    assert parsed["task_id"] == "t"


def test_summary_contains_key_fields():
    r = Report(task_id="abc", status="completed", total_tokens=500, total_cost_usd=0.01)
    r.add_step("response", "hello world")
    r.final_output = "hello world"
    text = r.summary()
    assert "abc" in text
    assert "completed" in text
    assert "500" in text
    assert "hello world" in text


def test_summary_shows_error():
    r = Report(task_id="t", status="failed", error="something broke")
    text = r.summary()
    assert "something broke" in text
