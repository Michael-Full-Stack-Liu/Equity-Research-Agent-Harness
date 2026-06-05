from __future__ import annotations

import os

from app.runtime.config import load_dotenv_if_present


DEFAULT_GEMINI_MODEL = "gemini-3-flash-preview"


def generate_with_gemini(prompt: str, *, use_google_search: bool = False) -> str | None:
    load_dotenv_if_present()
    if os.getenv("DISABLE_LIVE_LLM", "").strip().lower() in {"1", "true", "yes"}:
        return None
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return None

    from google import genai
    from google.genai import types

    client = genai.Client(api_key=api_key)
    config = None
    if use_google_search:
        config = types.GenerateContentConfig(
            tools=[types.Tool(google_search=types.GoogleSearch())],
        )
    response = client.models.generate_content(
        model=os.getenv("GEMINI_MODEL", DEFAULT_GEMINI_MODEL),
        contents=prompt,
        config=config,
    )
    return response.text or ""


def draft_memo_with_gemini(prompt: str) -> str:
    response = generate_with_gemini(prompt)
    if response is None:
        return _fallback_memo(prompt)
    return response


def _fallback_memo(prompt: str) -> str:
    return f"""# Equity Research Memo

Gemini is not configured, so this fallback memo confirms the workflow is wired.

## Company Snapshot

The workflow collected company context for the requested ticker.

## Market and Financial Snapshot

The workflow collected market, financial, and SEC context. Market chatter is investigated in a separate workflow node. Some data may be sample fallback data.

## Bull Case

- The company has structured profile and financial context available.

## Bear Case

- Data quality may be incomplete until live providers are configured.

## Key Risks and Data Limitations

- This is not personalized financial advice.
- This fallback output is for workflow validation only.

## Non-Personalized Research View

Research view: Neutral.

Prompt preview:

```text
{prompt[:1200]}
```
"""
