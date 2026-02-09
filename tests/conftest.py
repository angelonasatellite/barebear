import pytest

from barebear import Bear, MockModel, Policy, Task, Tool
from barebear.models.base import ModelResponse


# --------------- Tools ---------------

@pytest.fixture
def search_tool():
    return Tool(name="search", fn=lambda query: f"results for {query}", description="Search the web")


@pytest.fixture
def write_tool():
    return Tool(name="write_file", fn=lambda path, content: f"wrote {path}", description="Write a file")


@pytest.fixture
def send_email_tool():
    return Tool(
        name="send_email",
        fn=lambda to, body: f"sent to {to}",
        description="Send an email",
        side_effects="external",
        requires_approval=True,
    )


@pytest.fixture
def blocked_tool():
    return Tool(name="delete_all", fn=lambda: "deleted", description="Delete everything", risk="high")


# --------------- Policies ---------------

@pytest.fixture
def default_policy():
    return Policy()


@pytest.fixture
def strict_policy():
    return Policy(
        max_steps=3,
        max_tool_calls=2,
        max_cost_usd=0.10,
        require_approval_for=["send_email"],
        blocked_tools=["delete_all"],
    )


# --------------- Tasks ---------------

@pytest.fixture
def simple_task():
    return Task(goal="Say hello")


@pytest.fixture
def search_task():
    return Task(goal="Search for bears", input={"query": "bears"}, context="wildlife research")


# --------------- Models ---------------

@pytest.fixture
def auto_mock():
    return MockModel(mode="auto", final_text="Done.")


@pytest.fixture
def scripted_mock():
    return MockModel(responses=[
        ModelResponse(content="Step one done.", prompt_tokens=10, completion_tokens=5),
        ModelResponse(content="All done.", prompt_tokens=10, completion_tokens=5),
    ])


# --------------- Bears ---------------

@pytest.fixture
def basic_bear(auto_mock, search_tool):
    return Bear(model=auto_mock, tools=[search_tool])


@pytest.fixture
def strict_bear(auto_mock, search_tool, strict_policy):
    return Bear(model=auto_mock, tools=[search_tool], policy=strict_policy)
