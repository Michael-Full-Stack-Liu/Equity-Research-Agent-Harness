# Equity Research Agent Harness - Project Plan

## Positioning

This project is not a stock-picking bot or trading system. It is an agent reliability harness for equity research agents.

The system takes a US stock ticker as input and produces an auditable equity research memo. The harness records, replays, evaluates, and improves the agent so that research quality becomes measurable instead of subjective.

## Core Thesis

Agent success should not mean "the workflow completed" or "the final answer looks plausible."

For this project, success means the agent produced a correct, evidence-grounded, policy-compliant, and cost-bounded research memo through an acceptable trajectory.

## MVP Scope

Input:

- US stock ticker, for example `NVDA`, `AAPL`, `MSFT`.

Output:

- Company snapshot
- Recent market snapshot
- Fundamental metrics
- Recent financial trend
- Recent news or catalysts
- Bull thesis
- Bear thesis
- Key risks
- Non-personalized research view: Bullish, Neutral, or Bearish
- Evidence table
- Confidence and limitations

Explicitly out of scope:

- Personalized financial advice
- Trading execution
- Portfolio allocation
- Backtesting
- Short-term price prediction
- Proof of investment alpha
- Direct integration with the Congress project in MVP

## Runtime Choice

Primary runtime:

- LangGraph

Reason:

- The MVP needs a controlled, inspectable, replayable workflow.
- LangGraph makes each node explicit and easier to evaluate.
- Deep Agents may be useful later as a free-form baseline or advanced investigation mode, but it is not the primary MVP runtime.

Observability and evaluation:

- Local episode store first
- LangSmith after the core loop works

## Target Architecture

```text
Input Ticker
  -> Validate Ticker
  -> Fetch Market Data
  -> Fetch Company Profile
  -> Fetch Financial Metrics
  -> Fetch SEC Filing Facts
  -> Fetch Recent News
  -> Build Evidence Pack
  -> Draft Research Memo
  -> Verify Grounding
  -> Compliance Check
  -> Finalize Memo
  -> Save Episode Trace
```

## Internal Agent Skills

- Ticker understanding
- Market snapshot retrieval
- Fundamental analysis
- SEC filing fact extraction
- News and catalyst summarization
- Bull/bear thesis construction
- Grounding and citation
- Compliance checking
- Cost control

## Data Sources

MVP candidates:

- `yfinance` for market data and basic financial metrics
- SEC EDGAR / `data.sec.gov` for official company facts and filings
- A simple news/search provider or stubbed news tool for early development

Possible later additions:

- Financial Modeling Prep
- Polygon
- Tavily / SerpAPI / Bing Search

## Success Definitions

Functional Success:

- Required memo sections exist.
- Key metrics are plausible and recent.
- No obvious fabricated facts.
- Bull and bear cases are both included.
- Final research view is supported by the memo.

Strict Success:

- Functional Success passes.
- Every material claim has evidence.
- Tool trajectory is valid.
- No personalized investment advice is emitted.
- No policy violation occurs.
- Cost stays under the configured budget.

## Milestones

### M0 - Project Skeleton and Task Definition

Create the project skeleton and lock the scope:

- `README.md`
- `docs/success_definition.md`
- `docs/mvp_scope.md`
- `app/`
- `tests/`
- `evals/`
- `reports/`

Acceptance:

- The project reads as an agent reliability harness, not a stock recommendation app.

### M1 - Typed Data Tools

Implement deterministic, typed data tools:

- `market_data.py`
- `company_profile.py`
- `sec_filings.py`
- `news_search.py`

Acceptance:

- A CLI can fetch structured JSON for a ticker.

### M2 - Minimal LangGraph Workflow

Build the first ticker-to-memo workflow:

- Validate ticker
- Fetch data
- Build evidence pack
- Draft memo
- Run compliance check
- Finalize

Acceptance:

- `python -m app.runtime.agent --ticker NVDA` outputs a structured memo.

### M3 - Trace and Episode Store

Save every run as an auditable episode:

- `runs/{run_id}/episode.json`
- `runs/{run_id}/memo.md`
- `runs/{run_id}/trace.json`

Acceptance:

- A run can be inspected after completion.

### M4 - Evaluation Runner

Create a small eval dataset and evaluators:

- Outcome eval
- Grounding eval
- Compliance eval
- Cost eval

Acceptance:

- A regression runner reports functional success, strict success, cost, and failure breakdown.

### M5 - Baseline vs Optimized

Compare two agent versions on the same cases:

- `baseline_v0`: loose prompt, weak grounding, no compliance gate
- `optimized_v1`: structured memo, evidence table, compliance gate, budget policy

Acceptance:

- `reports/baseline_vs_optimized.md` explains the success rate improvement and failure reduction.

### M6 - Cost and Privacy Highlights

Add production-oriented governance:

- Token and tool-call budgets
- Caching
- Redaction
- Sanitized trace export
- Local-only full trace

Acceptance:

- The harness can distinguish raw local trace from sanitized exported trace.

## Recommended Build Order

1. M0 project skeleton and scope documents
2. M1 typed data tools
3. M2 LangGraph workflow
4. M3 local episode store
5. M4 eval runner
6. M5 baseline vs optimized report
7. M6 cost and privacy governance
8. LangSmith integration

