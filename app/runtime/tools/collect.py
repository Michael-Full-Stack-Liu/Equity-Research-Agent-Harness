from __future__ import annotations

import argparse

from app.runtime.schemas import TickerDataBundle
from app.runtime.tools.company_profile import get_company_profile
from app.runtime.tools.market_data import get_financial_metrics, get_market_snapshot
from app.runtime.tools.news_search import search_company_news
from app.runtime.tools.sec_filings import get_filing_facts


def collect_ticker_data(ticker: str) -> TickerDataBundle:
    normalized = ticker.upper().strip()
    return TickerDataBundle(
        ticker=normalized,
        company_profile=get_company_profile(normalized),
        market_snapshot=get_market_snapshot(normalized),
        financial_metrics=get_financial_metrics(normalized),
        filing_facts=get_filing_facts(normalized),
        news=search_company_news(normalized),
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Collect all M1 typed data for a ticker.")
    parser.add_argument("ticker")
    args = parser.parse_args()
    print(collect_ticker_data(args.ticker).to_json())


if __name__ == "__main__":
    main()

