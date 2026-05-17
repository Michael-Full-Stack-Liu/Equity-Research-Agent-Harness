import unittest

from app.runtime.tools.collect import collect_ticker_data
from app.runtime.tools.company_profile import get_company_profile
from app.runtime.tools.market_data import get_market_snapshot
from app.runtime.tools.news_search import search_company_news
from app.runtime.tools.sec_filings import get_filing_facts


class ToolTests(unittest.TestCase):
    def test_company_profile_normalizes_ticker(self) -> None:
        profile = get_company_profile("nvda")

        self.assertEqual(profile.ticker, "NVDA")
        self.assertEqual(profile.company_name, "NVIDIA Corporation")

    def test_market_snapshot_returns_typed_sample_when_yfinance_missing(self) -> None:
        snapshot = get_market_snapshot("MSFT")

        self.assertEqual(snapshot.ticker, "MSFT")
        self.assertIn(snapshot.source.name, {"sample_market_data", "yfinance"})

    def test_sec_filing_facts_returns_typed_result(self) -> None:
        facts = get_filing_facts("AAPL")

        self.assertEqual(facts.ticker, "AAPL")
        self.assertEqual(facts.cik, "0000320193")
        self.assertIsInstance(facts.facts, list)

    def test_news_search_stub_is_typed(self) -> None:
        news = search_company_news("AAPL")

        self.assertEqual(news.ticker, "AAPL")
        self.assertTrue(news.items)

    def test_collect_ticker_data_bundle(self) -> None:
        bundle = collect_ticker_data("NVDA")

        self.assertEqual(bundle.ticker, "NVDA")
        self.assertEqual(bundle.company_profile.company_name, "NVIDIA Corporation")
        self.assertEqual(bundle.market_snapshot.ticker, "NVDA")
        self.assertEqual(bundle.filing_facts.ticker, "NVDA")
        self.assertTrue(bundle.news.items)


if __name__ == "__main__":
    unittest.main()
