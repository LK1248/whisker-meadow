"""Build docs/monetization/Whisker-Meadow-Monetization.pptx (opens in Google Slides) from the sim charts."""
import pathlib
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parents[2]
D = ROOT / 'docs' / 'monetization'
FOREST, MOSS, ROSE, INK, MUTED, WHITE, TINT = (RGBColor.from_string(x) for x in
    ('2E5E3E', 'A8C98A', 'D9506E', '23302A', '5F6B64', 'FFFFFF', 'EEF4EA'))
HEAD, BODY = 'Cambria', 'Calibri'

prs = Presentation()
prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
BLANK = prs.slide_layouts[6]

def bg(s, color):
    f = s.background.fill; f.solid(); f.fore_color.rgb = color

def text(s, x, y, w, h, runs, size=16, color=INK, font=BODY, bold=False, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, bullets=False, space=6):
    tb = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h)); tf = tb.text_frame
    tf.word_wrap = True; tf.vertical_anchor = anchor
    for m in ('margin_left', 'margin_right', 'margin_top', 'margin_bottom'): setattr(tf, m, 0)
    if isinstance(runs, str): runs = [runs]
    for i, r in enumerate(runs):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align; p.space_after = Pt(space)
        parts = r if isinstance(r, list) else [(('• ' if bullets else '') + r, bold)]
        for t, b in parts:
            run = p.add_run(); run.text = t; run.font.size = Pt(size); run.font.bold = b
            run.font.color.rgb = color; run.font.name = font
    return tb

def card(s, x, y, w, h, fill=TINT):
    sh = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    sh.adjustments[0] = 0.08; sh.fill.solid(); sh.fill.fore_color.rgb = fill; sh.line.fill.background(); sh.shadow.inherit = False
    return sh

def dot(s, x, y, d, color, label):
    c = s.shapes.add_shape(MSO_SHAPE.OVAL, Inches(x), Inches(y), Inches(d), Inches(d))
    c.fill.solid(); c.fill.fore_color.rgb = color; c.line.fill.background(); c.shadow.inherit = False
    tf = c.text_frame; tf.margin_left = tf.margin_right = 0
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER; r = p.add_run(); r.text = label
    r.font.size = Pt(16); r.font.bold = True; r.font.color.rgb = WHITE; r.font.name = BODY

def title(s, t, sub=None):
    text(s, 0.6, 0.45, 12.1, 0.8, t, size=34, color=FOREST, font=HEAD, bold=True)
    if sub: text(s, 0.6, 1.25, 12.1, 0.4, sub, size=15, color=MUTED)

def pic(s, name, x, y, w=None, h=None):
    W, H = Image.open(D / name).size
    if w and h:  # fit inside box
        if W / H > w / h: h = w * H / W
        else: w = h * W / H
    elif w: h = w * H / W
    else: w = h * W / H
    s.shapes.add_picture(str(D / name), Inches(x), Inches(y), Inches(w), Inches(h)); return w, h

def slide(dark=False):
    s = prs.slides.add_slide(BLANK); bg(s, FOREST if dark else WHITE); return s

def notes(s, t): s.notes_slide.notes_text_frame.text = t

# 1 title
s = slide(True)
text(s, 0.9, 2.2, 11.5, 1.2, 'Whisker Meadow', size=54, color=WHITE, font=HEAD, bold=True)
text(s, 0.9, 3.35, 11.5, 0.8, 'Economy, pacing and ads: what a simulated week of players tells us', size=24, color=MOSS)
text(s, 0.9, 5.6, 11.5, 0.5, 'Overnight analysis, 23 Nov 2026  ·  base game unchanged', size=14, color=WHITE)
notes(s, 'All numbers come from a copy of the real game driven by a scripted player (tools/sim). The shipped game was not touched.')

# 2 summary
s = slide(); title(s, 'Four things to take away')
items = [('15–45 min', 'Pacing is already on target. Keep today\'s costs and timings.'),
         ('$0', 'Money is almost never the gate. Stars and adoptions are. Selling money is pointless.'),
         ('−12 min', 'A "call a family now" rewarded ad gets engaged players to L8 about 12 minutes sooner.'),
         ('4.9 h vs 15.4 h', 'Endless acres to level 20: linear need with more families, vs today\'s accelerating curve.')]
