# Research Brief  ← EDIT THIS FIRST

> This is the only file you must fill in before starting. Change the four
> variables, define the questions, then send one kickoff message to each agent.

## 0. Metadata
- Start date: `<YYYY-MM-DD>`
- Topic: `<one line>`
- Constraints: `<e.g. v1 within 24h, main report <= 12KB>`
- Money action? **No** (this is research, not a trade/transfer/deposit)

## 1. Goal — answer 1–3 explicit questions
- Q1: ...
- Q2: ...
- Q3: ...

## 2. Scope
- Must cover: `[A, B, C, ...]`
- Optional: `[...]`
- Out of scope: `[...]`  ← prevents scope creep

## 3. Division of labor
- **AGENT-A** drafts: `<sections>` → writes in `02-agent-a-draft.md`
- **AGENT-B** drafts/audits: `<sections>` → writes in `03-agent-b-audit.md`
- Audit window: within `<N>`h of the other finishing.

## 4. Acceptance checklist (operator runs before shipping)
- [ ] Every paragraph tagged `[AGENT-A]` / `[AGENT-B]` / `[BOTH]`
- [ ] Every critical fact has a source + confidence tier
- [ ] Zero unresolved `[CONFLICT]` and no `[UNCONFIRMED]` left in the report
- [ ] `reports/final-report.md` contains only `[BOTH]` / `[RESOLUTION]` content

---

## Kickoff messages (send one to each agent, swap the role)

To **Agent A**:
```
Start the task. Brief: research/00-brief.md
Your role: AGENT-A. Follow AGENTS.md. Ping me when done.
```

To **Agent B**:
```
Start the task. Brief: research/00-brief.md
Your role: AGENT-B. Follow AGENTS.md. Ping me when done.
```

> Don't relay one agent's progress to the other in chat — they sync only through
> `git pull`. Relaying breaks independence, which is the whole point.
