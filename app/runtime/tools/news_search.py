from __future__ import annotations

import argparse
from datetime import datetime, timezone

from app.runtime.schemas import NewsItem, NewsSearchResult
from app.runtime.tools.common import sample_source
from app.runtime.tools.sample_data import SAMPLE_COMPANIES


def search_company_news(ticker: str, limit: int = 5) -> NewsSearchResult:
    normalized = ticker.upper().strip()
    company_name = SAMPLE_COMPANIES.get(normalized, {}).get("company_name", normalized)
    source = sample_source(
        "sample_news_search",
        "News search is stubbed in M1. Replace with Tavily, SerpAPI, Bing, or another provider later.",
    )
    items = [
        NewsItem(
            title=f"{company_name} recent catalyst placeholder",
            publisher="MVP sample news",
            published_at=datetime.now(timezone.utc),
            summary="Stub item used to exercise the memo and evaluation pipeline before a live news provider is configured.",
        )
    ][:limit]
    return NewsSearchResult(ticker=normalized, source=source, query=f"{company_name} recent news", items=items)


def main() -> None:
    parser = argparse.ArgumentParser(description="Fetch typed company news.")
    parser.add_argument("ticker")
    parser.add_argument("--limit", type=int, default=5)
    args = parser.parse_args()
    print(search_company_news(args.ticker, limit=args.limit).model_dump_json(indent=2))


if __name__ == "__main__":
    main()

