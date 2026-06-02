#!/usr/bin/env python3
"""falsify — 证伪: give AI output a verdict before you trust it.

An Agent Review Kit CLI. Point it at an AI-written draft; a skeptic reviewer
(a different model) attacks it for factual errors, flipped signs, wrong units,
entity mix-ups, and tool/assumption mismatches, then returns a Verdict:

    PROCEED   — survived the attack, safe to ship
    HOLD      — issues found, must fix and re-run
    ARCHIVE   — structurally broken

Exit code mirrors the verdict (PROCEED=0, HOLD=1, ARCHIVE=2), so it drops
straight into CI: don't let AI output ship unreviewed.

Zero dependencies — Python 3.8+ stdlib only. Works with any OpenAI-compatible
endpoint (OpenAI, OpenRouter, a local proxy, ...).

    export FALSIFY_API_BASE=https://api.openai.com/v1
    export FALSIFY_API_KEY=sk-...
    export FALSIFY_MODEL=<reviewer model>          # Agent B (Skeptic)
    export FALSIFY_AUTHOR_MODEL=<author model>     # Agent A (defaults to MODEL)

    falsify lint   report.md           # deterministic, no API: tags + ship-blockers
    falsify review report.md           # skeptic attacks the draft -> Verdict
    falsify draft  brief.md -o draft.md
    falsify run    brief.md            # draft then review (full loop)
"""

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request

VERSION = "0.1.0"

# Audits (and this CLI's own glyphs) are UTF-8; Windows consoles default to a
# legacy codec that can't encode them. Force UTF-8 output where supported.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

# Markers that must not survive into a shippable doc.
SHIP_BLOCKERS = ["[CONFLICT]", "[NEEDS-SOURCE]", "[NEEDS-AUDIT]", "[UNCONFIRMED]"]
# Recognized author/status tags a prose block may start with.
TAG_RE = re.compile(r"^\s*\[(AGENT-A|AGENT-B|BOTH|RESOLUTION|CONFLICT|"
                    r"NEEDS-SOURCE|NEEDS-AUDIT|UNCONFIRMED|AGENT-B audit|"
                    r"AGENT-A audit)\b")

SKEPTIC_SYSTEM = """You are Agent B, the Skeptic — an adversarial reviewer. You do NOT
collaborate or restate the author. Your job is to make this draft's errors
impossible to ship quietly.

Attack the draft for:
- wrong numbers, flipped signs / directions, wrong units
- claims unsupported by their cited source
- stale / outdated facts
- secondary sources posing as first-hand
- misread tables (wrong row/column)
- G1 entity mix-ups: "part of X changed" stated as "X is dead"
- G2 scale errors: a number that's absurd once converted to a human scale
- G4 tool/assumption mismatch: the method's assumptions don't fit the data

Rules:
- Do not be polite. Do not rewrite the author's text.
- For every issue, give a concrete verification path (an official URL, an API
  call, or a source-code location).
- Output tagged findings, each starting with [AGENT-B audit].

End your response with EXACTLY one final line, nothing after it:
VERDICT: PROCEED    (no shippable error found)
or
VERDICT: HOLD       (fixable issues found — list them above)
or
VERDICT: ARCHIVE    (structurally broken, no fix revives it)
"""

AUTHOR_SYSTEM = """You are Agent A, the drafter. Produce a clear, auditable first draft
from the brief. Rules:
- Start every paragraph/table/list block with [AGENT-A].
- Every number, fee, date, or API behavior must cite a source.
- Mark anything uncertain [NEEDS-AUDIT] or [NEEDS-SOURCE]. Never invent a source.
- Your output must be auditable by a skeptic reviewer.
"""

EXIT = {"PROCEED": 0, "HOLD": 1, "ARCHIVE": 2}


def die(msg, code=3):
    print(f"falsify: {msg}", file=sys.stderr)
    sys.exit(code)


