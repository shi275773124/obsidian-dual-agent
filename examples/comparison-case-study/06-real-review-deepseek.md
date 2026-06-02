# 06 · A real `falsify review` run

This is an **actual** run of `falsify review` against
[`01-agent-a-draft-excerpt.md`](./01-agent-a-draft-excerpt.md) — the seeded-error
draft — not a mock-up. The reviewer (Agent B / the Skeptic) was a DeepSeek model
through its OpenAI-compatible API. No edits to the output below.

```
$ falsify review examples/comparison-case-study/01-agent-a-draft-excerpt.md

[AGENT-B audit] Venue A row is fabricated data. The draft explicitly states "no
dedicated docs page found; copied from a peer venue." This is not a fee — it's a
guess. Shipping this as a "cross-venue table" is shipping fiction. Verification
path: ask the author for the actual Venue A fee schedule URL. If none exists, the
row must be deleted, not footnoted.

[AGENT-B audit] Venue B maker fee "+1.5 bps" is ambiguous and likely wrong. The
draft says "assumed charge" but the plus sign is non-standard — most venues list
maker rebates as negative. If +1.5 bps is actually a rebate (the venue pays you),
treating it as a cost flips the direction of the comparison. Verification path:
check Venue B's official fee page for the VIP0 tier — look for a minus sign or the
word "rebate" in the maker column.

[AGENT-B audit] Venue C row is empty with a note "premium tier 'not public'." That
is not a data point — it's a hole. Verification path: confirm with Venue C's API
or support that the premium tier truly has no published rate, then drop the row or
use retail.

[AGENT-B audit] Venue D claim "flat across collateral types" is unsupported. Many
venues vary fees by collateral asset. Verification path: check Venue D's fee
schedule for collateral-specific tiers. If none, the claim is an assumption.

[AGENT-B audit] The entire table is built on "illustrative placeholders." The
draft's own text treats them as real data points. Shipped as-is, readers will
treat placeholders as real fees.

VERDICT: HOLD
```

`review` exited with code **1** (HOLD).

The point: every seeded error in the draft was caught — the fabricated row, the
flipped-sign fee, the empty hole, the unsupported claim — plus one the author
didn't even flag (placeholders being treated as real). That's the whole pitch:
**not a perfect first draft, but errors that can't ship quietly.**
