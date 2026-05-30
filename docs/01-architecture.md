# 01. Architecture

[中文](./01-architecture.zh-CN.md) · [Back to README](../README.md)

## The problem

Single-agent AI research fails silently. The agent confidently writes a fee schedule, a config snippet, an API contract — and 30% of the time some specific number is wrong. Without a second pair of eyes, the error ships.

Human review catches a lot, but humans don't scale to every paragraph and don't have the patience to chase every cited URL.

A second agent does.

## The pattern

Run two agents with **different prompts, different models (ideally), independent contexts** — but pointed at the **same writeable knowledge base**. They take turns:

1. Agent A writes a draft.
2. Agent B reads, audits, comments inline, fixes errors.
3. Agent A reviews B's fixes, accepts or pushes back.
4. Conflicts that survive both passes → resolved against first-hand sources.

The shared knowledge base is an **Obsidian vault** because:
- Plain markdown files (diff-able, git-friendly)
- Wikilinks for cross-references
- Local-first (no cloud dependency)
- Free desktop app for the human reader

The sync substrate is **git** because:
- Already universal among developers
- Author identity per commit (audit trail)
- Branching/merging if you want it
- GitHub gives free private repos

The auto-sync to your laptop is **Obsidian Git plugin** (community, free) which polls and pushes/pulls on a timer.

## Topology

```
            ┌──────────────────────────────────┐
            │   GitHub repo (private)           │
            │   = single source of truth        │
            └──────────────────────────────────┘
              ▲          ▲           ▲
              │          │           │
       git    │   git    │   Obsidian Git plugin
       push   │   push   │   (auto pull/push)
              │          │           │
       ┌──────┴──┐  ┌────┴────┐  ┌───┴────────┐
       │ Agent A │  │ Agent B │  │ Your laptop │
       │ (VPS 1) │  │ (VPS 2) │  │ Obsidian    │
       └─────────┘  └─────────┘  └─────────────┘
```

Three writers, one truth. Each writer has its own git author identity, so `git log` is a complete provenance record.

## Why this beats Obsidian Sync, Notion, Google Docs

| Concern | This pattern | Obsidian Sync | Notion | Google Docs |
|---|---|---|---|---|
| Multi-agent write access | ✓ | ✗ (paid, single-user) | partial (API limits) | partial (heavy auth) |
| Per-paragraph authorship | ✓ (tags + git blame) | ✗ | comments only | suggestions only |
| Diffable history | ✓ (git) | versions only | partial | suggestions |
| Offline-first | ✓ | ✓ | ✗ | ✗ |
| Free | ✓ | ✗ ($4-8/mo) | freemium | free |
| Self-hostable | ✓ | ✗ | ✗ | ✗ |

The killer feature is **diffable per-author history**. When something goes wrong, `git blame` plus the `[AGENT-X]` tag tells you exactly who wrote it and when.

## Why it works (the boring reason)

Two agents disagreeing about a fact creates a **structured conflict** that's easy to resolve. The resolution rule — go to first-hand source — turns "agent vibes" into "what does the official doc say."

Single agents have no such forcing function. They smooth over their own uncertainty with confident prose.

## Failure modes this pattern handles

- **Hallucinated fee tiers** → caught by the other agent reading the same source
- **Stale cached info** → caught when the other agent fetches fresh
- **Wrong unit conventions** (bps vs %, daily vs annualized) → caught by per-paragraph audit
- **Outdated API endpoints** → caught when the other agent actually hits the URL

## Failure modes this pattern doesn't handle

- Both agents share a wrong assumption (rare, but possible — e.g. both trained on the same outdated docs)
- Both agents skip the first-hand check (mitigated by the rule, not the pattern)
- The shared knowledge base itself becomes corrupt (mitigated by git history)

For the first one, add a third agent or a human spot-check. For the second, the rule has to be enforced at prompt level — see [03-collaboration.md](./03-collaboration.md).

## Next

- [Setup](./02-setup.md) — get it running in 30 minutes
- [Collaboration rules](./03-collaboration.md) — the tagging + conflict protocol
