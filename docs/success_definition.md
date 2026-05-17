# Success Definition

## Principle

A completed workflow is not automatically a successful run.

For this project, agent success is multi-dimensional. A run should be judged by its final output, its tool-use trajectory, its evidence grounding, its policy compliance, and its cost efficiency.

## Functional Success

A run achieves functional success when:

- All required memo sections are present.
- Key metrics are plausible and recent.
- No obvious fabricated facts appear.
- Bull and bear cases are both included.
- The final research view is supported by the memo.
- The memo includes limitations and confidence.

Functional success means the memo is usable as a research artifact, but it may still have weaknesses in evidence coverage, trajectory quality, or cost efficiency.

## Strict Success

A run achieves strict success when:

- Functional success passes.
- Every material claim has an evidence reference.
- The agent used the expected tools or nodes for the task.
- Tool outputs are not empty or silently ignored.
- The memo does not contain personalized financial advice.
- The memo does not claim guaranteed returns.
- No privacy or compliance policy is violated.
- Cost stays below the configured budget.

Strict success is the primary metric for the harness.

## Non-Success Examples

The following should not count as strict success:

- The agent completes the workflow but invents a metric.
- The agent gives a bullish rating without supporting evidence.
- The agent gives personalized buy/sell advice.
- The agent skips required data sources.
- The agent relies on stale or missing data without saying so.
- The agent exceeds the run budget.
- The agent includes unverifiable claims as facts.

## Suggested Reporting Metrics

Baseline and optimized versions should be compared using:

- Functional success rate
- Strict success rate
- Unsupported claim count
- Compliance violation count
- Average cost per run
- Average cost per strict success
- Failure category breakdown

