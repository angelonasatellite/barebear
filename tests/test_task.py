from barebear import Task


def test_task_defaults():
    t = Task(goal="Do something")
    assert t.goal == "Do something"
    assert t.input == {}
    assert t.context == ""


def test_task_id_auto_generated():
    t = Task(goal="test")
    assert isinstance(t.task_id, str)
    assert len(t.task_id) == 8


def test_task_custom_id():
    t = Task(goal="test", task_id="custom-123")
    assert t.task_id == "custom-123"


def test_task_unique_ids():
    ids = {Task(goal="test").task_id for _ in range(50)}
    assert len(ids) == 50


def test_task_to_dict():
    t = Task(goal="g", input={"k": "v"}, context="ctx", task_id="abc")
    d = t.to_dict()
    assert d == {"task_id": "abc", "goal": "g", "input": {"k": "v"}, "context": "ctx"}
