#!/usr/bin/env python3
"""falsify — 证伪: give AI output a verdict before you trust it.

An Agent Review Kit CLI. Point it at an AI-written draft; a skeptic reviewer
(a different model) attacks it for factual errors, flipped signs, wrong units,
entity mix-ups, and tool/assumption mismatches, then returns a Verdict:

    PROCEED   — survived the attack, safe to ship
    HOLD      — issues found, must fix and re-run
    ARCHIVE   — structurally broken

Exit code mirrors the verdict (PROCEED=0, HOLD=1, ARCHIVE=2), so it drops
straight into CI. Zero dependencies — Python 3.8+ stdlib only. Works with any
OpenAI-compatible endpoint.

One-command setup with a provider preset (only the key is required):

    export DEEPSEEK_API_KEY=sk-...
    falsify review report.md --provider deepseek

Or set it once in ./.falsify or ~/.falsify (run `falsify init`), then:

    falsify review report.md
    cat report.md | falsify review -        # paste-and-go via stdin

    falsify lint   report.md               # no API: tags + ship-blockers
    falsify run    brief.md                # full loop: draft then review
"""

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

VERSION = "0.2.0"

# provider -> (base_url, default_model, key_env). model None = user must set one.
PRESETS = {
    "deepseek":    ("https://api.deepseek.com/v1",   "deepseek-chat", "DEEPSEEK_API_KEY"),
    "openai":      ("https://api.openai.com/v1",       None,          "OPENAI_API_KEY"),
    "openrouter":  ("https://openrouter.ai/api/v1",    None,          "OPENROUTER_API_KEY"),
    "moonshot":    ("https://api.moonshot.cn/v1",      None,          "MOONSHOT_API_KEY"),
    "siliconflow": ("https://api.siliconflow.cn/v1",   None,          "SILICONFLOW_API_KEY"),
    "local":       ("http://127.0.0.1:4163/v1",        None,          None),
}

SHIP_BLOCKERS = ["[CONFLICT]", "[NEEDS-SOURCE]", "[NEEDS-AUDIT]", "[UNCONFIRMED]"]
TAG_RE = re.compile(r"^\s*\[(AGENT-A|AGENT-B|BOTH|RESOLUTION|CONFLICT|"
                    r"NEEDS-SOURCE|NEEDS-AUDIT|UNCONFIRMED|AGENT-B audit|"
                    r"AGENT-A audit)\b")

