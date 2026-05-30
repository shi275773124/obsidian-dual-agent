# Obsidian Dual-Agent Vault

> Two AI agents. One Obsidian vault. Git-synced. Conflict-resolved by first-hand sources, not vibes.

[![Link Check](https://github.com/shi275773124/obsidian-dual-agent/actions/workflows/link-check.yml/badge.svg)](https://github.com/shi275773124/obsidian-dual-agent/actions/workflows/link-check.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![中文](https://img.shields.io/badge/lang-中文-red.svg)](./README.zh-CN.md)

[中文版](./README.zh-CN.md) · [Architecture](./docs/01-architecture.md) · [Setup](./docs/02-setup.md) · [Collaboration Rules](./docs/03-collaboration.md) · [Troubleshooting](./docs/04-troubleshooting.md)

---

## What this is

A blueprint for letting **two independent AI agents collaborate inside a single Obsidian vault** — each writing, reviewing, and conflict-resolving the other's work, with full audit trail via git.

Works with any agent that can:
- Run shell commands (read/write files)
- Make git commits
- Read markdown

Tested with **Hermes Agent** (two profiles: `default` + `second`), but the pattern is agent-agnostic — drop in Claude Code, Cursor, OpenCode, or your own.

## Why

Single-agent research has a known failure mode: the agent fabricates plausible-but-wrong details, and there's nobody to catch it. Adding a second agent with **independent prompts and a shared writeable knowledge base** turns hallucinations into visible disagreements you can resolve against first-hand sources.

Real example that motivated this repo: two agents researched perp DEX fee schedules. Agent A wrote the report; Agent B audited and found **4 fee errors** (Lighter rebate sign flipped, HL VIP0 maker rebate wrong, trade.xyz Standard tier off, Aster USD1 row off). Without Agent B, those errors would have shipped.

## Architecture (90 seconds)

```
┌─────────────────┐         ┌─────────────────┐
│   Agent A       │         │   Agent B       │
│   (e.g. VPS-1)  │         │   (e.g. VPS-2)  │
└────────┬────────┘         └────────┬────────┘
         │                           │
         │  git push / pull          │  git push / pull
         ▼                           ▼
        ┌──────────────────────────────┐
        │   GitHub (private repo)       │
        │   = single source of truth    │
        └──────────────────────────────┘
                      ▲
                      │  Obsidian Git plugin
                      │  (5-min auto pull, 10-min auto push)
                      │
        ┌──────────────────────────────┐
        │   Your laptop                 │
        │   Obsidian app reads vault    │
        └──────────────────────────────┘
```

Each agent commits with **its own author identity**. Each block of prose is tagged `[AGENT-A]` / `[AGENT-B]` / `[BOTH]`. Conflicts get adjudicated by reading first-hand docs (official API, RFC, source code) — not by argument.

## 5-minute quickstart

```bash
# 1. Create a private GitHub repo (call it whatever — agent-vault, ops-notes, etc.)

# 2. On Agent A's host
git clone git@github.com:you/your-vault.git
cd your-vault
cp /path/to/this-repo/templates/AGENTS.md ./AGENTS.md
cp /path/to/this-repo/templates/.gitignore ./.gitignore
git add . && git commit -m "init: dual-agent rules" && git push

# 3. On Agent B's host
git clone git@github.com:you/your-vault.git
# (uses the same AGENTS.md you just committed)

# 4. On your laptop
git clone git@github.com:you/your-vault.git "$HOME/Documents/Obsidian Vault"
# Open the folder in Obsidian → install Obsidian Git community plugin
# Settings: Auto pull every 5 min, Auto push every 10 min
```

Now both agents and your laptop converge on the same vault. Full step-by-step in [docs/02-setup.md](./docs/02-setup.md).

## Collaboration rules (the important part)

Three rules. Memorize them.

1. **Tag every paragraph** with `[AGENT-A]`, `[AGENT-B]`, or `[BOTH]`. No untagged prose.
2. **Don't rewrite the other agent's tagged blocks.** Add your own block underneath instead, or add `[AGENT-B audit]:` inline notes.
3. **Conflicts go to first-hand sources.** If A says fee is 4.5bps and B says 9.0bps, neither wins by assertion — open the official docs URL, paste the quote, cite it.

Full conflict protocol + write-zone rules: [docs/03-collaboration.md](./docs/03-collaboration.md).

## What's in this repo

```
.
├── README.md                    (you are here)
├── README.zh-CN.md
├── docs/
│   ├── 01-architecture.md       why and how it works
│   ├── 02-setup.md              VPS + laptop step-by-step
│   ├── 03-collaboration.md      tagging, conflict resolution
│   └── 04-troubleshooting.md    git conflicts, plugin issues
├── templates/
│   ├── AGENTS.md                drop into your vault root
│   ├── .gitignore               sensible Obsidian defaults
│   └── obsidian-git-settings.md plugin config snippet
└── LICENSE                       MIT
```

## Real-world case study

The workflow in this repo produced a **12-venue Perp DEX fee + airdrop research report**, co-authored by two independent Hermes agents over ~6 hours. Agent A drafted, Agent B audited, conflicts resolved against official docs. The final report has 80+ cited URLs and per-paragraph authorship.

The agents disagreed on 4 fee tiers. Going to first-hand docs settled all 4 — none of them by Agent A's original numbers.

## License

MIT — fork it, ship it, write a blog post about it.
