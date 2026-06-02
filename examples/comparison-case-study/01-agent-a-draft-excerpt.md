# 01 · Agent A draft (excerpt)

> Sanitized excerpt from Agent A's first draft. Venue names are redacted to
> Venue A–D; all numbers are **illustrative placeholders**, not real fee data.
> The point is the shape of the work, not the values.

---

## Maker / taker fees — cross-venue table

[AGENT-A][C] Pulled the headline rates for each venue. Where a venue didn't have
an obvious docs page I reused a peer venue's published numbers as a starting point.

| Venue | Maker | Taker | Notes |
|---|---|---|---|
| Venue A | 1.5 bps | 4.5 bps | [NEEDS-AUDIT] no dedicated docs page found; copied from a peer venue |
| Venue B | +1.5 bps | 4.5 bps | VIP0 tier |
| Venue C | — | — | [NEEDS-SOURCE] premium tier "not public" |
| Venue D | 3.5 bps | 7.0 bps | flat across collateral types |

[AGENT-A][D] Venue B's VIP0 maker looks like a small fee (+1.5 bps). Treating it
as a cost in the comparison.

[AGENT-A] Venue C only publishes the retail tier; the premium/high-volume tier
appears to be unpublished, so I've left it blank for now.

[AGENT-A][B] Venue D charges one flat base fee regardless of which collateral
asset you post.

---

## Open items I'm not sure about

- `[NEEDS-AUDIT]` Venue A row — borrowed from a peer, not verified against its own docs
- `[NEEDS-SOURCE]` Venue C premium tier — couldn't find it
- `[NEEDS-AUDIT]` Venue B maker — is +1.5 bps a charge or a rebate? assumed charge
