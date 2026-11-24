"""v116: cats don't tip (they're strays: they give love, not money). The donation jar by the gate is back: visitors
leave donations every 25s, and the gift grows with how well the cats are looked after (love, health, coat, fullness;
fleas lower it). A cared-for meadow gets about what v115 paid, a neglected one very little. No text note."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    if s.count(old) != count: sys.exit(f'match count {s.count(old)} != {count} for: {old[:80]}')
    s = s.replace(old, new)
rep("donT-=dt; if(donT<=0){ donT=1; let got=0; for(const c of active()){ if(c.outside||c.carried||c.leaving)continue; c.tipT=(c.tipT??rand(8,25))-1; if(c.tipT>0)continue; c.tipT=rand(22,28);\n"
    "    const s=c.s, care=clamp(((s.aff+s.health+s.groom+s.full)/4-(c.fleas?15:0)-45)/40,0,1), amt=Math.round(2.2*care*(1+W.stars*0.2)); if(amt<=0)continue;\n"
    "    W.money+=amt; W.earned+=amt; W.stat.tips=(W.stat.tips||0)+amt; got+=amt; floatWorld(c.g.position.clone().setY(1.25*c.g.scale.x+0.2),'+$'+amt); }\n"
    "  if(got){ hud(); if(!W.stat.tipNote&&W.started&&!tutLock()){ W.stat.tipNote=1; toast('Happy, groomed, well-fed cats leave tips','badge',4200); } } }",
    "donT-=dt; if(donT<=0){ donT=25; /* visitors' donations grow with how well the cats are looked after */ let amt=0; for(const c of active()){ if(c.outside||c.leaving)continue; const s=c.s; amt+=2.2*clamp(((s.aff+s.health+s.groom+s.full)/4-(c.fleas?15:0)-45)/40,0,1); }\n"
    "  amt=Math.round(amt*(1+W.stars*0.2)); if(amt>0){ W.money+=amt; W.earned+=amt; if(W.jarPos)floatWorld(W.jarPos.clone().setY(1.2),'+$'+amt); hud(); } }")
rep("2) Tips: the donation jar is replaced by each cat leaving small tips", "2) (reverted in v116) Tips: the donation jar is replaced by each cat leaving small tips", 0) if False else None
open(P, 'w', encoding='utf-8').write(s); print('ok')
