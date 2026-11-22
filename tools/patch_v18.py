"""v18: grooming you can see. Scruffy cats carry burrs; brushing is a free scrub that pops them off; clean coats shine;
brushing is coat care (love comes from petting); a wordless burr hint; shiny coats impress fair judges."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()

def rep(old, new, count=1):
    global s
    if s.count(old) != count:
        sys.exit(f'match count {s.count(old)} != {count} for: {old[:80]}')
    s = s.replace(old, new)

# ---- burrs on the coat + shine ----
rep("function beginStroke(c,now){", r"""const BURR_SVG='<svg viewBox="0 0 32 32" width="30" height="30"><path d="M20 9q6-6 10-3-2 6-9 6z" fill="#7fa54a"/><g stroke="#6b5326" stroke-width="2.4" stroke-linecap="round"><path d="M16 6v20M6 16h20M9 9l14 14M23 9L9 23"/></g><circle cx="16" cy="16" r="6.5" fill="#8f7436"/></svg>';
function burrCount(c){ const g=c.s.groom; return g>=55?0:Math.min(6,Math.ceil((55-g)/8)); }
function ensureBurrs(c){ if(c.burrs)return; const B=BREEDS[c.coat.base], L=B?B.len:1, ax=[0.36,0.33,0.58];
  const dirs=[[0.55,0.75,0.2],[-0.5,0.8,-0.25],[0.85,0.25,-0.45],[-0.85,0.3,0.35],[0.15,0.9,-0.6],[-0.2,0.85,0.55]];
  c.burrs=dirs.map(dir=>{ const d=new V3(...dir).normalize(), t=1/Math.sqrt((d.x/ax[0])**2+(d.y/ax[1])**2+(d.z/ax[2])**2), p=d.clone().multiplyScalar(t);
    const g=new THREE.Group(); g.position.set(p.x,p.y,p.z*L); g.scale.setScalar(1.3);
    const ball=new THREE.Mesh(G.sphLo,M(0x8f7436)); ball.scale.setScalar(0.055); g.add(ball);
    for(let i=0;i<5;i++){ const sp=new THREE.Mesh(G.cone,M(0x6b5326)); sp.scale.set(0.014,0.05,0.014); const a=i*1.26; sp.position.set(Math.cos(a)*0.05,0.02,Math.sin(a)*0.05); sp.rotation.set(Math.sin(a)*1.2,0,-Math.cos(a)*1.2); g.add(sp); }
    const leaf=new THREE.Mesh(G.sph,M(0x7fa54a)); leaf.scale.set(0.06,0.012,0.03); leaf.position.set(0.05,0.04,0); leaf.rotation.z=0.5; g.add(leaf);
    g.traverse(o=>{ if(o.isMesh)o.userData={cat:c,zone:'back'}; }); g.visible=false; c.core.add(g); return g; }); c.burrN=0; }
function updateCoats(dt){ for(const c of W.cats){ if(c.away>0||!c.core)continue; ensureBurrs(c); const n=burrCount(c);
  if(n!==c.burrN){ c.burrs.forEach((b,i)=>b.visible=i<n); c.burrN=n; }
  if(c.s.groom>=85&&c.g.visible&&!c.outside){ c.shineT=(c.shineT||rand(0,2))-dt; if(c.shineT<=0){ c.shineT=rand(1.6,3); spawnFx('spark',c.g.position.clone().setY(0.75*c.g.scale.y),1,0.3,0.12); } } } }
// brushing: scrub back and forth anywhere on the coat; every bit of scrubbing pops off a burr. No rhythm to hit.
function brushScrub(c,len,zone){
  if(c.state==='hiding'){ foundCat(c); return; }
  if(c.away>0||c.carried||c.leaveT>0||c.outside||c.leaving||['boop','path','greet','bye','flop'].includes(c.state))return;
  c.petT=3; tagFor(c,3); if(!['sleep','pet','eat','litter','perch','shelter'].includes(c.state))setState(c,'pet');
  if(zone==='tail'){ c.flick=0.4; return; }
  c.scrub=(c.scrub||0)+len; if(c.scrub<160)return; c.scrub=0; c.lastStroke=W.time;
  const s=c.s, top=c.g.position.clone().setY(0.8*c.g.scale.y), before=burrCount(c);
  if(s.groom>=97){ spawnFx('spark',top,1,0.3,0.12); return; }
  s.groom=Math.min(100,s.groom+7); s.aff=Math.min(100,s.aff+0.3); W.stat.brush++; c.purr=Math.max(c.purr,0.2); c.lean=0.5;
  spawnFx('spark',top,1,0.3,0.14);
  if(burrCount(c)<before){ const b=c.burrs&&c.burrs[before-1]; if(b){ const wp=b.getWorldPosition(new V3()); spawnFx('spark',wp,4,0.12,0.12); b.visible=false; c.burrN=before-1; }
    if(Snd.ac){ const t=Snd.ac.currentTime; Snd.note(980,t,0.07,0.05,'square'); Snd.note(1480,t+0.04,0.05,0.06,'triangle'); } }
  if(before>0&&s.groom>=55&&s.groom-7<55){ spawnFx('spark',top,10,0.45,0.16); Snd.chime(); unlock&&unlock('first_brush'); } }
