"""v126: the feather wand is gone. The laser (a $25 shop buy) is the one play toy: no wand button, no wand lesson or
hints, no wand upgrades. The 'Wand pounces' goal becomes 'Laser pounces' (opens once the laser is bought).
The old wand code stays dormant (unreachable) so old saves with tool 'wand' just load on the hand."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    if s.count(old) != count: sys.exit(f'match count {s.count(old)} != {count} for: {old[:80]}')
    s = s.replace(old, new)
rep('  <button class="tool" data-tool="wand" aria-label="Feather wand"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M3 21L14 6"/><path d="M14 6c3-3 6-3 7-2-1 3-3 6-7 6" fill="currentColor"/><path d="M14 6c-1 3 0 6 2 7"/></svg>Wand</button>\n', '')
rep("function wandForce(){ if(!curHint||!W.started)return null;", "function wandForce(){ return null; if(!curHint||!W.started)return null;")
rep("  {id:'wand',when:()=>W.time>100,el:'[data-tool=wand]',g:'tap',label:()=>toolIco('wand'),done:()=>W.tool==='wand'},\n", "")
rep("  {id:'wand2',when:()=>W.tool==='wand',at:()=>wand.tip.clone().setY(0.2),g:'stroke',label:()=>toolIco('wand')+H_SWAY,done:()=>(W.stat.wandPounces||0)>=3},\n", "")
rep("const k={'1':'hand','2':'brush','3':'wand','4':'laser'}[e.key];", "const k={'1':'hand','2':'brush','3':'laser'}[e.key];")
rep("if(!['hand','brush','wand','laser'].includes(W.tool))W.tool='hand';", "if(!['hand','brush','laser'].includes(W.tool)||(W.tool==='laser'&&!W.laser))W.tool='hand';")
rep("const kinds=Object.keys(TIERS).filter(k=>k==='wand'||(k==='laser'?W.laser:countItems(k)>0))", "const kinds=Object.keys(TIERS).filter(k=>k!=='wand'&&(k==='laser'?W.laser:countItems(k)>0))")
rep("['herd','Herding Cats','Cats led together with the wand or laser',", "['herd','Herding Cats','Cats led together with the laser',")
rep("['Wand pounces',()=>W.stat.wandPounces||0,10]", "['Laser pounces',()=>W.stat.laserP||0,10]")
rep("5:()=>hintDone.has('wand')||(W.stat.wandPounces||0)>0,", "5:()=>!!W.laser,")
rep("<li><b>Wand</b>: drag to move, flick to toss, tap to make it jump, hold still to raise it so cats leap.</li><li><b>Laser</b> (shop): cats sprint and pounce.",
    "<li><b>Laser</b> (shop): drag the dot and cats sprint and pounce.")
open(P, 'w', encoding='utf-8').write(s); print('ok')
