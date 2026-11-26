"""v149:
- Star button: the count bubble now sits in front of the progress ring (the ring was painted over it).
- Laser pointer costs $100 (was $25).
- The very first meadow photo floats from the middle of the screen over to the corkboard and lands there with a
  little sparkle, so players learn where photos are kept. Later photos use the usual corner toast."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count: sys.exit(f'match count {n} != {count} for: {old[:80]}')
    s = s.replace(old, new)

rep("#bBadges .sn{position:absolute;", "#bBadges .sn{position:absolute;z-index:1;")
rep('data-tool="laser" aria-label="Laser pointer"><span class="lock">$25</span>', 'data-tool="laser" aria-label="Laser pointer"><span class="lock">$100</span>')
rep("{id:'laser',name:()=>'Laser pointer',desc:'Zoomies!',cost:()=>25,", "{id:'laser',name:()=>'Laser pointer',desc:'Zoomies!',cost:()=>100,")
rep(".toast.snap img{",
    ".snapFly{position:fixed;left:50%;top:42%;z-index:30;width:200px;margin:-80px 0 0 -106px;background:#fff;padding:6px 6px 14px;border-radius:4px;box-shadow:0 8px 24px rgba(0,0,0,.35);pointer-events:none;transform:rotate(-3deg);animation:snapIn .6s ease-out;transition:transform 1.9s cubic-bezier(.45,.05,.4,1),opacity .4s 1.6s}\n"
    ".snapFly img{display:block;width:200px;height:150px;object-fit:cover;border-radius:2px}\n"
    ".toast.snap img{")
rep("  toast(`<img src=\"${img}\" alt=\"\">`,'snap',3200); boardPop(); W.stat.snaps=",
    "  if(fresh&&SNAPS.length===1&&!(W.stat.snaps>0))snapFly(img); else { toast(`<img src=\"${img}\" alt=\"\">`,'snap',3200); boardPop(); } W.stat.snaps=")
rep("function boardPop(){",
    "// first photo ever: show it big, then float it over to the corkboard so players see where photos live\n"
    "function snapFly(img){ const d=document.createElement('div'); d.className='snapFly'; d.innerHTML=`<img src=\"${img}\" alt=\"\">`; document.body.appendChild(d);\n"
    "  if(cardBoard&&!cam.meet&&!camUser()){ const bp=cardBoard.getWorldPosition(new V3()), q=bp.clone().project(camera); if(q.z>=1||Math.abs(q.x)>0.75||Math.abs(q.y)>0.8){ cam.focus={g:{position:new V3(bp.x-0.6,0,bp.z+0.3)}}; cam.focusT=3.4; } }\n"
    "  setTimeout(()=>{ let tx=innerWidth*0.85, ty=innerHeight*0.4; if(cardBoard){ const p=cardBoard.getWorldPosition(new V3()).project(camera); if(p.z<1){ tx=(p.x+1)/2*innerWidth; ty=(1-p.y)/2*innerHeight; } }\n"
    "    tx=Math.max(24,Math.min(innerWidth-24,tx)); ty=Math.max(24,Math.min(innerHeight-24,ty)); const r=d.getBoundingClientRect(), dx=tx-(r.left+r.width/2), dy=ty-(r.top+r.height/2);\n"
    "    d.style.animation='none'; d.style.transform=`translate(${dx}px,${dy}px) rotate(6deg) scale(.12)`; d.style.opacity='0'; }, 1500);\n"
    "  setTimeout(()=>{ d.remove(); boardPop(); Snd.ding(); }, 3450); }\n"
    "function boardPop(){")
open(P, 'w', encoding='utf-8').write(s)
print('v149 applied')
