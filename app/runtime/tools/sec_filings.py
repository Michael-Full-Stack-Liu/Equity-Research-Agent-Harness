from __future__ import annotations

import argparse
from typing import Any

from app.runtime.schemas import FilingFact, FilingFacts
from app.runtime.tools.common import fetch_json, live_source, sample_source, unavailable_source
from app.runtime.tools.sample_data import SAMPLE_COMPANIES, SAMPLE_FINANCIALS


SEC_COMPANY_TICKERS_URL = "https://www.sec.gov/files/company_tickers.json"
SEC_COMPANY_FACTS_URL = "https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json"

CONCEPTS = {
    "RevenueFromContractWithCustomerExcludingAssessedTax": "revenue",
    "Revenues": "revenue",
    "GrossProfit": "gross_profit",
    "OperatingIncomeLoss": "operating_income",
    "NetIncomeLoss": "net_income",
    "EarningsPerShareDiluted": "diluted_eps",
    "NetCashProvidedByUsedInOperatingActivities": "operating_cash_flow",
    "CashAndCashEquivalentsAtCarryingValue": "cash_and_equivalents",
    "LongTermDebtAndFinanceLeaseObligationsCurrentAndNoncurrent": "total_debt",
}


def _format_cik(cik: str) -> str:
    digits = "".join(character for character in cik if character.isdigit())
    return digits.zfill(10)


def _sample_cik(ticker: str) -> str | None:
    sample = SAMPLE_COMPANIES.get(ticker.upper().strip(), {})
    cik = sample.get("cik")
    return _format_cik(cik) if cik else None


def lookup_cik(ticker: str) -> str | None:
    normalized = ticker.upper().strip()
    sample = _sample_cik(normalized)
    if sample:
        return sample

    try:
        payload = fetch_json(SEC_COMPANY_TICKERS_URL)
    except Exception:
        return None

    for item in payload.values():
        if item.get("ticker", "").upper() == normalized:
            return _format_cik(str(item["cik_str"]))
    return None


def _latest_fact(concept: str, values: dict[str, Any]) -> FilingFact | None:
    units = values.get("units", {})
    for unit, facts in units.items():
        annual = [fact for fact in facts if fact.get("form") in {"10-K", "10-Q"} and "val" in fact]
        if not annual:
            continue
        latest = sorted(annual, key=lambda fact: fact.get("filed", ""))[-1]
        return FilingFact(
            concept=concept,
            value=latest.get("val"),
            unit=unit,
            fiscal_year=latest.get("fy"),
            fiscal_period=latest.get("fp"),
            form=latest.get("form"),
            filed=latest.get("filed"),
            accession_number=latest.get("accn"),
        )
    return None


def get_filing_facts(ticker: str) -> FilingFacts:
    normalized = ticker.upper().strip()
    cik = lookup_cik(normalized)
    if not cik:
        return FilingFacts(
            ticker=normalized,
            cik=None,
            source=unavailable_source("sec_companyfacts", "Could not resolve CIK for ticker."),
            facts=[],
        )

    url = SEC_COMPANY_FACTS_URL.format(cik=cik)
    try:
        payload = fetch_json(url)
    except Exception as exc:
        sample_financials = SAMPLE_FINANCIALS.get(normalized, {})
        facts = [
            FilingFact(concept=key, value=value, unit="USD", fiscal_period=sample_financials.get("fiscal_period"))
            for key, value in sample_financials.items()
            if key != "fiscal_period"
        ]
        return FilingFacts(
            ticker=normalized,
            cik=cik,
            source=sample_source("sample_sec_filing_facts", f"SEC fetch failed: {exc}. Returning sample filing facts."),
            facts=facts,
        )

    us_gaap = payload.get("facts", {}).get("us-gaap", {})
    facts: list[FilingFact] = []
    for sec_concept, canonical_name in CONCEPTS.items():
        if sec_concept not in us_gaap:
            continue
        fact = _latest_fact(canonical_name, us_gaap[sec_concept])
        if fact:
            facts.append(fact)

    return FilingFacts(ticker=normalized, cik=cik, source=live_source("sec_companyfacts", url), facts=facts)


def main() -> None:
    parser = argparse.ArgumentParser(description="Fetch typed SEC company facts.")
    parser.add_argument("ticker")
    args = parser.parse_args()
    print(get_filing_facts(args.ticker).model_dump_json(indent=2))


if __name__ == "__main__":
    main()

