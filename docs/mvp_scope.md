# MVP Scope

## Problem

LLM-based financial research agents can produce plausible but unreliable outputs. Common failures include fabricated facts, stale metrics, weak evidence, unsupported recommendations, excessive token use, and policy violations.

This project focuses on the harness needed to observe and improve those failures.

## MVP User Flow

```text
User enters ticker
  -> agent gathers structured market, company, filing, and news context
  -> agent creates an evidence-grounded research memo
  -> harness stores the episode
  -> evaluators grade the memo and run trajectory
  -> report compares baseline and optimized versions
```

## In Scope

- Single-ticker US equity research
- Structured memo generation
- Evidence table generation
- Local trace and episode storage
- Functional and strict success evaluation
- Failure taxonomy
- Baseline vs optimized comparison
- Basic cost policy
- Basic compliance policy

## Out of Scope

- Personalized financial advice
- Buy/sell instructions for a specific user's situation
- Portfolio sizing
- Trading execution
- Backtesting
- Price-target automation
- Short-term price prediction
- Real-time production deployment
- Congress project integration

## Memo Sections

The MVP memo should include:

- Company snapshot
- Recent market snapshot
- Fundamental metrics
- Recent financial trend
- Recent news or catalysts
- Bull thesis
- Bear thesis
- Key risks
- Research view: Bullish, Neutral, or Bearish
- Evidence table
- Confidence and limitations

## Acceptance Criteria

M0 is complete when:

- The repository has a clear README.
- The project plan is saved.
- The MVP scope is documented.
- The success definition is documented.
- The project is clearly positioned as an agent reliability harness, not a trading or recommendation system.

