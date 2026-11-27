"""v180: a sleeping cat woken by petting stays lying in its loaf for the whole petting session: eyes open, head up,
purring, no turning on the spot or rolling over for a belly rub (and still on its bed if it was in one). It gets up once the petting ends.
(Cats loafing under a rain roof or on a perch already kept their pose.)"""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count: sys.exit(f'match count {n} != {count} for: {old[:80]}')
    s = s.replace(old, new)

rep("if(c.state==='sleep'){ setState(c,'pet'); c.slowBlink=1.9;",
    "if(c.state==='sleep'){ const ly=c.useItem&&c.useItem.kind==='bed'?0.08:0; setState(c,'pet'); c.loafPet={y:ly}; c.slowBlink=1.9;", 2)
rep("function setState(c,st,dur=0){\n", "function setState(c,st,dur=0){\n  if(st!=='pet')c.loafPet=null; // petting a cat woken from sleep keeps it in its loaf\n")
rep("coreY=0.46-0.04*j; }\n",
    "coreY=0.46-0.04*j;\n"
    "    if(c.loafPet){ coreY=0.3; rx=0; rz*=0.3; legA=[1.3,1.3,-1.3,-1.3]; tailUp=-0.9+0.3*j; swish=0.08; swSpd=2.2; baseY=c.loafPet.y; hx=Math.max(hx,-0.1); } }\n")
rep("case 'pet': c.petT-=dt; if(c.petT>2)c.sessT=(c.sessT||0)+dt; if(c.turnTo!==undefined){",
    "case 'pet': c.petT-=dt; if(c.petT>2)c.sessT=(c.sessT||0)+dt; if(c.turnTo!==undefined&&!c.loafPet){")
# a cat petted in its loaf doesn't roll over for a belly rub mid-session
rep("r<0.28&&s.aff>=35&&c.state==='pet'&&!lessonOn()&&W.stat.bellyTip", "r<0.28&&s.aff>=35&&c.state==='pet'&&!c.loafPet&&!lessonOn()&&W.stat.bellyTip")
rep("!brush&&!W.stat.bellyTip&&(W.stat.good||0)>=10&&", "!brush&&!c.loafPet&&!W.stat.bellyTip&&(W.stat.good||0)>=10&&")
open(P, 'w', encoding='utf-8').write(s)
print('v180 applied')
