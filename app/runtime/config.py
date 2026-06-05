from __future__ import annotations

import os
from pathlib import Path


def load_dotenv_if_present() -> None:
    env_path = Path.cwd() / ".env"
    if not env_path.exists():
        return

    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value

    if os.getenv("LANGSMITH_TRACING", "").strip().lower() == "true":
        os.environ.setdefault("LANGCHAIN_TRACING_V2", "true")
    if os.getenv("LANGSMITH_API_KEY"):
        os.environ.setdefault("LANGCHAIN_API_KEY", os.getenv("LANGSMITH_API_KEY", ""))


def langsmith_status() -> str:
    load_dotenv_if_present()
    tracing = os.getenv("LANGSMITH_TRACING", "false").strip().lower()
    langchain_tracing = os.getenv("LANGCHAIN_TRACING_V2", "false").strip().lower()
    project = os.getenv("LANGSMITH_PROJECT", "")
    has_key = bool(os.getenv("LANGSMITH_API_KEY"))
    return (
        f"LANGSMITH_TRACING={tracing}, "
        f"LANGCHAIN_TRACING_V2={langchain_tracing}, "
        f"LANGSMITH_PROJECT={project or '(unset)'}, "
        f"LANGSMITH_API_KEY={'set' if has_key else 'unset'}"
    )