def read_file(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except OSError as e:
        die(f"cannot read {path}: {e}")


# ---------------------------------------------------------------- lint (no API)

def iter_blocks(text):
    """Yield (block_text, in_code_fence) for blank-line-separated blocks."""
    lines = text.splitlines()
    block, in_fence = [], False
    fence_block = False
    for line in lines:
        if line.strip().startswith("```"):
            in_fence = not in_fence
        if line.strip() == "" and not in_fence:
            if block:
                yield "\n".join(block), fence_block
                block, fence_block = [], False
        else:
            if not block and line.strip().startswith("```"):
                fence_block = True
            block.append(line)
    if block:
        yield "\n".join(block), fence_block


def is_prose(block):
    """A block that should carry an author tag (skip headings, code, lists, etc.)."""
    s = block.lstrip()
    if not s:
        return False
    skip_prefixes = ("#", "```", ">", "|", "-", "*", "+", "<", "![", "[!",
                     "1.", "2.", "3.", "4.", "5.", "6.", "7.", "8.", "9.")
    return not s.startswith(skip_prefixes)


def cmd_lint(args):
    text = read_file(args.file)
    untagged, blockers = [], []

    for block, is_fence in iter_blocks(text):
        if is_fence or not is_prose(block):
            continue
        if not TAG_RE.match(block):
            first = block.strip().splitlines()[0][:60]
            untagged.append(first)

    for marker in SHIP_BLOCKERS:
        n = text.count(marker)
        if n:
            blockers.append((marker, n))

    print(f"falsify lint · {args.file}")
    if untagged:
        print(f"\n  ✗ {len(untagged)} untagged prose block(s) — every block needs "
              f"[AGENT-A]/[AGENT-B]/[BOTH]:")
        for u in untagged[:10]:
            print(f"      … {u}")
        if len(untagged) > 10:
            print(f"      (+{len(untagged) - 10} more)")
    else:
        print("\n  ✓ every prose block is tagged")

    if blockers:
        print(f"\n  ✗ ship-blockers present (resolve before shipping):")
        for marker, n in blockers:
            print(f"      {marker} ×{n}")
    else:
        print("  ✓ no open ship-blockers")

    shippable = not untagged and not blockers
    print(f"\n  → {'SHIPPABLE' if shippable else 'NOT shippable'}")
    sys.exit(0 if shippable else 1)


# ---------------------------------------------------------------- API plumbing

def chat(system, user, model=None):
    base = os.environ.get("FALSIFY_API_BASE")
    key = os.environ.get("FALSIFY_API_KEY")
    model = model or os.environ.get("FALSIFY_MODEL")
    if not base:
        die("set FALSIFY_API_BASE (e.g. https://api.openai.com/v1)")
    if not key:
        die("set FALSIFY_API_KEY")
    if not model:
        die("set FALSIFY_MODEL (the reviewer model)")

    payload = json.dumps({
        "model": model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "temperature": 0.2,
    }).encode("utf-8")

    req = urllib.request.Request(
        base.rstrip("/") + "/chat/completions",
        data=payload,
        headers={"Authorization": f"Bearer {key}",
                 "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=180) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        die(f"API error {e.code}: {e.read().decode('utf-8', 'replace')[:300]}")
    except urllib.error.URLError as e:
        die(f"network error: {e.reason}")
    try:
        return data["choices"][0]["message"]["content"]
    except (KeyError, IndexError):
        die(f"unexpected API response: {json.dumps(data)[:300]}")


def parse_verdict(text):
    m = re.search(r"VERDICT:\s*(PROCEED|HOLD(?:-\d+)?|ARCHIVE)",
                  text, re.IGNORECASE)
    if not m:
        return None
    v = m.group(1).upper()
    return "HOLD" if v.startswith("HOLD") else v


def show_request(system, user, model):
    print("--- DRY RUN (no API call) ---")
    print(f"model:  {model or os.environ.get('FALSIFY_MODEL', '<unset>')}")
    print(f"base:   {os.environ.get('FALSIFY_API_BASE', '<unset>')}")
    print(f"\n[system]\n{system}\n\n[user]\n{user[:800]}"
          f"{'... (truncated)' if len(user) > 800 else ''}")


# ---------------------------------------------------------------- review / draft

def cmd_review(args):
    draft = read_file(args.file)
    user = f"Audit this draft. Find what would ship wrong.\n\n{draft}"
    if args.dry_run:
        show_request(SKEPTIC_SYSTEM, user, args.model)
        return
    out = chat(SKEPTIC_SYSTEM, user, args.model)
    print(out)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(out)
        print(f"\n[audit written to {args.out}]", file=sys.stderr)

    verdict = parse_verdict(out)
    if verdict is None:
        die("reviewer returned no parseable VERDICT line", 3)
    print(f"\n=== Verdict: {verdict} ===", file=sys.stderr)
    sys.exit(EXIT[verdict])


def cmd_draft(args):
    brief = read_file(args.file)
    user = f"Draft from this brief:\n\n{brief}"
    if args.dry_run:
        show_request(AUTHOR_SYSTEM, user, args.model)
        return
    model = args.model or os.environ.get("FALSIFY_AUTHOR_MODEL")
    out = chat(AUTHOR_SYSTEM, user, model)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(out)
        print(f"[draft written to {args.out}]", file=sys.stderr)
    else:
        print(out)


def cmd_run(args):
    """Full loop: author drafts from the brief, then skeptic reviews."""
    brief = read_file(args.file)
    model = args.model or os.environ.get("FALSIFY_AUTHOR_MODEL")
    if args.dry_run:
        show_request(AUTHOR_SYSTEM, f"Draft from this brief:\n\n{brief}", model)
        return
    print("[1/2] Agent A drafting…", file=sys.stderr)
    draft = chat(AUTHOR_SYSTEM, f"Draft from this brief:\n\n{brief}", model)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(draft)
    print("[2/2] Agent B (Skeptic) reviewing…", file=sys.stderr)
    audit = chat(SKEPTIC_SYSTEM,
                 f"Audit this draft. Find what would ship wrong.\n\n{draft}",
                 None)
    print(audit)
    verdict = parse_verdict(audit)
    if verdict is None:
        die("reviewer returned no parseable VERDICT line", 3)
    print(f"\n=== Verdict: {verdict} ===", file=sys.stderr)
    sys.exit(EXIT[verdict])


def main():
    p = argparse.ArgumentParser(
        prog="falsify",
        description="证伪 — give AI output a verdict before you trust it.")
    p.add_argument("--version", action="version",
                   version=f"falsify {VERSION}")
    sub = p.add_subparsers(dest="cmd", required=True)

    pl = sub.add_parser("lint", help="deterministic tag + ship-blocker check (no API)")
    pl.add_argument("file")
    pl.set_defaults(func=cmd_lint)

    pr = sub.add_parser("review", help="skeptic reviewer attacks a draft -> Verdict")
    pr.add_argument("file")
    pr.add_argument("-o", "--out", help="write the audit to a file")
    pr.add_argument("-m", "--model", help="override reviewer model")
    pr.add_argument("--dry-run", action="store_true", help="print request, don't call")
    pr.set_defaults(func=cmd_review)

    pd = sub.add_parser("draft", help="author model drafts from a brief")
    pd.add_argument("file")
    pd.add_argument("-o", "--out", help="write the draft to a file")
    pd.add_argument("-m", "--model", help="override author model")
    pd.add_argument("--dry-run", action="store_true")
    pd.set_defaults(func=cmd_draft)

    prun = sub.add_parser("run", help="full loop: draft then review")
    prun.add_argument("file")
    prun.add_argument("-o", "--out", help="write the intermediate draft to a file")
    prun.add_argument("-m", "--model", help="override author model")
    prun.add_argument("--dry-run", action="store_true")
    prun.set_defaults(func=cmd_run)

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
