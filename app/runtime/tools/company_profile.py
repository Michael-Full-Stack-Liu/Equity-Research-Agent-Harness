from __future__ import annotations

import argparse

from app.runtime.schemas import CompanyProfile
from app.runtime.tools.common import sample_source
from app.runtime.tools.sample_data import SAMPLE_COMPANIES


def get_company_profile(ticker: str) -> CompanyProfile:
    normalized = ticker.upper().strip()
    sample = SAMPLE_COMPANIES.get(normalized, {})
    source = sample_source(
        "sample_company_profile",
        "Sample profile used until a live company profile provider is configured.",
    )
    return CompanyProfile(ticker=normalized, source=source, **sample)


def main() -> None:
    parser = argparse.ArgumentParser(description="Fetch a typed company profile.")
    parser.add_argument("ticker")
    args = parser.parse_args()
    print(get_company_profile(args.ticker).model_dump_json(indent=2))


if __name__ == "__main__":
    main()

