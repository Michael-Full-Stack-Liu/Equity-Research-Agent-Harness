from __future__ import annotations

from langgraph.graph import END, START, StateGraph

from app.runtime.llm import draft_memo_with_gemini
from app.runtime.prompting import build_memo_prompt, build_prompt_context
from app.runtime.research_context import analyze_industry_position, investigate_market_chatter
from app.runtime.state import AgentState
from app.runtime.tools.collect import collect_ticker_data


def validate_ticker(state: AgentState) -> AgentState:
    ticker = state.get("ticker", "").strip().upper()
    errors = list(state.get("errors", []))
    if not ticker:
        errors.append("ticker is required")
    return {"ticker": ticker, "errors": errors}


def collect_data(state: AgentState) -> AgentState:
    if state.get("errors"):
        return {}
    return {"data": collect_ticker_data(state["ticker"])}


def investigate_chatter(state: AgentState) -> AgentState:
    return {"market_chatter": investigate_market_chatter(state["data"])}


def analyze_industry(state: AgentState) -> AgentState:
    return {"industry_position": analyze_industry_position(state["data"])}


def build_context(state: AgentState) -> AgentState:
    return {
        "prompt_context": build_prompt_context(
            state["data"],
            state["market_chatter"],
            state["industry_position"],
        )
    }


def draft_memo(state: AgentState) -> AgentState:
    prompt = build_memo_prompt(state["prompt_context"])
    return {"memo": draft_memo_with_gemini(prompt)}


def finalize(state: AgentState) -> AgentState:
    errors = list(state.get("errors", []))
    if not state.get("memo"):
        errors.append("memo was not generated")
    return {"errors": errors}


def build_graph():
    graph = StateGraph(AgentState)
    graph.add_node("validate_ticker", validate_ticker)
    graph.add_node("collect_data", collect_data)
    graph.add_node("investigate_chatter", investigate_chatter)
    graph.add_node("analyze_industry", analyze_industry)
    graph.add_node("build_context", build_context)
    graph.add_node("draft_memo", draft_memo)
    graph.add_node("finalize", finalize)

    graph.add_edge(START, "validate_ticker")
    graph.add_edge("validate_ticker", "collect_data")
    graph.add_edge("collect_data", "investigate_chatter")
    graph.add_edge("investigate_chatter", "analyze_industry")
    graph.add_edge("analyze_industry", "build_context")
    graph.add_edge("build_context", "draft_memo")
    graph.add_edge("draft_memo", "finalize")
    graph.add_edge("finalize", END)

    return graph.compile()


def run_agent(ticker: str) -> AgentState:
    return build_graph().invoke({"ticker": ticker, "errors": []})
