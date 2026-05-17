from __future__ import annotations

import argparse
from typing import Any

from app.runtime.schemas import FinancialMetrics, MarketSnapshot
from app.runtime.tools.common import live_source, sample_source
from app.runtime.tools.sample_data import SAMPLE_FINANCIALS, SAMPLE_MARKET


def _load_yfinance_info(ticker: str) -> dict[str, Any] | None:
    try:
        import yfinance as yf  # type: ignore[import-not-found]
    except ModuleNotFoundError:
        return None

    try:
        info = yf.Ticker(ticker).info
    except Exception:
        return None
    return info or None


def get_market_snapshot(ticker: str) -> MarketSnapshot:
    normalized = ticker.upper().strip()
    info = _load_yfinance_info(normalized)
    if info:
        source = live_source(
            "yfinance",
            f"https://finance.yahoo.com/quote/{normalized}",
            "Fetched through the optional yfinance package.",
        )
        return MarketSnapshot(
            ticker=normalized,
            source=source,
            currency=info.get("currency"),
            previous_close=info.get("previousClose"),
            regular_market_price=info.get("regularMarketPrice") or info.get("currentPrice"),
            market_cap=info.get("marketCap"),
            trailing_pe=info.get("trailingPE"),
            forward_pe=info.get("forwardPE"),
            price_to_sales=info.get("priceToSalesTrailing12Months"),
            fifty_two_week_low=info.get("fiftyTwoWeekLow"),
            fifty_two_week_high=info.get("fiftyTwoWeekHigh"),
            average_volume=info.get("averageVolume"),
        )

    source = sample_source(
        "sample_market_data",
        "Install yfinance for live market data. Returning deterministic sample data for MVP wiring.",
    )
    return MarketSnapshot(ticker=normalized, source=source, **SAMPLE_MARKET.get(normalized, {}))


def get_financial_metrics(ticker: str) -> FinancialMetrics:
    normalized = ticker.upper().strip()
    source = sample_source(
        "sample_financial_metrics",
        "Financial statement normalization will be replaced by SEC company facts in a later M1/M2 refinement.",
    )
    return FinancialMetrics(ticker=normalized, source=source, **SAMPLE_FINANCIALS.get(normalized, {}))


def main() -> None:
    parser = argparse.ArgumentParser(description="Fetch typed market data.")
    parser.add_argument("ticker")
    parser.add_argument("--financials", action="store_true", help="Return financial metrics instead of market snapshot.")
    args = parser.parse_args()
    result = get_financial_metrics(args.ticker) if args.financials else get_market_snapshot(args.ticker)
    print(result.model_dump_json(indent=2))


if __name__ == "__main__":
    main()

