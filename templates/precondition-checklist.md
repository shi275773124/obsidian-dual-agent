# Precondition Checklist (G1–G4)

> Run this before **any** outward claim — "X is Y", "passes / fails",
> "should / shouldn't", "archive it". v1's three rules check whether *facts* are
> right. These four gates check whether the *claim built on those facts* is even
> meaningful.
>
> The failure mode they catch: **right numbers, wrong conclusion.**

Copy this block per claim. A claim that can't clear all four gates is not ready
to ship — downgrade it to `[NEEDS-AUDIT]` or open a `[CONFLICT]`.

---

## Claim under test

> `<state the exact assertion, e.g. "Signal Z has no predictive value">`

### G1 — Entity disambiguation
*Is the X I'm talking about actually that X?*

- [ ] The subject of the claim is one specific, named thing (not a fuzzy bucket)
- [ ] I'm not collapsing "a part of X changed" into "X changed"
- [ ] Example trap: "the endpoint returns null" → "the product was shut down"

Notes:

### G2 — Unit / scale alignment
*If I convert the number to a human scale, is it still plausible?*

- [ ] Every rate has its period attached (per-hour? per-8h? annual?)
- [ ] I converted to a comparable scale before judging "big/small/reasonable"
- [ ] Example trap: "−0.5% per 8h" *feels* tiny — annualized it's ~−547%/yr

Notes:

### G3 — Prior-conflict = brake
*The operator (or strong prior evidence) disagrees with me. Do I slow down or double down?*

- [ ] When my result conflicts with the operator's prior, I **re-verify**, not defend
- [ ] I am not adding more evidence to win an argument I might be wrong about
- [ ] Example trap: operator says "that can't be right" → I pile on citations instead of rechecking

Notes:

### G4 — Ruler / object match
*Do my tool's assumptions match the data's structure?*

- [ ] The method's assumptions (density, distribution, stationarity, sample size) fit the data
- [ ] A "bad score" actually means the object is bad — not that the tool is wrong for it
- [ ] Example trap: a panel-R² goodness-of-fit test on a **sparse, event-driven** signal —
      the test assumes dense continuous data, so a low R² says nothing about the signal

Notes:

---

## Verdict

- [ ] All four gates cleared → claim may ship
- [ ] Any gate failed → claim blocked; reason: `<which gate, why>`
