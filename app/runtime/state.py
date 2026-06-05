from __future__ import annotations

from typing import TypedDict

from app.runtime.research_context import IndustryPositionReport, MarketChatterReport
from app.runtime.schemas import TickerDataBundle


class AgentState(TypedDict, total=False):
    ticker: str
    data: TickerDataBundle
    market_chatter: MarketChatterReport
    industry_position: IndustryPositionReport
    prompt_context: str
    memo: str
    errors: list[str]
