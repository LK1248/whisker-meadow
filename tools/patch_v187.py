"""v187: thank-you notes for a pair name both cats.
"Thank you for Tumble and Truffle! They have been playing all day since they arrived."
(Pair notes without the thank-you keep "Tumble and Truffle haven't stopped playing since they got here.")"""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count: sys.exit(f'match count {n} != {count} for: {old[:80]}')
    s = s.replace(old, new)

rep("const nm=cats.map(c=>c.name), line=CARD_SCENES[scene].line(nm[0],nm[1]);\n  return {img:cv.toDataURL('image/jpeg',0.8),scene,line,thanks:first,noCard:grumpy};",
    "const nm=cats.map(c=>c.name), pair=nm.length>1, line=first&&pair?'They have been playing all day since they arrived.':CARD_SCENES[scene].line(nm[0],nm[1]);\n"
    "  return {img:cv.toDataURL('image/jpeg',0.8),scene,line,thanks:first,who:pair?nm[0]+' and '+nm[1]:null,noCard:grumpy};")
rep("scene:pc&&pc.scene,thanks:pc&&pc.thanks,", "scene:pc&&pc.scene,thanks:pc&&pc.thanks,who:pc&&pc.who,")
rep("${hm.thanks?`Thank you for ${hm.name}! `:''}", "${hm.thanks?`Thank you for ${hm.who||hm.name}! `:''}")
open(P, 'w', encoding='utf-8').write(s)
print('v187 applied')
