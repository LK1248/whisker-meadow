"""v25: developer panel, only with ?dev in the URL: money, food, stars, max stats, skip time, expand, adopters, strays."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    if s.count(old) != count: sys.exit(f'match count {s.count(old)} != {count} for: {old[:80]}')
    s = s.replace(old, new)
rep("let dayT=40;", r"""let dayT=40;
// ---- developer panel (only with ?dev in the address) ----
if(/[?&]dev\b/.test(location.search)){ const d=document.createElement('div'); d.id='devp';
  d.style.cssText='position:fixed;left:8px;bottom:96px;z-index:50;display:flex;flex-direction:column;gap:4px;font:600 12px sans-serif';
  const B=[['+$500',()=>{ W.money+=500; }],['+50 food',()=>{ W.food+=50; }],['+1 ★',()=>{ W.stars=(W.stars||0)+1; }],
    ['Max stats',()=>{ for(const c of W.cats)Object.assign(c.s,{trust:95,aff:95,health:95,full:95,fun:95,groom:95,clean:95}); }],
    ['Skip 2 min',()=>{ W.time+=120; for(const c of W.cats)c.arrivedAt=(c.arrivedAt||0)-120; }],
    ['Family',()=>{ if(!W.family)spawnFamily(); }],['Stray',()=>{ startDropoff(); }],['Night/Day',()=>{ dayT=(dayT+DAYLEN/2)%DAYLEN; }],
    ['Expand',()=>{ if(W.level<LEVELS.length-1){ W.stars=Math.max(W.stars||0,5); expand(); } }]];
  for(const [t,f] of B){ const b=document.createElement('button'); b.textContent=t; b.style.cssText='padding:4px 8px;border-radius:8px;border:0;background:rgba(40,30,50,.75);color:#fff;text-align:left'; b.onclick=e=>{ e.stopPropagation(); f(); hud(); }; d.appendChild(b); }
  const x=document.createElement('button'); x.textContent='DEV ▾'; x.style.cssText='padding:4px 8px;border-radius:8px;border:0;background:#e0507a;color:#fff'; x.onclick=()=>{ for(const b of [...d.children].slice(1))b.hidden=!b.hidden; }; d.prepend(x);
  document.body.appendChild(d); }""")
open(P, 'w', encoding='utf-8').write(s); print('ok')
