# AGENTS.md — Demo Vault Rules

> Both agents read this at the start of every session. Your identity is
> **AGENT-A** or **AGENT-B** — your host config tells you which.

This vault runs one dual-agent research task at a time. Agent A drafts and
advances; Agent B audits and challenges. Neither is the final judge — first-hand
sources and the human operator are.

## Hard rules

### 1. Pull before writing
```bash
git pull --rebase
```
If pull fails, STOP and report. Don't write until the vault is in sync.

### 2. Read the brief first
Open [`research/00-brief.md`](./research/00-brief.md) before writing anything.
It defines the topic, the questions, the scope, and who drafts what.

### 3. Tag every paragraph
Every paragraph, table, code block, or list block starts with one of:
- `[AGENT-A]` — Agent A wrote this
- `[AGENT-B]` — Agent B wrote this
- `[BOTH]` — both agents synced and agree

No untagged prose, ever. Mark critical facts with a confidence tier:
- `[A]` first-hand source, <7 days old
- `[B]` first-hand source, >7 days old
- `[C]` secondary source (aggregator, blog)
- `[D]` community / KOL, unverified

### 4. Don't rewrite the other agent's blocks
Disagree with an `[AGENT-A]` block? Don't edit it. Instead:
- add `[AGENT-B audit]: <correction + source URL>` underneath, or
- add a new `[AGENT-B]` paragraph, or
- open a `[CONFLICT]` in `research/04-conflicts.md`.

### 5. Conflicts go to first-hand sources
Neither agent wins by assertion. Resolve by:
1. Identify the authoritative source — order: official API > official docs >
   official app > verified announcement > source code > aggregator > KOL.
2. Fetch the URL **now** (not from memory).
3. Paste the quote + URL + timestamp into `research/05-resolutions.md`.
4. Update the affected text and mark it `[BOTH]`.

If nothing first-hand exists, mark the fact `[UNCONFIRMED]` and move on.
Never invent a resolution.

### 6. Commit with your own identity
```bash
git config user.name  "Agent A"      # or "Agent B"
git config user.email "agent-a@yourdomain.local"
git commit -m "draft(agent-a): <short topic>"   # or audit(agent-b)/resolve(human)
git push
```
`git log` should always show which agent wrote which commit.

## Never do these
- ❌ Write without pulling first
- ❌ Edit another agent's `[AGENT-X]` block to "fix" it
- ❌ Strip tags from existing paragraphs
- ❌ Cite training data as authority ("I recall that…")
- ❌ Put anything into `reports/final-report.md` that isn't `[BOTH]` or `[RESOLUTION]`
- ❌ `git push --force`; commit secrets (keys, tokens) even in private repos

## Roles at a glance
| Role | File they own | Job |
|---|---|---|
| AGENT-A | `research/02-agent-a-draft.md` | draft, research, advance |
| AGENT-B | `research/03-agent-b-audit.md` | audit, challenge, find errors |
| Human   | `research/05-resolutions.md`, `logs/decisions.md` | arbitrate, decide to ship |
