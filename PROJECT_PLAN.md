# Project Plan

## Positioning

This project is an AI business automation MVP for equity research workflows.

It automates a narrow analyst workflow:

```text
input ticker
-> gather company, market, filing, and news context
-> draft a non-personalized research memo
-> inspect traces and failures in LangSmith
-> iterate prompt/workflow
```

The point is not to prove stock-picking alpha. The point is to show that a real business process can be modeled, automated, traced, evaluated, and improved.

## Scope

In scope:

- US ticker input
- company profile, market, financial, SEC, and news context
- Gemini 3 Flash memo generation
- LangGraph orchestration
- LangSmith tracing
- later LangSmith dataset/evals

Out of scope:

- personalized financial advice
- trading execution
- portfolio allocation
- backtesting
- custom observability platform
- custom evaluator framework before the MVP proves it needs one

## Design Principles

- Start with the smallest useful workflow.
- Use LangSmith before building custom observability.
- Prefer simple typed tools over complex internal abstractions.
- Add guardrails only after observing real failures.
- Keep the first demo runnable with sample fallback data.

## MVP Architecture

```text
app/runtime/tools/
  collect_ticker_data(ticker)

LangGraph workflow:
  validate_ticker
  -> collect_data
  -> build_prompt_context
  -> draft_memo
  -> finalize

LangSmith:
  traces every workflow run
  stores examples and eval experiments later
```

## Milestones

### M0 - Project Reset

Clean up overdesigned custom harness layers and keep only the typed tools plus lean project docs.

Acceptance:

- README and project plan describe LangGraph + Gemini + LangSmith MVP.
- Tool tests still pass.

### M1 - Typed Tools

Status: implemented.

Tools:

- company profile
- market data
- financial metrics
- SEC filing facts
- news search stub
- combined collector

Acceptance:

- `python -m app.runtime.tools.collect NVDA` returns structured JSON.

### M2 - Minimal LangGraph Workflow

Build the first workflow around existing tools.

Nodes:

- validate ticker
- collect data
- build prompt context
- draft memo
- finalize

Acceptance:

- `python -m app.runtime.agent --ticker NVDA` returns a memo.
- The workflow can run with sample fallback data.

### M3 - Gemini 3 Flash Memo Node

Use Gemini 3 Flash for memo generation.

Acceptance:

- Gemini key in environment enables live memo generation.
- Missing key produces a clear error or deterministic fallback.

### M4 - LangSmith Tracing

Enable LangSmith tracing for local runs.

Acceptance:

- each workflow run appears in the configured LangSmith project when tracing env vars are set.

### M5 - LangSmith Evaluation Dataset

Create a small eval set of ticker tasks and expected memo requirements.

Acceptance:

- run baseline workflow against the dataset in LangSmith.
- record failure examples and improvement ideas.

### M6 - Iterate From Observed Failures

Improve prompts, tool context, or graph shape based on LangSmith traces/evals.

Acceptance:

- produce a short report showing baseline vs improved behavior.

