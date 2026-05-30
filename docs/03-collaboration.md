# 03. Collaboration Rules

[中文](./03-collaboration.zh-CN.md) · [Back to README](../README.md)

The pattern stops working the moment agents stop following these rules. Enforce them at prompt level.

## Rule 1 — Tag every paragraph

Every paragraph an agent writes is prefixed (or suffixed) with one of:

- `[AGENT-A]` — Agent A wrote this
- `[AGENT-B]` — Agent B wrote this
- `[BOTH]` — Both agents agree (after sync)

Code blocks, tables, and lists are tagged as units. Don't sprinkle tags inside a single bullet list — tag the list as a whole.

```markdown
[AGENT-A]
Lighter charges 0bps maker / 0bps taker for retail. The platform launched in 2024
with a ZK-rollup architecture and runs on its own L2.

[AGENT-B audit]: confirmed against https://docs.lighter.xyz/fees (fetched 2026-05-30)

[AGENT-B]
Adding context: Lighter Premium tier (≥$10M monthly volume) charges
0.004% / 0.028%. This applies only to whales — Chris's $200 capital is far below.

[BOTH]
Conclusion: for retail capital under $10k, Lighter is fee-free.
```

## Rule 2 — Don't rewrite the other agent's tagged blocks

If you disagree with `[AGENT-A]`'s paragraph, **don't edit it**. Choose one:

**Option A — inline audit note** (preferred for small fixes):

```markdown
[AGENT-A]
HL VIP0 maker fee is 1.5bps.

[AGENT-B audit]: incorrect. HL VIP0 maker is **rebate** -1.5bps (you receive 1.5bps),
not a charge. Source: https://app.hyperliquid.xyz/fees (2026-05-30).
```

**Option B — separate paragraph**:

```markdown
[AGENT-A]
trade.xyz Standard tier: 5.0bps maker / 1.5bps taker.

[AGENT-B]
Per official trade.xyz/fees (2026-05-30), Standard tier is **9.0bps / 3.0bps**.
[AGENT-A]'s numbers above are stale; flagging for revision.
```

**Option C — when both agree the original was wrong**, the original author edits their own block and adds a `[BOTH]` note:

```markdown
[AGENT-A — corrected 2026-05-30]
trade.xyz Standard tier: 9.0bps maker / 3.0bps taker.

[BOTH] verified against https://trade.xyz/fees on 2026-05-30.
```

## Rule 3 — Conflicts go to first-hand sources

When two agents disagree on a fact, **neither agent's confidence wins**. The conflict resolves only by:

1. Identifying the **authoritative source** (official docs > app screenshots > public API > X posts > KOL claims)
2. Fetching the source URL **right now** (not "I remember")
3. Pasting the relevant quote into the doc with the URL and timestamp
4. Updating the conflicting paragraph(s) to match

If no first-hand source exists, the fact is marked `[UNCONFIRMED]` and both agents move on. Do not invent a resolution.

```markdown
[CONFLICT — resolved 2026-05-30]
[AGENT-A] said Aster USD1 fee is 0.04%. [AGENT-B] said 0.5bps.
Resolution: per https://aster.exchange/fees (fetched 2026-05-30):
> "USD1 perpetuals: 0.04% maker / 0.04% taker"
[AGENT-A] was correct. [AGENT-B] confused units (0.04% = 4bps, not 0.5bps).
```

## Authority hierarchy (use this order)

1. Official API response (most authoritative — it's what the system actually does)
2. Official docs page on official domain
3. Official mobile app / web app screenshot
4. Verified team announcement (X/Discord/Telegram with official handle)
5. Source code on official GitHub
6. Trusted aggregator (DeFiLlama, Dune, etc.)
7. Community claims / KOL posts (lowest — easy to be wrong)

Anything below #4 should be marked `[UNCONFIRMED]` until promoted.

## Confidence tiers (mark on critical facts)

- **A** — first-hand source verified within last 7 days
- **B** — first-hand source verified, but >7 days old
- **C** — secondary source (aggregator, blog post)
- **D** — community claim, unverified

```markdown
[AGENT-A][A] Lighter retail fee: 0bps/0bps (verified 2026-05-30 via app)
[AGENT-A][C] Lighter daily volume: ~$200M (per DeFiLlama 2026-05-29)
[AGENT-A][D] Lighter targeting Q4 2026 token distribution (X rumor, unconfirmed)
```

## Write zones (who owns what)

To avoid two agents stomping on each other, define **write zones**:

- `agent-a-personal/` — Agent A only, B can read but not write
- `agent-b-personal/` — Agent B only, A can read but not write
- `shared/` — both can write, must follow tagging rules
- everything else — shared by default

This is a soft convention enforced by AGENTS.md, not a filesystem permission. Both agents have to respect it.

## Conflict resolution checklist

When you encounter a `[AGENT-X]` block you disagree with:

- [ ] Did I actually fetch the first-hand source? (Not from memory)
- [ ] Is my source higher in the authority hierarchy than theirs?
- [ ] Did I paste the quote + URL + timestamp?
- [ ] Did I add `[AGENT-Y audit]:` inline rather than rewriting their block?
- [ ] If we both agree on the fix, did the original author edit their block?
- [ ] Did I commit with my own git identity?

## Anti-patterns (don't do these)

- ❌ "I think Agent A is wrong" with no source check
- ❌ Editing Agent A's `[AGENT-A]` block to fix it
- ❌ Removing the `[AGENT-A]` tag entirely
- ❌ "Both agents agree" without actually consulting the other
- ❌ Citing your training data as authority ("I recall that…")
- ❌ Force-pushing to overwrite the other agent's commits

## Next

- [Troubleshooting](./04-troubleshooting.md) — what to do when this breaks
