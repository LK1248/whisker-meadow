"""v41: three stats are now Love, Groom and Health.
- Trust is folded into Love: s.aff is an alias of s.trust, so every old trust/affection rule now moves one Love value.
- Groom (brush icon) gates the fair (50+) and matters a little for adoption: a family turns down a cat under 30 unless Love is 90+.
- Fair place and prize scale with Groom.
- Below Groom 20 a cat can catch fleas: tiny black dots crawl on its back, it stops to scratch with a hind leg and grumbles. Brushing removes them.
- Head shake: cats now often shake their heads during and after a pond visit (on top of the random/rain shakes)."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    if s.count(old) != count: sys.exit(f'match count {s.count(old)} != {count} for: {old[:80]}')
    s = s.replace(old, new)

# ---- Love = trust + affection, one value ----
rep("W.cats.push(cat); return cat;", """{ const os=o.s||{}, st=cat.s; const love='trust' in os&&'aff' in os?Math.max(os.trust,os.aff):'trust' in os?os.trust:'aff' in os?os.aff:30;
    delete st.aff; st.trust=love; Object.defineProperty(st,'aff',{get(){ return this.trust; },set(v){ this.trust=v; },enumerable:false,configurable:true}); }
  W.cats.push(cat); return cat;""")

# ---- Groom icon replaces the trust icon in the UI ----
i0 = s.index("const ICO_T='"); i1 = s.index("';", i0) + 2
s = s[:i0] + """const ICO_T='<svg viewBox="0 0 24 24"><rect x="2.5" y="10.5" width="14" height="5" rx="2.5" fill="#b98af0"/><path d="M5 15.5v4M8 15.5v4M11 15.5v4M14 15.5v4" stroke="#7d55c7" stroke-width="1.6" stroke-linecap="round"/><path d="M15.5 12l5-6" stroke="#7d55c7" stroke-width="2.4" stroke-linecap="round"/><path d="M19 1.5l.8 1.7 1.7.8-1.7.8-.8 1.7-.8-1.7-1.7-.8 1.7-.8z" fill="#f6b800"/></svg>';""" + s[i1:]
rep('<span class="lb">Trust</span>', '<span class="lb">Groom</span>')
rep("tag.prev={a:c.s.aff,t:c.s.trust,h:c.s.health}", "tag.prev={a:c.s.aff,t:c.s.groom,h:c.s.health}")
rep("[['rA',c.s.aff],['rT',c.s.trust],['rH',c.s.health]]", "[['rA',c.s.aff],['rT',c.s.groom],['rH',c.s.health]]")
rep("[['a','aff','rA'],['t','trust','rT'],['h','health','rH']]", "[['a','aff','rA'],['t','groom','rT'],['h','health','rH']]")
rep('<i style="width:${c.s.trust}%;background:#5b9be6"></i>', '<i style="width:${c.s.groom}%;background:#b98af0"></i>')
rep("const trustIco=(x,y,w)=>ICO_T.replace(", "const trustIco=(x,y,w)=>ICO_A.replace(")
rep("['Trust',r.trust]", "['Love',r.trust]")

# ---- adoption: a very scruffy cat gets turned down unless it adores people ----
rep("f.match=c.trait===f.want||(c.s.trust>=75&&Math.random()<0.5)||Math.random()<0.15;",
    "f.match=c.trait===f.want||(c.s.trust>=75&&Math.random()<0.5)||Math.random()<0.15; f.scruffy=c.s.groom<GROOM_HOME&&c.s.trust<90; if(f.scruffy)f.match=false;")
rep("c.heading=0; showIcon(c,'huff',1.4); floatWorld(c.g.position.clone().setY(1.2),'Not quite');",
    "c.heading=0; showIcon(c,f.scruffy?'itch':'huff',1.4); floatWorld(c.g.position.clone().setY(1.2),f.scruffy?'Needs a brush':'Not quite');")

# ---- fair: needs Groom 50+, place and prize scale with Groom ----
rep("s.health>=60&&s.trust>=55&&s.aff>=50; }", "s.health>=60&&s.trust>=55&&s.groom>=GROOM_FAIR; }")
rep("const score=val*0.8+rand(0,28)-W.showTier*4+(shiny?10:scruffy?-8:0);", "const score=val*0.8+rand(0,28)-W.showTier*4+(s.groom-60)*0.35+(shiny?4:scruffy?-4:0);")
rep("const prize=[0,base*3,base*2,Math.round(base*1.3)][place];", "const prize=Math.round([0,base*3,base*2,base*1.3][place]*(0.7+0.6*s.groom/100));")

# ---- fleas ----
rep("const TIER_N=['','Bronze','Silver','Gold'];", """const TIER_N=['','Bronze','Silver','Gold'];
const GROOM_HOME=30, GROOM_FAIR=50, FLEA_AT=20, FLEA_M=new THREE.MeshBasicMaterial({color:0x161010}), FLEA_M2=new THREE.MeshBasicMaterial({color:0xc8a27a});
// fleas: tiny black dots that crawl over the back and hop now and then
function updateFleas(c,dt){ const n=c.fleas||0; if(!n&&!c.fleaG)return;
  if(!c.fleaG){ c.fleaG=[]; for(let i=0;i<8;i++){ const m=new THREE.Mesh(G.sph,c.coat.base==='black'?FLEA_M2:FLEA_M); m.raycast=()=>{}; c.bodyM.add(m); const a=rand(-2.6,2.6), b=rand(0,0.9); m.userData.d=new V3(Math.sin(a)*Math.cos(b),Math.sin(b),Math.cos(a)*Math.cos(b)); c.fleaG.push(m); } }
  const sc=c.bodyM.scale; c.fleaG.forEach((m,i)=>{ m.visible=i<n; if(!m.visible)return; const d=m.userData.d, hop=Math.random()<dt*1.5?0.35:0;
    d.x+=rand(-1,1)*(dt*0.9+hop); d.z+=rand(-1,1)*(dt*0.9+hop); d.y+=rand(-1,1)*dt*0.9; d.normalize(); if(d.y<-0.1){ d.y=-0.1; d.normalize(); }
    m.position.copy(d).multiplyScalar(1.02); m.scale.set(0.034/sc.x,0.034/sc.y,0.034/sc.z); }); }""")
rep("  s.groom=Math.max(0,s.groom-dt*0.04);\n", """  s.groom=Math.max(0,s.groom-dt*0.04);
  if(!c.fleas&&s.groom<FLEA_AT&&!c.outside&&Math.random()<dt/40)c.fleas=5+Math.floor(rand(0,4));
  if(c.fleas&&s.groom>=40)c.fleas=0;
  if(c.fleas&&!c.outside&&!c.carried){ if(['idle','walk'].includes(c.state)&&Math.random()<dt/9)setState(c,'itch',rand(1.4,2.2));
    if(Math.random()<dt/12){ showIcon(c,'itch',1.6); if(Math.random()<0.6)Snd.meow(1.05,0.5); } }