function beginStroke(c,now){""")
rep("""  if(S.dir&&S.len>=40&&ux*S.dir[0]+uy*S.dir[1]<-0.3){ finishStroke(); beginStroke(h.cat,now); }
  S.len+=len; S.zones[h.zone]=(S.zones[h.zone]||0)+len; S.last=now;""", """  if(W.tool==='brush'){ S.len+=len; S.last=now; brushScrub(S.cat,len,h.zone); return; }
  if(S.dir&&S.len>=40&&ux*S.dir[0]+uy*S.dir[1]<-0.3){ finishStroke(); beginStroke(h.cat,now); }
  S.len+=len; S.zones[h.zone]=(S.zones[h.zone]||0)+len; S.last=now;""")
rep("function finishStroke(){ if(S.cat&&S.len>=40){", "function finishStroke(){ if(S.cat&&S.len>=40&&W.tool!=='brush'){")
# the beat ring is for petting only
rep("if(!c||!(W.tool==='hand'||W.tool==='brush')||c.carried", "if(!c||W.tool!=='hand'||c.carried")
rep("  updateFirstAdopt(dt); updateIntro(dt);", "  updateFirstAdopt(dt); updateCoats(dt); updateIntro(dt);")

# ---- hints: wordless burr nudge ----
lab_old = "hintEl.querySelector('.lab').textContent=typeof h.label==='function'?h.label():h.label;"
rep(lab_old, "{ const L=typeof h.label==='function'?h.label():h.label, lb=hintEl.querySelector('.lab'); if(L.startsWith('<'))lb.innerHTML=L; else lb.textContent=L; }")
i = s.index("  {id:'brush',when:"); j = s.index("\n", s.index("  {id:'brush2',when:")); 
s = s[:i] + """  {id:'brush',when:()=>W.time>100&&W.tool!=='brush'&&!!scruffiest(),el:'[data-tool=brush]',g:'tap',label:()=>BURR_SVG,done:()=>W.tool==='brush'},
  {id:'brush2',when:()=>W.tool==='brush'&&!!scruffiest(),at:()=>{ const c=scruffiest(); return c&&bodyOf(c); },g:'stroke',label:()=>BURR_SVG+'<span style="font-size:24px;vertical-align:8px"> ⇆</span>',done:()=>W.stat.brush>=4},""" + s[j:]
rep("const HINTS=[", "function scruffiest(){ return active().filter(c=>burrCount(c)>0&&!c.carried&&!c.outside).sort((a,b)=>a.s.groom-b.s.groom)[0]||null; }\nconst HINTS=[")

# ---- fair: shiny coats impress, burrs cost points; photo sparkles ----
rep("  cats.sort((a,b)=>b[1]-a[1]); const cat=cats[0][0], val=cats[0][1];\n  const score=val*0.8+rand(0,28)-W.showTier*4;",
    "  cats.sort((a,b)=>b[1]-a[1]); const cat=cats[0][0], val=cats[0][1], shiny=s.groom>=85, scruffy=burrCount(c)>0;\n  const score=val*0.8+rand(0,28)-W.showTier*4+(shiny?10:scruffy?-8:0);")
rep("""openModal(`<div class="${shot?'fairpic':'center'}">${shot?`<img src="${shot}" alt="">`:''}""",
    """openModal(`<div class="${shot?'fairpic':'center'}">${shot?`<img src="${shot}" alt="">`:''}${shot&&shiny?'<div class="shine"><i></i><i></i><i></i><i></i><i></i></div>':''}""")
rep(".fairpic .fb{", """.fairpic .shine i{position:absolute;width:26px;height:26px;background:#fff6b0;clip-path:polygon(50% 0,61% 39%,100% 50%,61% 61%,50% 100%,39% 61%,0 50%,39% 39%);animation:twk 1.6s ease-in-out infinite;filter:drop-shadow(0 0 4px #fff)}
.fairpic .shine i:nth-child(1){left:38%;top:22%}.fairpic .shine i:nth-child(2){left:58%;top:34%;animation-delay:.4s;transform:scale(.7)}.fairpic .shine i:nth-child(3){left:44%;top:52%;animation-delay:.8s}.fairpic .shine i:nth-child(4){left:64%;top:18%;animation-delay:1.1s}.fairpic .shine i:nth-child(5){left:30%;top:42%;animation-delay:.6s}
@keyframes twk{0%,100%{opacity:0;transform:scale(.3) rotate(0)}50%{opacity:1;transform:scale(1) rotate(45deg)}}
.fairpic .fb{""")
rep("<li><b>Brush</b>: grooms the coat (fair judges notice). Cats also groom themselves a little when happy and fed.</li>",
    "<li><b>Brush</b>: scrub back and forth to clean the coat. Scruffy cats have burrs stuck in their fur; brushing pops them off, and a clean coat shines. Love and trust come from petting; brushing is coat care (it helps health, and fair judges love a shiny coat). Cats also groom themselves a little when happy and fed.</li>")
rep("window.__wm={animateCat,", "window.__wm={animateCat,burrCount,brushScrub,scruffiest,")
rep("let gOp=0; if(c.petT>0&&handOn(c)&&!c.carried)", "let gOp=0; if(c.petT>0&&handOn(c)&&!c.carried&&W.tool!=='brush')")
open(P, 'w', encoding='utf-8').write(s)
print('ok')
# (applied after: no rhythm glow while brushing)
