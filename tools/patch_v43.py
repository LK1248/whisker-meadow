"""v43:
- Shiny coat (Groom 85+): the gliding glint band is gone. The coat itself turns glossy: the toon shader gets a real
  specular highlight (a crisp toon-stepped spot plus a soft lobe) that moves with the light and camera as the cat moves.
  The sparkle twinkles are rarer.
- Owls: tap an owl to boop it; it ruffles, hoots and flies to a free tree nearby. Boop it again and it flies off for the
  night. When the next night comes, every owl is back on its home tree."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    if s.count(old) != count: sys.exit(f'match count {s.count(old)} != {count} for: {old[:80]}')
    s = s.replace(old, new)

# ---- glossy coat material ----
rep("function M(c){ return matCache[c]||(matCache[c]=new THREE.MeshToonMaterial({color:c,gradientMap:gradTex})); }",
"""function M(c){ return matCache[c]||(matCache[c]=new THREE.MeshToonMaterial({color:c,gradientMap:gradTex})); }
// glossy coat: the same toon material plus a specular highlight (a crisp stepped spot and a soft lobe around it)
const GLOSS_SPEC='reflectedLight.directDiffuse += irradiance * BRDF_Diffuse_Lambert( material.diffuseColor );';
const glossCache={};
function MG(c){ if(glossCache[c])return glossCache[c]; const m=new THREE.MeshToonMaterial({color:c,gradientMap:gradTex});
  m.onBeforeCompile=sh=>{ sh.fragmentShader=sh.fragmentShader.replace('#include <lights_toon_pars_fragment>',THREE.ShaderChunk.lights_toon_pars_fragment.replace(GLOSS_SPEC,GLOSS_SPEC+
    ' vec3 hv=normalize(directLight.direction+geometry.viewDir); float nh=max(dot(geometry.normal,hv),0.0); float sp=pow(nh,90.0); float soft=pow(nh,16.0);'+
    ' reflectedLight.directDiffuse += directLight.color*(smoothstep(0.3,0.5,sp)*0.5+soft*0.12);')); };
  m.customProgramCacheKey=()=>'gloss'; return glossCache[c]=m; }""")

# ---- coat modes: dull (scruffy) / gloss (shiny) / normal ----
i0 = s.index("function setDull(c,on){"); i1 = s.index("function dustPuff(c,")
s = s[:i0] + """function setCoat(c,mode){ c.g.traverse(o=>{ if(!o.isMesh||o.userData.scruff||!DULL_ZONES.includes(o.userData.zone))return;
    if(c.eyes.some(e=>e===o.parent))return;
    if(o.userData.m0){ o.material=o.userData.m0; delete o.userData.m0; }
    if(!mode||!o.material.isMeshToonMaterial||PINKS.includes(o.material.color.getHex()))return;
    o.userData.m0=o.material; o.material=mode==='dull'?M(dullHex(o.material)):MG(o.material.color.getHex()); }); }
