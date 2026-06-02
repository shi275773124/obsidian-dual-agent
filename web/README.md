# falsify web (local POC)

Paste-and-go in the browser: one box, one button — **find what's wrong before you ship.**
A skeptic model takes your AI output apart and returns a Verdict + the top risks.

```bash
pip install -e .              # or just keep falsify.py on the path
export DEEPSEEK_API_KEY=sk-...        # or set FALSIFY_PROVIDER in a .falsify
python web/serve.py                   # → http://127.0.0.1:8000
```

- Pick a scenario (general / tech selection / competitor / PR / research) — it tunes what the Skeptic looks for.
- Output: a **Verdict** (PROCEED / HOLD / ARCHIVE) + up to 5 ranked risks, each tagged by type (number / logic / source / stale / scope).
- Zero dependencies (Python stdlib only). Reuses [`falsify.py`](../falsify.py) for the model call and config.

> This local POC uses **your** key. The hosted "try 3× free, no key" experience is a
> separate deployment — this is its seed. Don't commit keys; `.falsify` is gitignored.
