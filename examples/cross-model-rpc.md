# Cross-model review without two machines

The v1 quickstart assumes two agents on two hosts syncing through git. You don't
actually need that. **Two different models + isolated context = enough independence.**

The reviewer can be a single call to a *different* model through any
OpenAI-compatible endpoint — the official OpenAI API, OpenRouter, a self-hosted
proxy (LiteLLM, etc.), or a local model server. The author drafts; you hand the
draft to a model from a different family and ask it to attack.

> Why a *different* family: a model reviewing its own output shares its own blind
> spots. Different lineage is what makes the audit adversarial instead of agreeable.

---

## The shape

- **Author** = your main session (Model A) → writes the draft to a file
- **Reviewer** = a one-shot call to Model B → reads the file, returns an attack
- Both sides read the same file (via git or a shared path) — no human relaying
- Reviewer's system prompt must say: *find holes, don't be polite, don't restate the author*

A full round is usually under a minute. Three rounds of draft → attack → fix is
a few minutes, not a few hours.

## Minimal reviewer call (any OpenAI-compatible endpoint)

```bash
# Endpoint + key come from env. NEVER hardcode or commit a key.
: "${REVIEW_API_BASE:?set REVIEW_API_BASE, e.g. https://api.openai.com/v1}"
: "${REVIEW_API_KEY:?set REVIEW_API_KEY}"
REVIEW_MODEL="${REVIEW_MODEL:-<a-model-from-a-different-family-than-the-author>}"

DRAFT_FILE="research/02-agent-a-draft.md"
OUT_FILE="research/03-agent-b-audit.md"

SYSTEM='You are Agent B, an adversarial reviewer. Find factual errors, flipped
signs, wrong units, entity mix-ups, and tool/assumption mismatches in the draft.
Do not be polite. Do not restate the author. For each issue give a verification
path (an official URL, an API call, or a source-code location). Output tagged
blocks starting with [AGENT-B audit].'

# Build the request with jq so the file content is safely JSON-encoded.
jq -n --arg sys "$SYSTEM" --rawfile draft "$DRAFT_FILE" --arg model "$REVIEW_MODEL" '
  {model:$model, messages:[
    {role:"system", content:$sys},
    {role:"user",   content:("Audit this draft:\n\n" + $draft)}
  ]}' \
| curl -s "$REVIEW_API_BASE/chat/completions" \
    -H "Authorization: Bearer $REVIEW_API_KEY" \
    -H "Content-Type: application/json" \
    -d @- \
| jq -r '.choices[0].message.content' \
> "$OUT_FILE"

echo "Audit written to $OUT_FILE"
```

## Notes

- Swap `REVIEW_API_BASE` for OpenRouter, a local proxy, or any OAI-compatible
  server — the call shape is identical.
- Keep keys in environment variables. The repo's `.gitignore` already excludes
  `.env`, `*.key`, etc. — don't defeat it.
- This pairs with the [verdict ladder](../docs/05-adversarial-review.md): run the
  reviewer, read the verdict, fix, and re-run until `PROCEED`.
- For multi-step pipelines, guard each step's output with
  [`templates/step-verify.sh`](../templates/step-verify.sh).