""" + s[i1:]
rep("if(on!==S.on){ S.on=on; setDull(c,on); ", "if(on!==S.on){ S.on=on; ")

i0 = s.index("// a thin shell over the body;"); i1 = s.index("function updateCoats(dt){")
s = s[:i0] + """// coat look follows Groom: dull below SCRUFF_AT, glossy at 85+
function updateSheen(c){ const g=c.s.groom, mode=g<SCRUFF_AT?'dull':g>=85?'gloss':''; if(mode!==(c.coatMode||'')){ setCoat(c,mode); c.coatMode=mode; } }
""" + s[i1:]
rep("c.shineT=(c.shineT||rand(0,2))-dt; if(c.shineT<=0){ c.shineT=rand(1.6,3);", "c.shineT=(c.shineT||rand(0,4))-dt; if(c.shineT<=0){ c.shineT=rand(4,8);")

# ---- owls: boop -> nearby tree, boop again -> gone until next night ----
rep("return {g,body,head,eyes}; }", "return {g,body,head,eyes,wings:body.children.filter(m=>Math.abs(m.position.x)>0.15)}; }")
rep("const owls=[]; let owlEyeMat=null;", "const owls=[], owlTrees=[]; let owlEyeMat=null;")
rep("const trs=[]; owls.length=0;", "const trs=[]; owls.length=0; owlTrees.length=0;")
rep("trs.sort((a,b)=>a.d-b.d); const perch=", "trs.sort((a,b)=>a.d-b.d); owlTrees.push(...trs); const perch=")
rep("owls.push(Object.assign(ow,{inv:1/P0.sc,k:0,", "owls.push(Object.assign(ow,{inv:1/P0.sc,tree:P0,home:P0,boops:0,k:0,")
rep("function updateOwls(dt){ const on=(W.night||0)>0.45&&!weather.raining;\n  for(const o of owls){ o.k=clamp(o.k+(on?dt:-dt)*0.5,0,1); o.g.visible=o.k>0.01; if(!o.g.visible)continue;",
"""const PERCH_Y=2.92;
function perchOwl(o,T){ T.t.add(o.g); o.g.position.set(0,PERCH_Y,0); o.g.rotation.set(0,rand(-0.5,0.5)-T.t.rotation.y,0); o.inv=1/T.sc; o.tree=T; }
// boop: ruffle and hoot, then fly to a free tree nearby; a second boop sends it off for the night
function boopOwl(o){ if(o.fly||o.flyT>0)return; o.boops++; o.hoot=1.4; Snd.owl(0.55); { const wp=o.g.getWorldPosition(new V3()); wp.y+=0.4; spawnFx('spark',wp,4,0.25,0.14); }
  const from=o.g.getWorldPosition(new V3()); let to, away=o.boops>=2;
  if(!away){ const free=owlTrees.filter(T=>T!==o.tree&&!owls.some(x=>x.tree===T&&!x.gone)).map(T=>({T,d:dist2(T.t.position,o.tree.t.position)})).filter(x=>x.d>2).sort((a,b)=>a.d-b.d);
    if(free.length){ const T=free[Math.floor(Math.random()*Math.min(3,free.length))].T; o.dest=T; to=T.t.localToWorld(new V3(0,PERCH_Y,0)); } else away=true; }
  if(away){ const dir=from.clone().setY(0); if(dir.lengthSq()<0.01)dir.set(1,0,0); dir.normalize(); to=from.clone().addScaledVector(dir,26).setY(9); o.dest=null; }
  o.flyT=0.55; o.fly={from,to,t:0,dur:away?3.2:Math.max(1.4,from.distanceTo(to)/4.5),away}; }
function owlFlight(o,dt){ if(o.flyT>0){ o.flyT-=dt; if(o.flyT>0)return; const par=o.g.parent.parent||scene; par.attach(o.g); o.flyPar=par; o.inv=1; o.g.rotation.set(0,0,0); }
  const f=o.fly; f.t=Math.min(1,f.t+dt/f.dur); const q=f.t, p=f.from.clone().lerp(f.to,q); p.y+=Math.sin(q*Math.PI)*(f.away?1.5:1.1);
  o.g.position.copy(o.flyPar.worldToLocal(p)); o.g.rotation.y=Math.atan2(f.to.x-f.from.x,f.to.z-f.from.z); o.body.rotation.x=0.35*Math.sin(q*Math.PI);
  const fl=Math.sin(W.time*22)*0.9; o.wings.forEach((w,i)=>{ w.rotation.z=(i?-1:1)*(0.4+fl); });
  if(q>=1){ o.fly=null; o.body.rotation.x=0; o.wings.forEach(w=>w.rotation.z=0); if(f.away){ o.gone=true; o.g.visible=false; } else perchOwl(o,o.dest); } }
function updateOwls(dt){ const on=(W.night||0)>0.45&&!weather.raining;
  for(const o of owls){
    if(!on&&(o.gone||o.tree!==o.home)&&!o.fly&&!(o.flyT>0)){ o.gone=false; o.boops=0; o.k=0; perchOwl(o,o.home); }
    if(!on&&!o.fly)o.boops=0;
    if(o.gone){ o.g.visible=false; continue; }
    if(o.fly){ owlFlight(o,dt); if(o.fly||o.gone)continue; }
    o.k=clamp(o.k+(on?dt:-dt)*0.5,0,1); o.g.visible=o.k>0.01; if(!o.g.visible)continue;""")
# tap: owls (they sit high in the trees, so a generous radius)
rep("  return false; }\n// ---- the world outside the fence ----",
"""  for(const o of owls){ if(!o.g.visible||o.gone||o.fly||o.k<0.9)continue; const sc=toScreen(o.head.getWorldPosition(new V3())); if(sc.ok&&Math.hypot(sc.x-e.clientX,sc.y-e.clientY)<52){ boopOwl(o); return true; } }
  return false; }
// ---- the world outside the fence ----""")
rep("window.__wm={Snd,", "window.__wm={Snd,owls,boopOwl,owlTrees,")
open(P, 'w', encoding='utf-8').write(s); print('ok')
