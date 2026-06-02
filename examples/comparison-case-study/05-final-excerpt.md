# 05 · Final report (excerpt)

> Sanitized excerpt of the shipped table — after audit + arbitration. Every row
> is now `[BOTH]` (agreed) or `[RESOLUTION]` (arbitrated). Numbers are
> illustrative placeholders.

---

## Maker / taker fees — cross-venue table (final)

[BOTH] All four rows below were either confirmed by both agents or resolved
against first-hand sources. None ship on a single agent's word.

| Venue | Maker | Taker | Source | Tier |
|---|---|---|---|---|
| Venue A | 3.0 bps | 9.0 bps | official docs `[A]` | corrected — was a borrowed peer row (R-01) |
| Venue B | **−1.5 bps (rebate)** | 4.5 bps | official docs + app `[A]` | corrected — sign was flipped (R-02) |
| Venue C | 0.4 bps | 2.8 bps | official docs `[A]` | premium tier — was wrongly marked "not public" |
| Venue D | 0.5 bps | 4.0 bps | official docs `[A]` | cheapest collateral path — was wrong row |

[BOTH] Every cell carries a first-hand citation and a confidence tier. The four
cells that started wrong are exactly the four Agent B caught — see
`03-conflict-log.md` and `04-resolution-log.md` for the trail.

---

## What the git history shows

```
draft(agent-a):   add initial fee comparison table
audit(agent-b):   flag venue-b maker sign + venue-a borrowed row
resolve(human):   settle venue-b maker sign using official docs
verify(agent-b):  confirm venue-c premium tier + venue-d collateral row
docs(human):      finalize table after review
```

[BOTH] Each correction is a commit with an author. Anyone can `git log`/`git blame`
the table and see which number changed, who changed it, and which source closed it.
