"""v36: show-ready coat. A groomed cat (groom >= 85) gets a glossy highlight that sweeps along its back; crossing 85 while brushing
gets a star and a sparkle burst so it's clear the cat is fair-worthy."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    if s.count(old) != count: sys.exit(f'match count {s.count(old)} != {count} for: {old[:80]}')
    s = s.replace(old, new)

rep("function updateCoats(dt){ for(const c of W.cats){ if(c.away>0||!c.core)continue; ensureBurrs(c); const n=burrCount(c);",
"""// a thin shell over the body; a bright band of light glides head-to-tail across the top, like a glint on a polished coat
const SHEEN_VS='varying vec3 vP; varying vec3 vN; void main(){ vP=position; vN=normal; gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.0); }';
const SHEEN_FS='uniform float u; uniform float a; uniform float g; varying vec3 vP; varying vec3 vN; void main(){ float b=exp(-pow((vP.z-u)/0.3,2.0)); float top=clamp(vN.y*1.6+0.15,0.0,1.0); gl_FragColor=vec4(1.0,0.96,0.84,(b*a+g*top)*top); }';
function sheenOf(c){ if(c.sheen)return c.sheen; const m=new THREE.ShaderMaterial({uniforms:{u:{value:2},a:{value:0},g:{value:0.14}},vertexShader:SHEEN_VS,fragmentShader:SHEEN_FS,transparent:true,depthWrite:false,blending:THREE.AdditiveBlending});
  const sh=new THREE.Mesh(G.sph,m); sh.scale.setScalar(1.045); sh.raycast=()=>{}; sh.renderOrder=2; c.bodyM.add(sh); c.sheen=sh; c.sheenT=rand(0,2); return sh; }
function updateSheen(c,dt){ const on=c.s.groom>=85&&c.g.visible&&!c.outside;
  if(!on){ if(c.sheen)c.sheen.visible=false; return; } const sh=sheenOf(c); sh.visible=true;
  c.sheenT-=dt; const dur=0.95; if(c.sheenT<=-dur)c.sheenT=rand(1.4,2.6); const q=c.sheenT<0?-c.sheenT/dur:-1;
  sh.material.uniforms.u.value=q<0?2:1.25-2.5*q; sh.material.uniforms.a.value=q<0?0:(0.8+0.5*(c.s.groom-85)/15)*Math.sin(q*Math.PI); sh.material.uniforms.g.value=0.1+0.08*(c.s.groom-85)/15; }
function updateCoats(dt){ for(const c of W.cats){ if(c.away>0||!c.core)continue; ensureBurrs(c); updateSheen(c,dt); const n=burrCount(c);""")

rep("  s.groom=Math.min(100,s.groom+7); s.aff=Math.min(100,s.aff+0.3); W.stat.brush++;",
"""  const g0=s.groom; s.groom=Math.min(100,s.groom+7); s.aff=Math.min(100,s.aff+0.3); W.stat.brush++;
  if(g0<85&&s.groom>=85){ spawnFx('spark',top,14,0.6,0.2); showIcon(c,'star',2.4); Snd.chime(); c.sheenT=0; }""")
open(P, 'w', encoding='utf-8').write(s); print('ok')
