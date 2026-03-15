from barebear import Checkpoint, CheckpointManager, Task


def _make_task():
    return Task(goal="test goal", task_id="t1")


def test_checkpoint_creation():
    cp = Checkpoint(checkpoint_id="cp1", bear_id="b1", task=_make_task(), state={"x": 1})
    assert cp.checkpoint_id == "cp1"
    assert cp.status == "pending"
    assert cp.state == {"x": 1}


def test_approve():
    cp = Checkpoint(checkpoint_id="cp1", bear_id="b1", task=_make_task(), state={})
    cp.approve()
    assert cp.status == "approved"


def test_reject():
    cp = Checkpoint(checkpoint_id="cp1", bear_id="b1", task=_make_task(), state={})
    cp.reject()
    assert cp.status == "rejected"


def test_expire():
    cp = Checkpoint(checkpoint_id="cp1", bear_id="b1", task=_make_task(), state={})
    cp.expire()
    assert cp.status == "expired"


def test_to_dict_and_from_dict():
    cp = Checkpoint(checkpoint_id="cp1", bear_id="b1", task=_make_task(), state={"a": 1})
    d = cp.to_dict()
    restored = Checkpoint.from_dict(d)
    assert restored.checkpoint_id == "cp1"
    assert restored.state == {"a": 1}
    assert restored.task.goal == "test goal"


def test_to_json_roundtrip():
    cp = Checkpoint(checkpoint_id="cp1", bear_id="b1", task=_make_task(), state={})
    restored = Checkpoint.from_json(cp.to_json())
    assert restored.checkpoint_id == "cp1"


# --------------- CheckpointManager ---------------

class TestCheckpointManager:
    def test_create_and_get(self):
        mgr = CheckpointManager()
        cp = mgr.create(bear_id="b1", task=_make_task(), state={"k": "v"})
        assert mgr.get(cp.checkpoint_id) is cp

    def test_approve_changes_status(self):
        mgr = CheckpointManager()
        cp = mgr.create(bear_id="b1", task=_make_task(), state={})
        mgr.approve(cp.checkpoint_id)
        assert cp.status == "approved"

    def test_reject_changes_status(self):
        mgr = CheckpointManager()
        cp = mgr.create(bear_id="b1", task=_make_task(), state={})
        mgr.reject(cp.checkpoint_id)
        assert cp.status == "rejected"

    def test_pending_filter(self):
        mgr = CheckpointManager()
        cp1 = mgr.create(bear_id="b1", task=_make_task(), state={})
        cp2 = mgr.create(bear_id="b1", task=_make_task(), state={})
        mgr.approve(cp1.checkpoint_id)
        assert len(mgr.pending()) == 1
        assert mgr.pending()[0].checkpoint_id == cp2.checkpoint_id

    def test_all(self):
        mgr = CheckpointManager()
        mgr.create(bear_id="b1", task=_make_task(), state={})
        mgr.create(bear_id="b1", task=_make_task(), state={})
        assert len(mgr.all()) == 2

    def test_get_missing_raises(self):
        mgr = CheckpointManager()
        import pytest
        with pytest.raises(KeyError):
            mgr.get("nonexistent")

    def test_json_roundtrip(self):
        mgr = CheckpointManager()
        mgr.create(bear_id="b1", task=_make_task(), state={"x": 1})
        raw = mgr.to_json()
        restored = CheckpointManager.from_json(raw)
        assert len(restored.all()) == 1
