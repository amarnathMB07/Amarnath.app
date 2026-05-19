from streamlit_app_successful import generate_assistant_response

def test_assistant_soil():
    resp = generate_assistant_response("Tell me about soil", "Wheat", {})
    assert "soil" in resp.lower()
    resp2 = generate_assistant_response("soil conditions", "Rice", {})
    assert "water-retentive" in resp2


def test_assistant_harvest():
    resp = generate_assistant_response("When will I harvest?", "Corn", {"harvest": "90-120 days"})
    assert "90-120" in resp


def test_assistant_unknown():
    resp = generate_assistant_response("What about tractors?", "Corn", {})
    assert "not sure" in resp.lower()


def test_greetings_and_help():
    assert "hello" in generate_assistant_response("Hi there", "Wheat", {}).lower()
    assert "welcome" in generate_assistant_response("Thanks", "Wheat", {}).lower()
    help_resp = generate_assistant_response("How do I use this?", "Wheat", {})
    assert "ask me about" in help_resp.lower()


def test_fertilizer_alternates():
    resp = generate_assistant_response("What fertilizer should I use?", "Wheat", {"fertilizer": "Nitrogen-rich (urea)"})
    assert "alternate" in resp.lower()
    assert "urea" in resp.lower()


def test_openai_call(monkeypatch):
    # simulate OpenAI API path with dummy response
    monkeypatch.setenv("OPENAI_API_KEY", "fake-key")
    import streamlit_app_successful as appmod

    class Dummy:
        @staticmethod
        def create(**kwargs):
            class Choice:
                def __init__(self):
                    self.message = type("M", (), {"content": "Dummy response"})
            return type("R", (), {"choices": [Choice()]})

    if not hasattr(appmod, "openai") or appmod.openai is None:
        class FakeOpenAI:
            ChatCompletion = type("X", (), {"create": Dummy.create})
        appmod.openai = FakeOpenAI
    else:
        monkeypatch.setattr(appmod.openai.ChatCompletion, "create", Dummy.create)

    resp = generate_assistant_response("Test question", "Wheat", {})
    assert resp == "Dummy response"

    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
