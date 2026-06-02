# 03 · Conflict log (sample)

> A filled-in example of `templates/conflict-log.md`. Sanitized; numbers are
> illustrative placeholders.

---

## Conflict C-02 — Venue B VIP0 maker direction

- Topic: Is Venue B's VIP0 maker fee a charge or a rebate?
- Status: open
- Raised by: Agent B
- Date: 2026-05-30

### Agent A Claim

[AGENT-A][D] Venue B VIP0 maker is **+1.5 bps**, treated as a cost in the table.

### Agent B Audit

[AGENT-B audit] This reverses the sign. VIP0 maker is a **rebate of −1.5 bps** —
the trader receives it. Carrying it as a cost flips every downstream comparison
that uses Venue B as a baseline.

### Required Evidence

- Official docs: https://docs.example-venue-b.xyz/fees
- API: fee-schedule endpoint response (maker field sign)
- Source code: n/a
- Other first-hand source: in-app fee screen screenshot

### Notes

Highest-impact error in the table — it doesn't just change one cell, it changes
the direction of the comparison. Do not ship the table until resolved.

---

## Conflict C-01 — Venue A row copied from a peer

- Topic: Are Venue A's maker/taker rates real or borrowed?
- Status: open
- Raised by: Agent B
- Date: 2026-05-30

### Agent A Claim

[AGENT-A][C] Reused a peer venue's published numbers as a stand-in for Venue A.

### Agent B Audit

[AGENT-B audit] Venue A's own docs list a rate ~2× the borrowed figure.
Wrong base assumption.

### Required Evidence

- Official docs: https://docs.example-venue-a.xyz/fees
- API: —
- Source code: —
- Other first-hand source: —

### Notes

Resolve by replacing the borrowed row with the venue's own published rate.
