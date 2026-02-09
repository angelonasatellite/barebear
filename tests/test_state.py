from barebear import State


def test_set_and_get():
    s = State()
    s.set("key", "value")
    assert s.get("key") == "value"


def test_get_missing_returns_default():
    s = State()
    assert s.get("nope") is None
    assert s.get("nope", 42) == 42


def test_delete():
    s = State()
    s.set("x", 1)
    s.delete("x")
    assert s.get("x") is None


def test_delete_nonexistent_is_noop():
    s = State()
    s.delete("missing")  # should not raise


def test_snapshot_returns_frozen_copy():
    s = State()
    s.set("a", [1, 2, 3])
    snap = s.snapshot()
    assert snap["data"]["a"] == [1, 2, 3]
    assert "timestamp" in snap


def test_snapshot_not_affected_by_later_changes():
    s = State()
    s.set("a", {"nested": True})
    snap = s.snapshot()
    s.set("a", {"nested": False})
    s.set("b", "new")
    assert snap["data"]["a"] == {"nested": True}
    assert "b" not in snap["data"]


def test_history_tracks_snapshots():
    s = State()
    s.set("x", 1)
    s.snapshot()
    s.set("x", 2)
    s.snapshot()
    assert len(s.history()) == 2
    assert s.history()[0]["data"]["x"] == 1
    assert s.history()[1]["data"]["x"] == 2


def test_initial_state():
    s = State(initial={"a": 1, "b": 2})
    assert s.get("a") == 1
    assert s.get("b") == 2


def test_changes_tracked():
    s = State()
    s.set("k", "v")
    s.delete("k")
    changes = s.changes()
    assert len(changes) == 2
    assert changes[0]["action"] == "set"
    assert changes[1]["action"] == "delete"