""")
rep("+(c.nourT>0?6:0); s.health=", "+(c.nourT>0?6:0)-(c.fleas?10:0); s.health=")
rep("    case 'pondwatch':", "    case 'itch': if(c.stT<=0)setState(c,'idle',1); break;\n    case 'pondwatch':")
rep("  else if(st==='groom'){ const lick=", """  else if(st==='itch'){ rx=-0.45; coreY=0.44; legA=[0.45,0.45,-2.1+Math.sin(t*34)*0.5,-1.0]; hx=0.1; hy=0.55; hz=0.5; eye=0.3; earOut=0.7; tailUp=-0.2; swish=0.3; swSpd=6; }
  else if(st==='groom'){ const lick=""")
rep("ensureBurrs(c); updateSheen(c,dt);", "ensureBurrs(c); updateSheen(c,dt); updateFleas(c,dt);")
rep("const g0=s.groom; s.groom=Math.min(100,s.groom+7);", "if(c.fleas){ c.fleas=Math.max(0,c.fleas-2); spawnFx('spark',top,3,0.25,0.12); } const g0=s.groom; s.groom=Math.min(100,s.groom+7);")
rep("    case 'star':", """    case 'itch': x.fillStyle='#2a1c18'; [[44,52],[70,40],[86,64],[58,76],[36,82]].forEach(([a,b])=>{x.beginPath();x.arc(a,b,6,0,7);x.fill();});
      x.strokeStyle='#e2574c'; x.lineWidth=5; x.lineCap='round'; x.beginPath(); x.moveTo(18,34); x.lineTo(28,24); x.moveTo(100,32); x.lineTo(110,22); x.moveTo(100,94); x.lineTo(110,104); x.stroke(); break;
    case 'star':""")

# ---- head shake around the pond ----
rep("if(c.swipeT<=0){ c.swipeT=rand(2.5,4.5);", "if(c.swipeT<=0){ c.swipeT=rand(2.5,4.5); if(Math.random()<0.3)c.shake=0.65;")
rep("c.earTw=0.3; } if(c.stT<=0)setState(c,'idle',1); break;", "c.earTw=0.3; } if(c.stT<=0){ setState(c,'idle',1); if(Math.random()<0.7)c.shake=0.65; } break;")

# ---- help text ----
rep("<li><b>Love</b> (heart): petting, playing, butt taps (for cats who like them), premium food.</li><li><b>Trust</b> (paw in hand): gentle on-beat petting, feeding, play, blinking back. Drops when you scratch the wrong spot, pet too fast, or hold a nervous cat too long. Kittens learn to trust faster.</li>",
    "<li><b>Love</b> (heart): gentle on-beat petting, playing, feeding, blinking back, butt taps (for cats who like them), premium food. Drops when you scratch the wrong spot, pet too fast, or hold a nervous cat too long. Kittens warm up faster.</li><li><b>Groom</b> (brush): a clean, shiny coat. It fades slowly; brush to bring it back. Fair judges care a lot, families a little. A very scruffy cat catches <b>fleas</b> (tiny black dots, lots of scratching and grumbling): brush them off.</li>")
rep("Love and trust come from petting; brushing is coat care (it helps health, and fair judges love a shiny coat).", "Love comes from petting; brushing raises Groom (it helps health, wins fairs and gets rid of fleas).")
rep("has trust 75+", "has Love 75+")
rep("<b>Trust 55+, Love 50+ and Health 60+</b> gets a <b>Fair!</b> button on its tag.", "<b>Love 55+, Groom 50+ and Health 60+</b> gets a <b>Fair!</b> button on its tag. The better groomed, the higher it places and the bigger the prize.")
rep("with Trust 50+ and Health 55+. Looks and ribbons don't matter.", "with Love 50+ and Health 55+. Ribbons don't matter, but a family turns down a very scruffy cat (Groom under 30) unless it adores people (Love 90+).")
rep("A cat with very low trust may slip out the gate.", "A cat with very low love may slip out the gate.")
rep("(trust goes up)", "(love goes up)")
rep("window.__wm={Snd,", "window.__wm={Snd,updateFleas,")
open(P, 'w', encoding='utf-8').write(s); print('ok')
