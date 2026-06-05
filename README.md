# Equity Research Workflow Automation Agent

An AI business automation MVP that turns a manual equity research workflow into a traceable LangGraph agent.

The project takes a US stock ticker as input, gathers company and market context, asks Gemini 3 Flash to draft a non-personalized equity research memo, and uses LangSmith for tracing, debugging, and later evaluations.

## Current Direction

This is not a trading bot, portfolio advisor, or backtesting system. The goal is to demonstrate practical AI workflow automation:

- model a business process as a LangGraph workflow
- connect typed data tools
- generate a useful research memo with an LLM
- inspect traces in LangSmith
- iterate prompts and workflow based on observed failures

## MVP Workflow

```text
ticker
-> collect_ticker_data
-> build_prompt_context
-> draft_memo_with_gemini
-> return memo
-> trace run in LangSmith
```

## Stack

- Workflow: LangGraph
- LLM: Gemini 3 Flash
- Tracing and evals: LangSmith
- Data tools: yfinance, SEC EDGAR, and MVP sample fallbacks
- Schemas: Pydantic

## Setup

Install dependencies:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Configure environment variables:

```powershell
copy .env.example .env
```

Required for live LLM runs:

```text
GEMINI_API_KEY=
GEMINI_MODEL=gemini-3-flash-preview
```

Optional LangSmith tracing:

```text
LANGSMITH_TRACING=true
LANGSMITH_API_KEY=
LANGSMITH_PROJECT=equity-research-workflow-agent
```

Check runtime tracing config:

```powershell
.\.venv\Scripts\python.exe -m app.runtime.agent --ticker NVDA --show-config
```

## Existing Tools

The typed data tools are already implemented:

```powershell
.\.venv\Scripts\python.exe -m app.runtime.tools.collect NVDA
```

Individual tools:

```powershell
.\.venv\Scripts\python.exe -m app.runtime.tools.company_profile NVDA
.\.venv\Scripts\python.exe -m app.runtime.tools.market_data NVDA
.\.venv\Scripts\python.exe -m app.runtime.tools.market_data NVDA --financials
.\.venv\Scripts\python.exe -m app.runtime.tools.sec_filings NVDA
.\.venv\Scripts\python.exe -m app.runtime.tools.news_search NVDA
```

If live providers fail, tools return deterministic sample data and mark source quality as `sample`.

## MVP Build Steps

1. Keep typed tools.
2. Add a minimal LangGraph workflow.
3. Add a Gemini memo node.
4. Enable LangSmith tracing.
5. Create a small LangSmith eval dataset.
6. Improve prompts and workflow from trace/eval findings.

## Run The MVP Agent

```powershell
.\.venv\Scripts\python.exe -m app.runtime.agent --ticker NVDA
```

Without `GEMINI_API_KEY`, the workflow returns a fallback memo so the graph can still be tested. With `GEMINI_API_KEY`, the memo node calls Gemini 3 Flash.
