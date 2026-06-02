# Horizontal Comparison Case Study

A sanitized case study of a dual-agent research run. Venue names and the specific
vertical are redacted on purpose — the point here is the *method*, not the targets.

## Setup

- **Scope**: a horizontal comparison of ~12 competing venues in one fast-moving category
- **Topic**: pricing / fee schedules and incentive-program eligibility
- **Agents**: two independent agents running **different model families**.
  Different models is deliberate: it keeps the reviewer from sharing the
  drafter's blind spots.
- **Duration**: approximately 6 hours
- **Output**: main report + a graded source list with 80+ URLs (A/B/C/D tiers),
  plus a machine-readable fact sheet
- **Result**: the auditing agent caught 4 critical pricing errors before shipping

## The 4 errors caught

Drafter wrote it; auditor flagged it; the official docs settled it. None of these
are dramatic — they're exactly the kind of plausible-looking error that ships when
nobody reviews.

| Field | Drafter wrote | Resolved (first-hand docs) | Failure mode |
|---|---|---|---|
| Venue A maker/taker tier | inherited a peer venue's numbers | actual was 2× higher | wrong base assumption |
| Venue B VIP0 maker | +1.5 bps fee | **−1.5 bps rebate** (you *receive* it) | sign / direction flipped |
| Venue C premium tier | "not public" | docs already listed the numbers | gave up too early |
| Venue D base fee | one flat number | depended on collateral type (one path ~8× cheaper) | wrong row in fee table |

Lesson from the run: **every number must cite an official docs URL.** A web-search
agent synthesizing "what the fee probably is" is how all four of these slipped in.

## What made it work

- Each fact carried a confidence tier (`[A]`/`[B]`/`[C]`/`[D]`) and a fetch date.
- Conflicts were marked `[CONFLICT -> resolved via <source>]`, never silently overwritten.
- The auditor was not allowed to rewrite the drafter's blocks — only to flag and cite.
- The whole process lived in Git, so every correction is a diff with an author.

## The point

> The goal wasn't a perfect first draft. It was making four wrong numbers
> *impossible to ship quietly*.

## Walk the trail (sanitized samples)

Read these in order to see errors caught from draft to shipped, end to end:

1. [`01-agent-a-draft-excerpt.md`](./01-agent-a-draft-excerpt.md) — Agent A drafts the table, seeds the errors, flags its own uncertainty
2. [`02-agent-b-audit-excerpt.md`](./02-agent-b-audit-excerpt.md) — Agent B audits, catches 4 issues, each with a verification path
3. [`03-conflict-log.md`](./03-conflict-log.md) — the two table-level disagreements, written up not overwritten
4. [`04-resolution-log.md`](./04-resolution-log.md) — each conflict closed against a first-hand source
5. [`05-final-excerpt.md`](./05-final-excerpt.md) — the shipped table, every cell cited, plus the git trail

> All venue names are redacted (Venue A–D) and all numbers are illustrative
> placeholders. The sequence is real; the values are not.

## Still to come

- [ ] full (longer) draft and audit passes, not just excerpts
- [ ] a real `git log --follow` walkthrough on the table
