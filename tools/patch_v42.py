"""v42: burrs are gone. A neglected coat now has one gentle "scruffy" tier, then fleas.
- Groom under 35: the coat goes dull (white fur turns a patchy, yellowish off-white), bed-head tufts on the head and back,
  muddy socks, a leaf caught by the ear and a twig in the back fur, and little dust puffs when the cat shakes, sits down
  or gets brushed. Brushing knocks off the leaf and twig; once Groom is back to 35 the coat is clean again.
- Groom under 20: fleas can appear (unchanged)."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    if s.count(old) != count: sys.exit(f'match count {s.count(old)} != {count} for: {old[:80]}')
    s = s.replace(old, new)

# ---- replace the burr builder with the scruffy look ----
i0 = s.index("function burrCount(c){"); i1 = s.index("// a thin shell over the body;")
s = s[:i0] + r"""// a scruffy coat: one tier below SCRUFF_AT. burrCount = how much brushing is still needed (the brush tutorial and fair use it)
const SCRUFF_AT=35, DULL_ZONES=['back','belly','chest','head','cheek','chin','leg','tail'], PINKS=[0xf4a0a8,0xf6b7c0];
function burrCount(c){ const g=c.s.groom; return g>=SCRUFF_AT?0:Math.min(5,Math.ceil((SCRUFF_AT-g)/7)); }
const isWhite=col=>Math.min(col.r,col.g,col.b)>0.88;
function dullHex(m){ const col=m.color, w=isWhite(col); return col.clone().lerp(new THREE.Color(w?0xe0cf98:0x8d8576),w?0.45:0.3).getHex(); }
function ensureBurrs(c){ if(c.scruff)return; const B=BREEDS[c.coat.base], Ln=B?B.len:1, ax=[0.36,0.33,0.58], body=c.bodyM.material.color;
  const onBody=(dir,e=ax,zl=Ln)=>{ const d=new V3(...dir).normalize(), t=1/Math.sqrt((d.x/e[0])**2+(d.y/e[1])**2+(d.z/e[2])**2); const p=d.multiplyScalar(t); p.z*=zl; return p; };
  const fur=M(new THREE.Color(dullHex(c.bodyM.material)).getHex()), parts=[], tag=(o,zone)=>{ o.traverse(m=>{ if(m.isMesh){ m.userData={cat:c,zone,scruff:1}; } }); o.visible=false; return o; };
  const head=c.head;
  // bed-head: spikes of the cat's own (dull) fur
  [[0,0.27,-0.02,0.25],[0.06,0.26,-0.05,-0.35],[-0.07,0.25,-0.04,0.5]].forEach(([x,y,z,r])=>{ const m=new THREE.Mesh(G.cone,fur); m.position.set(x,y,z); m.scale.set(0.035,0.11,0.035); m.rotation.set(-0.3,0,r); head.add(m); parts.push(tag(m,'head')); });
  [[0.4,0.92,-0.2],[-0.35,0.93,0.15],[0.1,0.98,-0.45]].forEach(d=>{ const p=onBody(d), g=new THREE.Group(); g.position.copy(p); g.lookAt(p.clone().multiplyScalar(2)); g.rotateX(Math.PI/2);
    [[-0.025,0.3],[0.025,-0.3]].forEach(([x,r])=>{ const m=new THREE.Mesh(G.cone,fur); m.position.set(x,0.04,0); m.scale.set(0.03,0.085,0.03); m.rotation.z=r; g.add(m); }); c.core.add(g); parts.push(tag(g,'back')); });
  // muddy socks
  const mud=M(0x8a6a48), mud2=M(0x9c7d58); c.legs.forEach(L=>{ const shin=L.children[0], paw=L.children[1];
    const sl=new THREE.Mesh(shin.geometry,mud2); sl.position.set(0,-0.235,0); sl.scale.set(shin.scale.x*1.06,shin.scale.y*0.32,shin.scale.z*1.06); L.add(sl); parts.push(tag(sl,'leg'));
    const pw=new THREE.Mesh(paw.geometry,mud); pw.position.copy(paw.position); pw.scale.copy(paw.scale).multiplyScalar(1.04); L.add(pw); parts.push(tag(pw,'leg')); });
  // white fur yellows in patches
  if(isWhite(body)){ [[0.8,0.55,0.15,0.085],[0.75,0.35,-0.55,0.07],[-0.6,0.5,-0.5,0.08],[0.2,0.85,-0.75,0.065],[-0.8,0.1,0.4,0.075],[0.5,0.85,0.35,0.06]].forEach(([x,y,z,r])=>{ const p=onBody([x,y,z]), n=p.clone().normalize();
      const m=new THREE.Mesh(G.sph,M(0xd9c483)); m.position.copy(p).addScaledVector(n,-r*0.5); m.scale.setScalar(r); m.scale.y*=0.8; c.core.add(m); parts.push(tag(m,'back')); });
    const hp=onBody([-0.5,0.7,0.3],[0.3,0.27,0.27],1), m=new THREE.Mesh(G.sph,M(0xd9c483)); m.position.copy(hp).addScaledVector(hp.clone().normalize(),-0.035); m.scale.setScalar(0.065); head.add(m); parts.push(tag(m,'head')); }
  // a leaf caught by the ear, a twig in the back fur (brushing knocks these off first)
  const leaf=new THREE.Group(); leaf.position.set(0.2,0.2,-0.02); leaf.rotation.set(0.3,-0.4,-0.7); leaf.scale.setScalar(1.25); head.add(leaf);
  { const a=new THREE.Mesh(G.sph,M(0xd9a23a)); a.scale.set(0.085,0.012,0.045); leaf.add(a); const b=new THREE.Mesh(G.cyl,M(0x8a5a2b)); b.position.x=0.1; b.scale.set(0.006,0.04,0.006); b.rotation.z=Math.PI/2; leaf.add(b); }
  const tw=new THREE.Group(); tw.position.copy(onBody([0.55,0.85,-0.35])); tw.rotation.set(0.2,0.7,0.35); c.core.add(tw);
  { const a=new THREE.Mesh(G.cyl,M(0x7a5232)); a.scale.set(0.012,0.22,0.012); a.rotation.z=Math.PI/2-0.15; tw.add(a); const b=new THREE.Mesh(G.cyl,M(0x7a5232)); b.position.set(0.05,0.03,0); b.scale.set(0.008,0.08,0.008); b.rotation.z=0.7; tw.add(b);
    const l=new THREE.Mesh(G.sph,M(0x6fa64a)); l.position.set(0.1,0.055,0); l.scale.set(0.03,0.008,0.017); l.rotation.z=0.4; tw.add(l); }
  c.scruff={parts,bits:[tag(leaf,'head'),tag(tw,'back')],on:false}; }