for i, (big, small) in enumerate(items):
    x, y = 0.6 + (i % 2) * 6.15, 1.75 + (i // 2) * 2.7
    card(s, x, y, 5.9, 2.4)
    text(s, x + 0.35, y + 0.3, 5.2, 0.9, big, size=40, color=ROSE, font=HEAD, bold=True)
    text(s, x + 0.35, y + 1.25, 5.2, 1.0, small, size=16)

# 3 pacing
s = slide(); title(s, 'Players reach a new room every 3–15 minutes', 'Median minutes to each meadow level, no ads (3 casual, 4 engaged, 2 optimizer runs)')
pic(s, '01_progression.png', 0.5, 1.85, w=8.2)
text(s, 9.1, 2.0, 3.7, 4.8, ['Casual: L4 at 15 min, L6 at 38 min', 'Engaged: L5 at 17 min, L7 at 43 min', 'Optimizer: L8 at 59 min',
     'Fits the 15–45 minute session target: keep the numbers as they are.'], size=16, bullets=True, space=12)
notes(s, 'Treat these as a shape, not exact minutes: the bot never fumbles controls and skips the tutorial.')

# 4 gates
s = slide(); title(s, 'Stars gate the early game, adoptions gate the late game', 'Minutes spent waiting on each requirement before each expansion')
w, h = pic(s, '02_gates.png', 0.9, 1.8, w=11.5)
text(s, 0.6, 1.8 + h + 0.25, 12.1, 1.2, ['Stars hold back levels 2–5 (2–9 min each). Homes hold back levels 6–8 (5–16 min each).',
     'Money only gates casual players briefly around L5–L6. Family visits are the slow, out-of-your-hands part.'], size=16, bullets=True)

# 5 cash
s = slide(); title(s, 'Money snowballs and has nowhere to go', 'Cash earned over the first hour')
pic(s, '03_cash.png', 0.5, 1.85, w=8.2)
text(s, 9.1, 2.0, 3.7, 4.8, ['Earned in 60 min: casual ~$10k, engaged $25–59k, optimizer ~$145k',
     'All 7 expansions cost $9,320 in total', 'Fair prizes drive the snowball: the optimizer entered 1,255 fairs in an hour',
     'No late-game money sink yet'], size=16, bullets=True, space=12)

# 6 ads
s = slide(); title(s, 'Rewarded ads help only at the real bottleneck', 'Meadow level reached at 60 minutes')
pic(s, '04_ad_variants.png', 0.5, 1.85, w=8.2)
text(s, 9.1, 2.0, 3.7, 4.8, ['Engaged + family ad: L6 at 21 min instead of 33, 19 homes',
     'Casual + family ad backfired: fewer cats meant fewer donations, so money became the gate',
     '"Smart" offer that helps with whatever blocks the next room: a steady, modest gain'], size=16, bullets=True, space=12)
notes(s, 'Gains are about 10–15 minutes per hour: helpful, never an escape from a grind.')

# 7 poki rules
s = slide(); title(s, 'Poki\'s rules decide what is possible', 'From the Poki SDK docs and requirements')
rules = [('1', 'No purchases', 'No in-app purchases, no currency packs, no "remove ads". Only Poki\'s ads.'),
         ('2', 'No own ad timers', 'Call commercialBreak() at natural pauses. Poki decides whether an ad plays.'),
         ('3', 'Rewarded = announced', 'Players choose to watch, know the reward first, and get it only if the ad played.'),
         ('4', 'Pause the game', 'gameplayStop() before every break and gameplayStart() after.')]
for i, (n, h_, b) in enumerate(rules):
    x, y = 0.6 + (i % 2) * 6.15, 1.95 + (i // 2) * 2.45
    card(s, x, y, 5.9, 2.15); dot(s, x + 0.35, y + 0.35, 0.6, FOREST, n)
    text(s, x + 1.2, y + 0.38, 4.4, 0.5, h_, size=20, color=FOREST, font=HEAD, bold=True)
    text(s, x + 1.2, y + 0.95, 4.4, 1.1, b, size=15)
text(s, 0.6, 6.85, 12.1, 0.4, 'Sources: sdk.poki.com/html5.html · sdk.poki.com/new-requirements · developers.poki.com/guide/monetization', size=11, color=MUTED)

# 8 endless
s = slide(); title(s, 'Endless acres can stay fun or turn into a grind', 'Extra hours after level 8 for an engaged player, four designs')
pic(s, '05_endless.png', 0.5, 1.85, w=8.2)
text(s, 9.1, 2.0, 3.7, 4.8, ['Today\'s accelerating need: 15.4 h to L20, hopeless by L14–16',
     'Flat +8 homes per acre: 6.5 h', 'Growing need, but more families as the meadow grows: 4.9 h',
     'Same plus a family ad: 3.0 h. A shortcut, not an escape hatch'], size=16, bullets=True, space=12)

# 9 revenue
s = slide(); title(s, 'Rewarded offers could double to quadruple ad revenue', 'Illustrative gross $ per 1,000 players. Assumed eCPMs; Poki publishes no rates')
pic(s, '06_revenue.png', 0.5, 1.85, w=8.2)
text(s, 9.1, 2.0, 3.7, 4.8, ['Breaks only: $1.45–7.26', 'Light rewarded (~6/h): $3.66–15.53', 'Heavier rewarded (~14/h): $6.60–26.57',
     'The money comes from long sessions, so retention and revenue point the same way'], size=16, bullets=True, space=12)
notes(s, 'Assumptions: 40% of players leave at ~2 min, 30% at 6, 18% at 18, 8% at 38, 4% at 70. Breaks every 4 min after minute 4 at 60% fill. Rewarded offers after minute 5, 70% watched. eCPM low 1/4, mid 2.5/8, high 5/15 (commercial/rewarded).')

# 10 recommendations
s = slide(); title(s, 'What to build, in a way that never breaks the game')
cols = [('Ads', ['Breaks only at natural pauses: after a postcard, after an expansion', 'Nothing in the first 4–5 minutes',
                 'Rewarded offers tied to moments: "a family is on the way", "a stray needs rescue", "welcome back: double donations"',
                 'Never gate food or health behind an ad']),
        ('Long-term players', ['Endless acres with a linear need and more family visits', 'Money sinks: decor, cosmetics, themed areas',
                               '"Sister sanctuaries" prestige that keeps your album', 'Capped offline donations and seasonal events']),
        ('Balance later', ['Fair prizes snowball: cool down per cat or flatten high tiers', 'Casual players\' cats sit at 40–50 happiness',
                           'A hungry cat being petted never leaves to eat'])]
for i, (h_, bl) in enumerate(cols):
    x = 0.6 + i * 4.1
    card(s, x, 1.65, 3.85, 5.3)
    text(s, x + 0.3, 1.9, 3.3, 0.5, h_, size=22, color=ROSE if i < 2 else MUTED, font=HEAD, bold=True)
    text(s, x + 0.3, 2.6, 3.3, 4.2, bl, size=15, bullets=True, space=10)

# 11 next steps
s = slide(True)
text(s, 0.9, 1.0, 11.5, 0.9, 'Suggested next steps', size=40, color=WHITE, font=HEAD, bold=True)
text(s, 0.9, 2.2, 11.5, 4.5, ['1.  Keep levels 1–8 exactly as they are',
     '2.  Wire in the Poki SDK: gameplayStart/Stop and commercialBreak at natural pauses',
     '3.  Add one rewarded offer: "a family is on the way"',
     '4.  Add endless acres after level 8, then decor as a money sink',
     '5.  Re-run the simulator after each change (tools/sim)'], size=22, color=WHITE, space=14)

out = D / 'Whisker-Meadow-Monetization.pptx'; prs.save(out); print('saved', out)
