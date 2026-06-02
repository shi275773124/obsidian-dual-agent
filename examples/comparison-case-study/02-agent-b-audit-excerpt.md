# 02 · Agent B audit (excerpt)

> Sanitized excerpt from Agent B's audit pass over `01-agent-a-draft-excerpt.md`.
> Agent B does **not** edit Agent A's blocks — it appends audit notes and opens
> conflicts. Numbers are illustrative placeholders.

---

[AGENT-B audit] Venue A row — **rejected as unverified.** Agent A copied a peer
venue's numbers. I fetched Venue A's own fee docs (first-hand) and the real rate
is ~2× the copied figure. This is a wrong-base-assumption error. Opening a conflict.
Source: https://docs.example-venue-a.xyz/fees (fetched 2026-05-30) `[A]`

[AGENT-B audit] Venue B VIP0 maker — **direction is flipped.** Agent A read
"+1.5 bps" as a charge. Per the venue's own fee schedule, VIP0 maker is a
**rebate of −1.5 bps** (you *receive* it). Writing it as a cost reverses the
sign in the whole comparison. This is the highest-impact error in the table.
Opening a conflict. Source: https://app.example-venue-b.xyz/fees (2026-05-30) `[A]`

[AGENT-B audit] Venue C premium tier — **not actually unpublished.** Agent A gave
up too early. The premium tier *is* in the docs, just on a separate page. Filling
it in with a citation rather than leaving `[NEEDS-SOURCE]`.
Source: https://docs.example-venue-c.xyz/fees#premium (2026-05-30) `[A]`

[AGENT-B audit] Venue D base fee — **wrong row.** The flat-fee claim is wrong:
the base fee depends on collateral type, and one collateral path is materially
cheaper than the row Agent A used. Needs a source-confirmed correction.
Source: https://docs.example-venue-d.xyz/fees (2026-05-30) `[A]`

---

## Audit summary

4 issues raised, all with a verification path:

| Venue | Failure mode | Status |
|---|---|---|
| Venue A | wrong base assumption (copied a peer) | → conflict |
| Venue B | sign / direction flipped | → conflict (high impact) |
| Venue C | gave up too early | corrected inline with source |
| Venue D | wrong row in fee table | → conflict |

The two table-level conflicts (A, B) are written up in `03-conflict-log.md`.
