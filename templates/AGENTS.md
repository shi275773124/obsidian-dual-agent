# AGENTS.md — Dual-Agent Vault Rules

> Drop this file at the root of your shared vault. Both agents must read it at the start of every session.

You are one of two agents collaborating on this knowledge base. Your identity is **AGENT-A** or **AGENT-B** — the host config tells you which.

## Hard rules

### 1. Pull before writing

```bash
cd <vault-path>
git pull --rebase
```

If pull fails (merge conflict, network), STOP and report. Do not write until vault is in sync with origin.

### 2. Read the index first

Open `🏠 ops-knowledge-base.md` (or `🏠 运维知识库.md`) before any non-trivial write. It tells you which folders matter for the current task.

Priority folders:
- `current-truth/` — the canonical state of things (what's running, what config, what credentials)
- `methodology/` — how-tos, patterns, decisions
- `system-map/` — architecture diagrams, dependency maps
- `runbooks/` — step-by-step ops procedures
- `incidents/` — postmortems
- `change-log/` — every production change with rollback notes
- `research/` — investigations, comparisons, deep-dives

### 3. Tag every paragraph

Every paragraph, code block, table, or list block you write must be prefixed with one of:

- `[AGENT-A]` — Agent A wrote this
- `[AGENT-B]` — Agent B wrote this
- `[BOTH]` — both agents have synced and agree

No untagged prose. Ever.

### 4. Don't rewrite the other agent's tagged blocks

If you disagree with `[AGENT-A]`'s text, do **not** edit their block. Instead:

- **Inline audit note**: add `[AGENT-B audit]: <correction with source URL>` underneath
- **New paragraph**: add a `[AGENT-B]` paragraph with the corrected info
- **Both agree on rewrite**: only the original author edits their block, then add `[BOTH]` confirmation

### 5. Conflicts go to first-hand sources

When two agents disagree on a fact, neither wins by assertion. Resolve by:

1. Identify the authoritative source (official API > official docs > official app > verified team announcement > source code > aggregator > KOL claim)
2. Fetch the URL **right now**
3. Paste the relevant quote with URL + timestamp
4. Update the conflicting paragraph(s) to match

If no first-hand source exists, mark the fact `[UNCONFIRMED]` and move on. Never invent a resolution.

### 6. Commit with your own identity

```bash
git config user.name  "Agent A"      # or "Agent B"
git config user.email "agent-a@yourdomain.local"
git commit -m "[AGENT-X] <short topic>"
git push
```

`git log` should always tell you which agent wrote which commit.

### 7. After production changes, write a change log

Any change to a running system (config edit, service restart, deploy, schema change) gets:

- A new file in `change-log/YYYY-MM-DD-<topic>.md`
- Authored with your `[AGENT-X]` tag
- Including: what changed, why, rollback procedure, verification command
- Linked from `current-truth/` if it changed canonical state

## Confidence tiers (use on critical facts)

- `[A]` — first-hand source verified within last 7 days
- `[B]` — first-hand source verified, but >7 days old
- `[C]` — secondary source (aggregator, blog post)
- `[D]` — community claim, unverified

Example: `[AGENT-A][A] HL VIP0 maker rebate: -1.5bps (verified 2026-05-30 via app)`

## Write zones

- `agent-a-personal/` — Agent A only
- `agent-b-personal/` — Agent B only
- everything else — shared, follow tagging rules

## Never do these

- ❌ Write without pulling first
- ❌ Edit another agent's `[AGENT-X]` block to "fix" it
- ❌ Strip tags from existing paragraphs
- ❌ Cite training data as authority ("I recall that...")
- ❌ `git push --force` (use `--force-with-lease` only if absolutely needed and after explicit operator approval)
- ❌ Commit secrets (API keys, tokens, passwords) — even in private repos

## Session checklist (run at every session start)

```bash
cd <vault-path>
git pull --rebase
git status                                    # should be clean
git config user.name                          # should be "Agent A" or "Agent B"
grep -c "AGENT-A\|AGENT-B\|BOTH" recent-edits.md  # tags present
```

Read `🏠 ops-knowledge-base.md`. Then begin work.
