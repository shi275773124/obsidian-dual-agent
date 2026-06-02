#!/usr/bin/env python3
"""Render assets/demo.gif — a terminal-style animation of a real `falsify review`
run. Lines are faithful (trimmed) excerpts of an actual DeepSeek-as-Skeptic audit
of examples/comparison-case-study/01-agent-a-draft-excerpt.md (Verdict: HOLD).

    python assets/make-demo-gif.py
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1100, 520
BG = (13, 17, 23)
BAR = (22, 27, 34)
DOT = [(248, 81, 73), (210, 153, 34), (63, 185, 80)]
GREEN = (63, 185, 80)
WHITE = (230, 237, 243)
ORANGE = (240, 136, 62)
GRAY = (139, 148, 158)
RED = (248, 81, 73)

PADX, TOP, LH = 40, 70, 36
FONTS = "C:/Windows/Fonts/"
mono = ImageFont.truetype(FONTS + "consola.ttf", 21)
monob = ImageFont.truetype(FONTS + "consolab.ttf", 22)

CMD = "$ falsify review report.md"
LINES = [
    ('[AGENT-B audit] ', 'Venue A row is fabricated — "copied from a peer venue."'),
    ('[AGENT-B audit] ', 'Venue B "+1.5 bps" maker: sign likely flipped (rebate?).'),
    ('[AGENT-B audit] ', 'Venue C row is empty — a hole, not a data point.'),
    ('[AGENT-B audit] ', 'Venue D "flat across collateral": unsupported, no source.'),
    ('[AGENT-B audit] ', 'whole table = placeholders shipped as real numbers.'),
]
VERDICT = "=== Verdict: HOLD ==="
VTAIL = "   exit 1 · don't ship"


def frame(typed, n_lines, verdict, cursor):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    # title bar
    d.rectangle([0, 0, W, 44], fill=BAR)
    for i, c in enumerate(DOT):
        d.ellipse([20 + i * 26, 16, 32 + i * 26, 28], fill=c)
    d.text((W // 2 - 90, 13), "falsify — the Skeptic reviews", font=mono, fill=GRAY)

    y = TOP
    # command line
    x = PADX
    d.text((x, y), "$", font=monob, fill=GREEN)
    cmd_body = typed[1:] if typed.startswith("$") else typed
    d.text((x + d.textlength("$", font=monob), y), cmd_body, font=monob, fill=WHITE)
    if cursor and n_lines == 0 and not verdict:
        cx = x + d.textlength(typed, font=monob)
        d.rectangle([cx + 2, y + 2, cx + 13, y + 26], fill=WHITE)
    y += LH + 12

    for i in range(n_lines):
        prefix, body = LINES[i]
        d.text((PADX, y), prefix, font=mono, fill=ORANGE)
        d.text((PADX + d.textlength(prefix, font=mono), y), body, font=mono, fill=GRAY)
        y += LH

    if verdict:
        y += 14
        d.text((PADX, y), VERDICT, font=monob, fill=RED)
        d.text((PADX + d.textlength(VERDICT, font=monob), y), VTAIL,
               font=mono, fill=GRAY)
    return img


frames, durs = [], []

# 1) type the command
for i in range(0, len(CMD) + 1, 2):
    frames.append(frame(CMD[:i], 0, False, True)); durs.append(55)
# blink cursor on full command
for _ in range(2):
    frames.append(frame(CMD, 0, False, True)); durs.append(260)
    frames.append(frame(CMD, 0, False, False)); durs.append(260)
# 2) reveal audit lines one by one
for n in range(1, len(LINES) + 1):
    frames.append(frame(CMD, n, False, False)); durs.append(430)
# 3) verdict
frames.append(frame(CMD, len(LINES), True, False)); durs.append(2600)

out = os.path.join(os.path.dirname(__file__), "demo.gif")
frames[0].save(out, save_all=True, append_images=frames[1:], duration=durs,
               loop=0, optimize=True, disposal=2)
print(f"wrote {out} · {len(frames)} frames · {sum(durs)/1000:.1f}s loop")
