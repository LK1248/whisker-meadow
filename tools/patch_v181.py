"""v181: a cat petted in its loaf can again roll onto its side and offer its belly after a few seconds of petting,
the same way as any petted cat (and the belly rub lesson can start from it). It still doesn't stand up or turn."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count: sys.exit(f'match count {n} != {count} for: {old[:80]}')
    s = s.replace(old, new)

rep("c.state==='pet'&&!c.loafPet&&!lessonOn()&&W.stat.bellyTip", "c.state==='pet'&&!lessonOn()&&W.stat.bellyTip")
rep("!brush&&!c.loafPet&&!W.stat.bellyTip&&", "!brush&&!W.stat.bellyTip&&")
open(P, 'w', encoding='utf-8').write(s)
print('v181 applied')
