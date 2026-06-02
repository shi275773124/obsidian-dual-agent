# When right facts produce a wrong conclusion

> Sanitized from a real run. The domain and specifics are redacted; numbers are
> illustrative. The lesson is the point.

This is the case that motivated **Gate G4 (ruler / object match)** in
[`templates/precondition-checklist.md`](../templates/precondition-checklist.md).
v1's three rules only check whether *facts* are right. They do not catch a claim
where the facts are right but the **tool was wrong for the data**.

## What happened

A research run asked: *does signal Z have predictive value?*

The agent applied a standard goodness-of-fit test — a panel R² regression — across
the dataset. Result:

```
R² < 0.005 everywhere
```

The agent's verdict: **"Signal Z has no edge. Archive it."**

Every number was correct. The R² really was that low. An auditor checking *facts*
(v1's job) would have confirmed each figure and waved it through.

## Why the conclusion was still wrong

Panel R² assumes a **dense, continuous cross-section**: lots of observations,
roughly stationary, value spread across the whole sample. Signal Z was the
opposite — **sparse and event-driven**: most of the time it says nothing, and its
value lives in a handful of rare, large events.

On that kind of data, a near-zero R² is **expected and meaningless**. It measures
how well a dense-data tool fits sparse data — not whether the signal works. The
agent used the wrong ruler and read the ruler's failure as the object's failure.

The correct verdict was not "Signal Z has no edge." It was **"R² panel regression
is the wrong test for a sparse event signal — measure it with an event study
instead."** Different test, different (and real) answer.

## The fix: a fourth gate

v1 conflict resolution can't catch this, because there's no factual conflict —
both agents would agree the R² is 0.004. The error is upstream of the facts, in
the **choice of tool**. So the adversarial-review variant adds a precondition gate:

> **G4 — Ruler / object match:** before shipping any "X is / isn't true" verdict,
> check that the method's assumptions match the data's structure. A bad score from
> the wrong tool is not evidence about the object.

## Takeaways

- "The numbers are right" is not the same as "the conclusion is right."
- The most dangerous errors aren't wrong facts — they're right facts measured with
  the wrong instrument, then stated with confidence.
- Make the *tool choice* reviewable, not just the *numbers*. That's what the
  [G1–G4 checklist](../templates/precondition-checklist.md) is for, and why the
  [verdict ladder](../docs/05-adversarial-review.md) keeps re-judging until the
  reasoning — not just the data — holds up.
