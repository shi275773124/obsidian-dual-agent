# 04 · Resolution log (sample)

> A filled-in example of `templates/resolution-log.md`. Sanitized; numbers are
> illustrative placeholders.

---

## Resolution R-02 — Venue B VIP0 maker direction

- Conflict: C-02
- Status: resolved
- Decided by: Human Operator (confirmed against first-hand source)
- Date: 2026-05-30

### Evidence

- Source: https://docs.example-venue-b.xyz/fees
- Quote / data: "VIP0 — maker −1.5 bps (rebate), taker 4.5 bps"
- Retrieved at: 2026-05-30, also cross-checked against the in-app fee screen

### Decision

[RESOLUTION] Agent B is correct. Venue B VIP0 maker is a **rebate of −1.5 bps**,
not a +1.5 bps charge. The comparison table and any baseline math using Venue B
are updated to reflect the rebate sign.

### Final Text

[BOTH] Venue B VIP0: maker −1.5 bps (rebate), taker 4.5 bps. Verified against
official docs + in-app fee screen on 2026-05-30.

### Follow-up

Re-check on the next quarterly review — fee schedules change when new tiers or
token programs launch.

---

## Resolution R-01 — Venue A row

- Conflict: C-01
- Status: resolved
- Decided by: Agent A (corrected own block after B's source check)
- Date: 2026-05-30

### Evidence

- Source: https://docs.example-venue-a.xyz/fees
- Quote / data: Venue A's own published maker/taker rate (~2× the borrowed figure)
- Retrieved at: 2026-05-30

### Decision

[RESOLUTION] Replace the borrowed peer-venue numbers with Venue A's own
published rate. The "copied from a peer" assumption was wrong.

### Final Text

[BOTH] Venue A maker/taker updated to the venue's own published rate (per its
fee docs, 2026-05-30).

### Follow-up

None.
