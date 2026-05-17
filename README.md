# Equity Research Agent Harness

An agent reliability harness for equity research agents.

The project takes a US stock ticker as input and produces an auditable equity research memo. The goal is not to prove investment alpha or provide personalized financial advice. The goal is to make an LLM-powered research workflow observable, replayable, evaluable, and improvable.

## MVP Goal

Build a LangGraph-based equity research workflow and a harness that can show:

- what the agent did,
- where it failed,
- whether the final memo is evidence-grounded,
- whether the run stayed within cost and compliance limits,
- and whether an optimized version improves strict success rate over a baseline.

## Current Scope

Input:

- US stock ticker, for example `NVDA`, `AAPL`, `MSFT`.

Output:

- Structured equity research memo
- Evidence table
- Non-personalized research view
- Confidence and limitations
- Local episode trace

Out of scope:

- Personalized investment advice
- Trading execution
- Portfolio allocation
- Backtesting
- Short-term price prediction

## Planned Stack

- Runtime: LangGraph
- Observability: local episode store first, LangSmith later
- Data: yfinance, SEC EDGAR, and a news/search provider or stub
- Schemas: Pydantic
- Evaluation: local regression runner with outcome, grounding, compliance, and cost evaluators

## Documentation

- [Project Plan](PROJECT_PLAN.md)
- [MVP Scope](docs/mvp_scope.md)
- [Success Definition](docs/success_definition.md)

