# Retrospective Template

Run this after every task. Each agent fills in its own half. The operator reads
both halves and decides which new rule, if any, gets promoted into the shared
protocol or an agent's prompt.

> The retro is what makes the kit improve over time: every task either confirms
> the rules or surfaces a new one. Without it, the agents keep making the same
> class of mistake.

---

## Task metadata

- Topic: `<...>`
- Start / end date: `<YYYY-MM-DD>` / `<YYYY-MM-DD>`
- Main report: `reports/final-report.md`
- Total time: `<e.g. 6h across 2 days>`

---

## [AGENT-A] self-review

### 3 mistakes I made
1. ... (fact error caught by [AGENT-B] audit — include the original URL + fix)
2. ...
3. ...

### 1 thing [AGENT-B] did better than me this task
...

### 1 new rule I propose
- **Rule name**: ...
- **Trigger**: when does it apply
- **Forced action**: what it makes the agent do
- **Why** (the pain point from this task): ...

---

## [AGENT-B] self-review

### 3 mistakes I made
1. ...
2. ...
3. ...

### 1 thing [AGENT-A] did better than me this task
...

### 1 new rule I propose
- **Rule name**: ...
- **Trigger**: ...
- **Forced action**: ...
- **Why**: ...

---

## [OPERATOR] decision

### Rules adopted
- [ ] [AGENT-A]'s proposal: `<rule name>` → patch `<prompt / docs file>`
- [ ] [AGENT-B]'s proposal: `<rule name>` → patch `<prompt / docs file>`

### Rejected / parked
- ... (reason)

---

## Meta-retrospective (run once every ~5 tasks)

The risk of a dual-agent setup isn't that the agents disagree — it's that over
time they **stop** disagreeing. They learn each other's habits and start making
the same class of error in unison. When that happens, the second agent is no
longer a real reviewer.

Check:

- Across the last ~5 tasks, what error type recurs most?
- Which prompt / rule file has bloated and should be split?
- Are the two agents "collaborating too well" — converging on the same blind spots?

If independence is eroding, on the next task deliberately force divergence:
give the two agents **different models** or **different skill/tool sets** so they
reach the draft by different paths.
