from __future__ import annotations

import json
import urllib.request
from typing import Any

from app.runtime.schemas import DataQuality, SourceRecord


SEC_USER_AGENT = "EquityResearchAgentHarness/0.1 contact@example.com"


def sample_source(name: str, notes: str) -> SourceRecord:
    return SourceRecord(name=name, quality=DataQuality.SAMPLE, notes=notes)


def live_source(name: str, url: str, notes: str | None = None) -> SourceRecord:
    return SourceRecord(name=name, url=url, quality=DataQuality.LIVE, notes=notes)


def unavailable_source(name: str, notes: str) -> SourceRecord:
    return SourceRecord(name=name, quality=DataQuality.UNAVAILABLE, notes=notes)


def fetch_json(url: str, headers: dict[str, str] | None = None, timeout: int = 20) -> dict[str, Any]:
    request_headers = {"User-Agent": SEC_USER_AGENT, "Accept": "application/json"}
    if headers:
        request_headers.update(headers)
    request = urllib.request.Request(url, headers=request_headers)
    with urllib.request.urlopen(request, timeout=timeout) as response:
        payload = response.read().decode("utf-8")
    return json.loads(payload)

