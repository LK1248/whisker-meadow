"""v98: when a lesson is waiting for you to pick a tool (brush for fleas/brushing, wand), that tool pulses with a pink
ring in the dock until it's picked. The flea lesson's bubble also stays up for the whole lesson instead of fading."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    if s.count(old) != count: sys.exit(f'match count {s.count(old)} != {count} for: {old[:80]}')
    s = s.replace(old, new)
rep("el.style.opacity=tips.t>T.dur-0.6?0:1;", "el.style.opacity=tips.t>T.dur-0.6&&T.kind!=='flea'?0:1;")
rep(".tool.on{background:#ffe3ec;color:var(--pinkd)}",
    ".tool.on{background:#ffe3ec;color:var(--pinkd)}\n"
    "body.tutLock .tool.tutOk:not(.on){animation:pulse 1.1s ease-in-out infinite;background:#ffe3ec;color:var(--pinkd);box-shadow:0 0 0 3px var(--pink)}")
open(P, 'w', encoding='utf-8').write(s); print('ok')
