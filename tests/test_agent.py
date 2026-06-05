from app.runtime.graph import run_agent


def test_minimal_workflow_generates_memo_with_fallback(monkeypatch):
    monkeypatch.setenv("DISABLE_LIVE_LLM", "true")
    state = run_agent("NVDA")

    assert state["ticker"] == "NVDA"
    assert state["data"].ticker == "NVDA"
    assert state["market_chatter"].ticker == "NVDA"
    assert state["industry_position"].ticker == "NVDA"
    assert "prompt_context" in state
    assert "Market chatter" in state["prompt_context"]
    assert "Industry position" in state["prompt_context"]
    assert "Research view: Neutral" in state["memo"]
    assert state["errors"] == []