SKEPTIC_SYSTEM = """You are Agent B, the Skeptic — an adversarial reviewer. You do NOT
collaborate or restate the author. Your job is to make this draft's errors
impossible to ship quietly.

Attack the draft for:
- wrong numbers, flipped signs / directions, wrong units
- claims unsupported by their cited source
- stale / outdated facts, secondary sources posing as first-hand
- misread tables (wrong row/column)
- G1 entity mix-ups: "part of X changed" stated as "X is dead"
- G2 scale errors: a number that's absurd once converted to a human scale
- G4 tool/assumption mismatch: the method's assumptions don't fit the data

Rules:
- Do not be polite. Do not rewrite the author's text.
- For every issue, give a concrete verification path (an official URL, an API
  call, or a source-code location).
- You only see THIS document. Do NOT claim that a file, tool, or repo "does not
  exist" just because it isn't in front of you — if you can't verify a referenced
  thing from the text, say so, don't assert it's fake.
- List each DISTINCT issue once, most important first, at most ~8. Never repeat.
- Output tagged findings, each starting with [AGENT-B audit].

End with EXACTLY one final line, nothing after it:
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
MAX_TOKENS = 2048


def die(msg, code=3):
    print(f"falsify: {msg}", file=sys.stderr)
    sys.exit(code)


# ------------------------------------------------------------ config resolution

def load_config():
    """First of ./.falsify or ~/.falsify wins. Simple KEY=VALUE lines."""
    cfg = {}
    for p in (Path(".falsify"), Path.home() / ".falsify"):
        try:
            if not p.is_file():
                continue
            for line in p.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, v = line.split("=", 1)
                cfg[k.strip()] = v.strip().strip('"').strip("'")
            break
        except OSError:
            continue
    return cfg


CFG = load_config()


def setting(name, default=None):
    return os.environ.get(name) or CFG.get(name) or default


def resolve(args):
    """Resolve base / key / model from flags > env > .falsify > provider preset."""
    provider = (getattr(args, "provider", None) or setting("FALSIFY_PROVIDER") or "").lower()
    base = getattr(args, "base", None) or setting("FALSIFY_API_BASE")
    model = getattr(args, "model", None) or setting("FALSIFY_MODEL")
    key = setting("FALSIFY_API_KEY")

    if provider:
        if provider not in PRESETS:
            die(f"unknown --provider '{provider}'. Known: {', '.join(PRESETS)}")
        pbase, pmodel, pkey_env = PRESETS[provider]
        base = base or pbase
        model = model or pmodel
        if not key and pkey_env:
            key = os.environ.get(pkey_env) or CFG.get(pkey_env)

    if not key:  # last-resort: any common provider key already in the env
        for env in ("FALSIFY_API_KEY", "DEEPSEEK_API_KEY", "OPENAI_API_KEY",
                    "OPENROUTER_API_KEY", "MOONSHOT_API_KEY", "SILICONFLOW_API_KEY"):
            if os.environ.get(env):
                key = os.environ[env]
                break
    return base, key, model


# ----------------------------------------------------------------- I/O + API

def read_input(path):
    if path == "-":
        return sys.stdin.read()
    try:
        return Path(path).read_text(encoding="utf-8")
    except OSError as e:
        die(f"cannot read {path}: {e}")


def chat(system, user, base, key, model):
    if not base:
        die("no endpoint. Set --provider <name>, or FALSIFY_API_BASE, or run `falsify init`.")
    if not key:
        die("no API key. Set FALSIFY_API_KEY (or a provider key like DEEPSEEK_API_KEY).")
    if not model:
        die("no model. Set --model, FALSIFY_MODEL, or use a --provider with a default.")

    payload = json.dumps({
        "model": model,
        "messages": [{"role": "system", "content": system},
                     {"role": "user", "content": user}],
        "temperature": 0.2,
        "max_tokens": MAX_TOKENS,
    }).encode("utf-8")
    req = urllib.request.Request(
        base.rstrip("/") + "/chat/completions", data=payload,
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        method="POST")
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
    m = re.search(r"VERDICT:\s*(PROCEED|HOLD(?:-\d+)?|ARCHIVE)", text, re.IGNORECASE)
    if not m:
        return None
    v = m.group(1).upper()
    return "HOLD" if v.startswith("HOLD") else v


def finish(audit, verdict_text=None):
    """Print audit, resolve verdict (no explicit verdict -> HOLD), exit by code."""
    print(audit)
    v = parse_verdict(verdict_text if verdict_text is not None else audit)
    if v is None:
        v = "HOLD"
        print("\n[no explicit VERDICT line — defaulting to HOLD]", file=sys.stderr)
    print(f"\n=== Verdict: {v} ===", file=sys.stderr)
    sys.exit(EXIT[v])


# ----------------------------------------------------------------- commands

def iter_blocks(text):
    block, in_fence, fence_block = [], False, False
    for line in text.splitlines():
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
    s = block.lstrip()
    skip = ("#", "```", ">", "|", "-", "*", "+", "<", "![", "[!",
            "1.", "2.", "3.", "4.", "5.", "6.", "7.", "8.", "9.")
    return bool(s) and not s.startswith(skip)


def cmd_lint(args):
    text = read_input(args.file)
    untagged = [b.strip().splitlines()[0][:60]
                for b, fence in iter_blocks(text)
                if not fence and is_prose(b) and not TAG_RE.match(b)]
    blockers = [(m, text.count(m)) for m in SHIP_BLOCKERS if text.count(m)]

    print(f"falsify lint · {args.file}")
    if untagged:
        print(f"\n  ✗ {len(untagged)} untagged prose block(s):")
        for u in untagged[:10]:
            print(f"      … {u}")
    else:
        print("\n  ✓ every prose block is tagged")
    if blockers:
        print("\n  ✗ ship-blockers present:")
        for m, n in blockers:
            print(f"      {m} ×{n}")
    else:
        print("  ✓ no open ship-blockers")
    ok = not untagged and not blockers
    print(f"\n  → {'SHIPPABLE' if ok else 'NOT shippable'}")
    sys.exit(0 if ok else 1)


def cmd_review(args):
    base, key, model = resolve(args)
    draft = read_input(args.file)
    user = f"Audit this draft. Find what would ship wrong.\n\n{draft}"
    if args.dry_run:
        print(f"[dry-run] base={base} model={model}\n\n{SKEPTIC_SYSTEM}")
        return
    out = chat(SKEPTIC_SYSTEM, user, base, key, model)
    if args.out:
        Path(args.out).write_text(out, encoding="utf-8")
        print(f"[audit written to {args.out}]", file=sys.stderr)
    finish(out)


def cmd_draft(args):
    base, key, model = resolve(args)
    brief = read_input(args.file)
    out = chat(AUTHOR_SYSTEM, f"Draft from this brief:\n\n{brief}", base, key, model)
    if args.out:
        Path(args.out).write_text(out, encoding="utf-8")
        print(f"[draft written to {args.out}]", file=sys.stderr)
    else:
        print(out)


def cmd_run(args):
    base, key, model = resolve(args)
    brief = read_input(args.file)
    print("[1/2] Agent A drafting…", file=sys.stderr)
    draft = chat(AUTHOR_SYSTEM, f"Draft from this brief:\n\n{brief}", base, key, model)
    if args.out:
        Path(args.out).write_text(draft, encoding="utf-8")
    print("[2/2] Agent B (Skeptic) reviewing…", file=sys.stderr)
    audit = chat(SKEPTIC_SYSTEM,
                 f"Audit this draft. Find what would ship wrong.\n\n{draft}",
                 base, key, model)
    finish(audit)


def cmd_init(args):
    target = Path(".falsify")
    if target.exists() and not args.force:
        die(f"{target} already exists (use --force to overwrite)", 1)
    target.write_text(
        "# falsify config — settings here are picked up automatically.\n"
        "# Pick a provider preset (deepseek/openai/openrouter/moonshot/siliconflow/local):\n"
        "FALSIFY_PROVIDER=deepseek\n"
        "# Override the model if you want a specific one:\n"
        "# FALSIFY_MODEL=deepseek-chat\n"
        "# Key: prefer an env var (DEEPSEEK_API_KEY / OPENAI_API_KEY / ...) over writing it here.\n"
        "# FALSIFY_API_KEY=sk-...\n",
        encoding="utf-8")
    print(f"wrote {target}. Set your key in the environment, then: falsify review <file>")


def main():
    p = argparse.ArgumentParser(prog="falsify",
                                description="证伪 — give AI output a verdict before you trust it.")
    p.add_argument("--version", action="version", version=f"falsify {VERSION}")
    sub = p.add_subparsers(dest="cmd", required=True)

    def add_api_flags(sp):
        sp.add_argument("-p", "--provider", help="endpoint preset: " + ", ".join(PRESETS))
        sp.add_argument("-m", "--model", help="override model")
        sp.add_argument("--base", help="override API base URL")

    pl = sub.add_parser("lint", help="tag + ship-blocker check (no API)")
    pl.add_argument("file")
    pl.set_defaults(func=cmd_lint)

    pr = sub.add_parser("review", help="skeptic reviewer attacks a draft -> Verdict")
    pr.add_argument("file", help="file path, or - for stdin")
    pr.add_argument("-o", "--out", help="write the audit to a file")
    pr.add_argument("--dry-run", action="store_true")
    add_api_flags(pr)
    pr.set_defaults(func=cmd_review)

    pd = sub.add_parser("draft", help="author model drafts from a brief")
    pd.add_argument("file", help="file path, or - for stdin")
    pd.add_argument("-o", "--out")
    add_api_flags(pd)
    pd.set_defaults(func=cmd_draft)

    prun = sub.add_parser("run", help="full loop: draft then review")
    prun.add_argument("file", help="file path, or - for stdin")
    prun.add_argument("-o", "--out", help="write the intermediate draft to a file")
    add_api_flags(prun)
    prun.set_defaults(func=cmd_run)

    pi = sub.add_parser("init", help="write a .falsify config template")
    pi.add_argument("--force", action="store_true")
    pi.set_defaults(func=cmd_init)

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
