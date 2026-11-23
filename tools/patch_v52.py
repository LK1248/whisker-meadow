"""v52: the first adoption's goodbye is uninterrupted.
After the first cat is handed over, the quiet stage (no families, strays, runaways, rain, hints, tips, other cats'
icons, romps, nightfall, postcards) holds until the family has walked back and their car has driven off.
A stray that was due in that time comes a few seconds after the car is gone."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    if s.count(old) != count: sys.exit(f'match count {s.count(old)} != {count} for: {old[:80]}')
    s = s.replace(old, new)

# mark the first adoption's family, and its car once they are in it
rep("function adoptOK(c){ const f=W.family; f.state='bye';", "function adoptOK(c){ const f=W.family; if(!W.homes.length)f.first=true; f.state='bye';")
rep("function removeFamily(){ const f=W.family; if(!f)return; for(const m of f.members)scene.remove(m.g); carLeave(f.car);",
    "function removeFamily(){ const f=W.family; if(!f)return; for(const m of f.members)scene.remove(m.g); if(f.first&&f.car)f.car.first=true; carLeave(f.car);")
rep("function tutQuiet(){ return !!(W.started&&(lessonOn()||(!W.stat.brushTut&&W.time<480))); }",
    "function tutQuiet(){ return !!(W.started&&(lessonOn()||(!W.stat.brushTut&&W.time<480)||firstBye())); }\n"
    "// the first adopting family walking back to their car and driving away\n"
    "function firstBye(){ return !!((W.family&&W.family.first)||cars.some(k=>k.first)); }")
# a stray due during the goodbye waits for it
rep("strayT-=dt; if(strayT<=0){ strayT=rand(110,170);", "strayT-=dt; if(strayT<=0&&firstBye())strayT=8; if(strayT<=0){ strayT=rand(110,170);")
# postcards wait too
rep("if(W.postQ.length&&W.postQ[0].t<=W.time&&$('#modal').hidden&&!W.paused){", "if(W.postQ.length&&W.postQ[0].t<=W.time&&$('#modal').hidden&&!W.paused&&!tutQuiet()){")
# the cat going home still shows its goodbye icons
rep("function showIcon(c,kind,dur=2.5){ if(tutQuiet()&&!lessonCat(c)&&", "function showIcon(c,kind,dur=2.5){ if(tutQuiet()&&!lessonCat(c)&&!(W.family&&W.family.cats&&W.family.cats.includes(c))&&")
rep("window.__wm={Snd,", "window.__wm={Snd,firstBye,cars,pickForHome,")
open(P, 'w', encoding='utf-8').write(s); print('ok')