// swap coat materials for dull ones (and back); pink nose/ears, eyes and extras keep theirs
function setDull(c,on){ c.g.traverse(o=>{ if(!o.isMesh||o.userData.scruff||!DULL_ZONES.includes(o.userData.zone)||!o.material.isMeshToonMaterial)return;
    if(c.eyes.some(e=>e===o.parent))return;
    if(on){ if(o.userData.m0||PINKS.includes(o.material.color.getHex()))return; o.userData.m0=o.material; o.material=M(dullHex(o.material)); }
    else if(o.userData.m0){ o.material=o.userData.m0; delete o.userData.m0; } }); }
function dustPuff(c,n=5){ const p=c.g.position, sc=c.g.scale.y; spawnFx('dust',new V3(p.x,0.25*sc,p.z),n,0.32*sc,0.3*sc); }
function updateScruff(c){ const on=c.s.groom<SCRUFF_AT, S=c.scruff;
  if(on!==S.on){ S.on=on; setDull(c,on); S.parts.forEach(m=>m.visible=on); S.bits.forEach(m=>m.visible=on);
    if(!on&&W.started){ spawnFx('spark',c.g.position.clone().setY(0.8*c.g.scale.y),8,0.4,0.15); } }
  if(on&&c.g.visible&&!c.outside){ const sh=c.shake>0, st=c.state; if(sh&&!c.wasShake)dustPuff(c,6);
    else if(st!==c.scrPrev&&['sit','sleep','flop','loaf'].includes(st)&&Math.random()<0.6)dustPuff(c,4); c.wasShake=sh; c.scrPrev=st; } }
""" + s[i1:]

rep("ensureBurrs(c); updateSheen(c,dt); updateFleas(c,dt); const n=burrCount(c);\n  if(n!==c.burrN){ c.burrs.forEach((b,i)=>b.visible=i<n); c.burrN=n; }\n",
    "ensureBurrs(c); updateScruff(c); updateSheen(c,dt); updateFleas(c,dt);\n")

# ---- brushing: dust flies, the leaf and twig come off ----
rep("// brushing: scrub back and forth anywhere on the coat; every bit of scrubbing pops off a burr. No rhythm to hit.",
    "// brushing: scrub back and forth anywhere on the coat; a scruffy coat puffs dust and loses its leaf and twig. No rhythm to hit.")
rep("""  if(burrCount(c)<before){ const b=c.burrs&&c.burrs[before-1]; if(b){ const wp=b.getWorldPosition(new V3()); spawnFx('spark',wp,4,0.12,0.12); b.visible=false; c.burrN=before-1; }""",
    """  if(before>0)dustPuff(c,3);
  if(burrCount(c)<before){ const b=c.scruff&&c.scruff.bits.find(x=>x.visible); if(b){ const wp=b.getWorldPosition(new V3()); spawnFx('spark',wp,4,0.12,0.12); b.visible=false; }""")
rep("if(before>0&&s.groom>=55&&s.groom-7<55){", "if(before>0&&s.groom>=SCRUFF_AT&&s.groom-7<SCRUFF_AT){")

# ---- dust puff sprite ----
rep("    case 'itch': x.fillStyle", """    case 'dust': { const gr=x.createRadialGradient(64,64,6,64,64,58); gr.addColorStop(0,'rgba(226,208,170,0.95)'); gr.addColorStop(0.6,'rgba(214,196,156,0.6)'); gr.addColorStop(1,'rgba(214,196,156,0)'); x.fillStyle=gr;
      [[64,70,50],[42,58,30],[86,56,32]].forEach(([a,b,r])=>{ x.beginPath(); x.arc(a,b,r,0,7); x.fill(); }); break; }
    case 'itch': x.fillStyle""", 1)

# ---- help text ----
rep("Scruffy cats have burrs stuck in their fur; brushing pops them off, and a clean coat shines.",
    "A scruffy cat (Groom under 35) looks dull and dusty, with bed-head, muddy socks and bits of leaf and twig in its fur; brushing cleans it up, and a really clean coat shines.")
rep("window.__wm={Snd,", "window.__wm={Snd,ensureBurrs,updateScruff,dustPuff,")
open(P, 'w', encoding='utf-8').write(s); print('ok')
