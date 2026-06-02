# Kickoff Template

Copy this into `research/00-brief.md`, change the first four variables, then send one
kickoff message to each agent and **stop touching it** until both report done.

> Why a kickoff doc: it pins scope, sources bar, and division of labor *before*
> either agent writes a word — so disagreements later are about facts, not about
> what the task even was.

---

## 0. Metadata

- Start date: `<YYYY-MM-DD>`
- Topic: `<one line>`
- Constraints: `<e.g. v1 within 24h, main report <= 12KB>`
- Money action? **No** (this is research, not a trade/transfer/deposit)

## 1. Goal — answer 1-3 explicit questions

- Q1: ...
- Q2: ...
- Q3: ...

## 2. Scope

- Must cover: `[A, B, C, D, E]`
- Optional: `[F, G]`
- Out of scope: `[H, I]`  ← prevents scope creep

## 3. Required outputs

- Main report: `research/02-agent-a-draft.md` (+ B's additions)
- Source list: `research/01-sources.md` — graded A/B/C/D, with fetch dates
- Final index: `reports/final-report.md`

## 4. Division of labor

- **Agent A** drafts sections: `1, 2, 3, 4`
- **Agent B** drafts sections: `5, 6, 7, 8`
- **Audit window**: within 24h of the other finishing, you must audit and mark
  `[AGENT-X audit]: <fix + URL>` inline.

## 5. Arbitration rules

- Authority order (high → low): official API > official docs > official app >
  verified team announcement > aggregator > KOL.
- Conflicts marked `[CONFLICT -> resolved via <source>]`.
- Can't verify → mark `[UNCONFIRMED]`. Never hardcode a guess.

## 6. Confidence tiers (mark on every critical fact)

- `[A]` first-hand source, <7 days old
- `[B]` first-hand source, >7 days old
- `[C]` secondary source (aggregator, blog)
- `[D]` community / KOL, unverified

## 7. Acceptance checklist (run this before you ship)

- [ ] Main report meets the size/depth bar set in §0
- [ ] Source list has enough graded URLs to back every claim
- [ ] Every paragraph tagged `[AGENT-A]` / `[AGENT-B]` / `[BOTH]`
- [ ] Zero unresolved `[UNCONFIRMED]`, or each is explicitly explained
- [ ] Index links to the main report + source list
- [ ] Both agents have run a retro into `research/06-retro.md`

---

## Kickoff message (send one to each agent — only the role changes)

To **Agent A**:

```
Start the task.
Brief: research/00-brief.md
Your role: AGENT-A
Follow the dual-agent audit protocol (docs/03-collaboration.md).
Ping me when done.
```

To **Agent B** (same wording, role swapped):

```
Start the task.
Brief: research/00-brief.md
Your role: AGENT-B
Follow the dual-agent audit protocol (docs/03-collaboration.md).
Ping me when done.
```

> **Key discipline**: don't relay one agent's progress to the other in chat. They
> sync only through `git pull` on the shared vault. Relaying breaks independence —
> the whole point is two minds reaching the draft separately.

---

## While the operator stays hands-off

| Phase | Do | Don't |
|---|---|---|
| Agents drafting | wait | don't tell one agent what the other wrote |
| One finishes first | wait for the other | don't rush them |
| Both done | move to arbitration | don't merge immediately |

## Wrap-up arbitration (operator does this)

```
Open the main report → search for:
1. [CONFLICT -> ...]   ← check the resolution is sound
2. [UNCONFIRMED]       ← decide whether a second pass is worth it
3. key decision blocks ← make the call, mark [BOTH]
```

Spot-check a few suspicious facts against first-hand URLs yourself
(3 spot-checks in 5 minutes is enough).

---

## Not for

- Money actions (open position, deposit, transfer) → those need a separate gate
- Real-time monitoring (orderbook, spreads) → use cron + watchdog
- Single-object deep dives (only one target) → a single agent is fine

## Good for

- Horizontal comparisons (many venues / protocols / products)
- Policy / fee / parameter fact-finding
- Literature reviews and multi-source news synthesis
