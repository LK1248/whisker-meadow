"""v48: the adoption panel (what the family would love, Pick a cat) appears only once the family has walked
up to the gate, with the chime, instead of as soon as their car is on its way."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    if s.count(old) != count: sys.exit(f'match count {s.count(old)} != {count} for: {old[:80]}')
    s = s.replace(old, new)

rep("W.family={members,want,tries:0,t:0,name:pick(FAM_NAMES),state:'arrive',car}; Snd.chime(); renderFamily(); }",
    "W.family={members,want,tries:0,t:0,name:pick(FAM_NAMES),state:'arrive',car,atGate:false}; $('#family').hidden=true; }")
rep("  else { f.t+=dt;\n    if(f.state==='walking'&&f.cat",
    "  else { f.t+=dt;\n    if(!f.atGate&&f.state==='arrive'&&f.members.every(m=>m.g.visible&&m.route&&arrived(m))){ f.atGate=true; Snd.chime(); renderFamily(); }\n    if(f.state==='walking'&&f.cat")
open(P, 'w', encoding='utf-8').write(s); print('ok')
