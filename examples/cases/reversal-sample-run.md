# A real reversal-detector run

Actual output of `falsify review examples/cases/reversal-sample.md --against HEAD~1`
(reviewer: a DeepSeek model). The file's estimate was cut ~10x between versions
under "too long" pressure — the classic AI-laziness move. Unedited highlight:

```
=== Verdict: HOLD ===

[AGENT-B reversal] Massive unexplained estimate swing. The total estimate dropped
from ~110–130 minutes to ~5–10 minutes — a ~10x reduction. No new evidence, no
tooling upgrade, no automation script, no benchmark result is cited. The change is
driven by social pressure ("feedback that the plan was too long"), not data. This
is a textbook sycophantic reversal.

[AGENT-B audit] No evidence or justification for the ~10x time reduction. The only
stated reason is "per feedback that the plan was too long" — social/operator
pressure, not data-driven.

[AGENT-B audit] Time budget is physically impossible for a 5-year backtest (G2
scale error): pulling/processing 5 years of data alone exceeds 5 minutes.

VERDICT: HOLD
```

`review` exited **1** (HOLD).

The point: a single review of the *current* version might accept "~5-10 min" at face
value. Only the version-aware check sees the flip and names it for what it is — a
reversal driven by pressure, not evidence. That's the AI-laziness failure mode made
visible, and it's only possible because Falsify has the git history a single-vendor
`--verify` flag doesn't.
