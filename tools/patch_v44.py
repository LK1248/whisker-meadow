"""v44: brushing is speed controlled.
- Brush speed is measured like hand petting (path length over the last half second).
- The speed limit is looser than petting (about 1.4x for a cat with Love ~70) and scales with Love:
  a low-Love cat (a fresh, dirty rescue) only tolerates very slow brushing, so it usually needs some petting first.
- Too fast: hourglass warnings, scrubbing stops counting, the cat flattens its ears and meows crossly, and if you keep
  going it runs off (Love 50+) or hisses and scratches."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    if s.count(old) != count: sys.exit(f'match count {s.count(old)} != {count} for: {old[:80]}')
    s = s.replace(old, new)

# measure brush speed with the same windowed path as the hand
rep("  if(W.tool==='hand'){ const sm=S.samp||(S.samp=[]);", "  if(W.tool==='hand'||W.tool==='brush'){ const sm=S.samp||(S.samp=[]);")

rep("""  if(zone==='tail'){ c.flick=0.4; return; }
  c.scrub=(c.scrub||0)+len;""", """  if(zone==='tail'){ c.flick=0.4; return; }
  // speed: looser than petting, and it grows with Love (a wary rescue only puts up with very slow brushing)
  { const D=2.5*Math.max(60,Math.min(400,catScreenH(c))), loveF=br.c===c?Math.max(1,clamp((c.s.trust-10)/60,0.4,1.3)):clamp((c.s.trust-10)/60,0.4,1.3), vMax=D*0.7*1.4*loveF*(c.trait==='shy'?0.87:1), v=S.v||0, now=W.time, hy=P.hy-(P.type==='mouse'?62:112);
    if(v>vMax*2.2){ const hard=v>vMax*4.5; c.over+=len/D*(hard?1.2:0.5);
      if(now>(c.hgT||0)){ c.hgT=now+(hard?0.9:1.1); floatHourglass(P.hx,hy,hard); slowNag.n++; if(slowNag.n>=4&&now>slowNag.next){ slowNag.n=0; slowNag.next=now+40; showSlow(); } }
      if(c.over>=1.5&&now>(c.grumbleT||0)){ c.grumbleT=now+2.5; showIcon(c,'angry',1.4); c.earFlat=1; Snd.meow(0.78,0.9); }
      return; } }
  c.scrub=(c.scrub||0)+len;""")

# when brushing pushes a cat too far, it complains out loud before leaving
rep("  if(s.trust>=50){ showIcon(c,'huff',1.5); s.aff=Math.max(0,s.aff-1); walkAway(c,Math.random()<0.5); }",
    "  if(s.trust>=50){ showIcon(c,'huff',1.5); if(W.tool==='brush')Snd.meow(0.75,1); s.aff=Math.max(0,s.aff-1); walkAway(c,Math.random()<0.5); }")

rep("<li><b>Brush</b>: scrub back and forth to clean the coat.", "<li><b>Brush</b>: scrub back and forth, gently, to clean the coat. Too fast and the cat grumbles, then leaves or scratches. Cats that don't love you yet only tolerate very slow brushing, so pet a new rescue first.")
open(P, 'w', encoding='utf-8').write(s); print('ok')
