from src.agents.product_manager import ProductManagerAgent


class StubLLM:
    def __init__(self):
        self.last_kwargs = None

    def chat_json(self, **kwargs):
        self.last_kwargs = kwargs
        return {"ok": True}


def test_build_prd_json_uses_full_prd_schema_prompt():
    llm = StubLLM()
    agent = ProductManagerAgent(llm)  # type: ignore[arg-type]
    result = agent.build_prd_json({"title": "x"}, "demo")

    assert result == {"ok": True}
    assert llm.last_kwargs is not None
    prompt = llm.last_kwargs["user_prompt"]
    assert "product_vision" in prompt
    assert "user_scenarios" in prompt
    assert "non_functional_requirements" in prompt
    assert "prototype_description" in prompt
    assert "question_id" in prompt
