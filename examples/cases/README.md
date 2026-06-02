# Case library — Falsify isn't just for finance

Falsify works on **any fact-dense output**, not just trading/fees. Each sample below
is a realistic draft with **planted errors that would ship** — the kind a single
model writes confidently. Run the reviewer and watch them get caught:

```bash
falsify review examples/cases/tech-selection-sample.md -p deepseek
falsify review examples/cases/market-research-sample.md -p deepseek
```

| Case | Domain | Planted error types |
|---|---|---|
| [tech-selection-sample.md](./tech-selection-sample.md) | Engineering / architecture | unsupported benchmark · logic jump · missing source · scope overreach |
| [market-research-sample.md](./market-research-sample.md) | Market / competitor research | numbers that don't add up · stale stat as current · apples-to-oranges · unsupported conclusion |
| [reversal-sample.md](./reversal-sample.md) | Any (anti-laziness) | sycophantic reversal — an estimate cut ~10x with no new evidence |

The reversal sample needs the version-aware check (it compares against git history):

```bash
falsify review examples/cases/reversal-sample.md --against HEAD~1 -p deepseek
```

`--against <ref>` catches what a single review can't: a number/recommendation that
flipped because someone pushed back ("too long", "you're wrong"), not because the
data changed. That's the AI-laziness / sycophancy failure mode, made visible.

> Errors are **intentionally planted** and the content is illustrative. The point is
> the same across every domain: *without a second reviewer, these ship.*

Want your industry covered (legal, medical, product, academic)? That's exactly what
[Contributing](../../README.md#contributing) is for — a sanitized sample + the errors
it plants.
