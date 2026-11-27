"""v195: quick one-way strokes (lift, swipe, lift) annoy a cat as much as rubbing back and forth with the finger down.
1) Stroke speed was averaged over at least 0.25 s, so a fresh 60 ms swipe read about 4x slower than it was. The floor is now 0.06 s.
2) Agitation no longer drains during a short lift (under 0.4 s) between fast strokes.
3) When a fast stroke follows a short lift, the time in the air counts as fast too (up to 0.35 s), as it does for a finger held down."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count: sys.exit(f'match count {n} != {count} for: {old[:80]}')
    s = s.replace(old, new)

rep("S.v=path/Math.max(0.25,(now-sm[0][0])/1000);", "S.v=path/Math.max(0.06,(now-sm[0][0])/1000);")
rep("if(tn-(c.fastT||0)>0.15)c.fastM=Math.max(0,(c.fastM||0)-bdt*AGI_CALM);",
    "if(tn-(c.fastT||0)>(P.mode==='stroke'?0.15:0.4))c.fastM=Math.max(0,(c.fastM||0)-bdt*AGI_CALM); /* a short lift between strokes doesn't calm it */")
rep("let gain=0; const gap=Math.min(0.12,Math.max(0,performance.now()/1000-(c.pmT||0))); c.pmT=performance.now()/1000;",
    "let gain=0; const gapRaw=Math.max(0,performance.now()/1000-(c.pmT||0)), gap=Math.min(0.12,gapRaw); c.pmT=performance.now()/1000;")
rep("c.fastM=Math.min(3.4,(c.fastM||0)+gap*(0.6+Math.min(1.5,x-tf)));",
    "const gF=(performance.now()/1000-(c.fastT||0)<0.5)?Math.min(0.35,gapRaw):gap; /* fast again right after a short lift: the lift counts too */\n"
    "    c.fastM=Math.min(3.4,(c.fastM||0)+gF*(0.6+Math.min(1.5,x-tf)));")
rep("if(c.fastM>2.6&&!(W.time<180&&x<tf+1.5))c.over+=gap*2.6; }", "if(c.fastM>2.6&&!(W.time<180&&x<tf+1.5))c.over+=gF*2.6; }")
open(P, 'w', encoding='utf-8').write(s)
print('v195 applied')
