from __future__ import annotations

import argparse
import json
from typing import Any

from pydantic import BaseModel

from app.runtime.config import langsmith_status, load_dotenv_if_present


def _jsonable(value: Any) -> Any:
    if isinstance(value, BaseModel):
        return value.model_dump(mode="json")
    if isinstance(value, list):
        return [_jsonable(item) for item in value]
    if isinstance(value, dict):
        return {key: _jsonable(item) for key, item in value.items()}
    return value


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the equity research workflow automation agent.")
    parser.add_argument("--ticker", required=True)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--show-config", action="store_true")
    args = parser.parse_args()

    load_dotenv_if_present()
    if args.show_config:
        print(langsmith_status())

    from app.runtime.graph import run_agent

    state = run_agent(args.ticker)
    if args.json:
        print(json.dumps(_jsonable(state), indent=2))
    else:
        print(state.get("memo", ""))

    return 0 if not state.get("errors") else 1


if __name__ == "__main__":
    raise SystemExit(main())
