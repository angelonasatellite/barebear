"""BAREBEAR_MODEL env var support on OpenRouterModel and OllamaModel."""

from unittest.mock import patch

from barebear import OllamaModel, OpenRouterModel


@patch("openai.OpenAI")
def test_openrouter_uses_explicit_model_arg(_oai):
    m = OpenRouterModel(model="explicit/m1", api_key="sk-test")
    assert m._model == "explicit/m1"


@patch.dict("os.environ", {"BAREBEAR_MODEL": "from-env/m2", "OPENROUTER_API_KEY": "sk-test"}, clear=False)
@patch("openai.OpenAI")
def test_openrouter_falls_back_to_env_var(_oai):
    m = OpenRouterModel()
    assert m._model == "from-env/m2"


@patch.dict("os.environ", {"OPENROUTER_API_KEY": "sk-test"}, clear=False)
@patch("openai.OpenAI")
def test_openrouter_falls_back_to_default_when_neither_set(_oai, monkeypatch):
    monkeypatch.delenv("BAREBEAR_MODEL", raising=False)
    m = OpenRouterModel()
    assert m._model == OpenRouterModel.DEFAULT_MODEL


@patch("openai.OpenAI")
def test_openrouter_explicit_arg_beats_env_var(_oai, monkeypatch):
    monkeypatch.setenv("BAREBEAR_MODEL", "from-env/m3")
    monkeypatch.setenv("OPENROUTER_API_KEY", "sk-test")
    m = OpenRouterModel(model="explicit/m4")
    assert m._model == "explicit/m4"


@patch("openai.OpenAI")
def test_ollama_uses_explicit_model_arg(_oai):
    m = OllamaModel(model="explicit:llama")
    assert m._model == "explicit:llama"


@patch("openai.OpenAI")
def test_ollama_falls_back_to_env_var(_oai, monkeypatch):
    monkeypatch.setenv("BAREBEAR_MODEL", "qwen2.5:7b")
    m = OllamaModel()
    assert m._model == "qwen2.5:7b"


@patch("openai.OpenAI")
def test_ollama_falls_back_to_default_when_neither_set(_oai, monkeypatch):
    monkeypatch.delenv("BAREBEAR_MODEL", raising=False)
    m = OllamaModel()
    assert m._model == OllamaModel.DEFAULT_MODEL


@patch("openai.OpenAI")
def test_ollama_explicit_arg_beats_env_var(_oai, monkeypatch):
    monkeypatch.setenv("BAREBEAR_MODEL", "qwen2.5:7b")
    m = OllamaModel(model="explicit:tinyllama")
    assert m._model == "explicit:tinyllama"
