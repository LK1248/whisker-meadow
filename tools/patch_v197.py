"""v197: tutorials don't break into petting.
- Lessons (blink, brush, pair) and hint pointers (which can lock the controls) wait until 4 s after petting,
  brushing, carrying or butt taps end. The 'pet' and 'belly' hints are about petting, so they can still show.
- When a lesson needs the camera somewhere far away, the camera first zooms out slowly, then pans across,
  then zooms in on the lesson, instead of sliding and zooming in one quick move."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count: sys.exit(f'match count {n} != {count} for: {old[:80]}')
    s = s.replace(old, new)

# --- lessons and hints wait for petting
rep("if(brushReady()&&uiGapOk())startBrushTut();", "if(brushReady()&&uiGapOk()&&!petRecent())startBrushTut();")
rep("if(pairReady()&&uiGapOk())startPairTut();", "if(pairReady()&&uiGapOk()&&!petRecent())startPairTut();")
rep("evBusy()||tips.cur||!uiGapOk())return; /* never barge into another lesson */",
    "evBusy()||tips.cur||!uiGapOk()||petRecent())return; /* never barge into another lesson, or into petting */")
rep("  for(const h of HINTS){ if(hintDone.has(h.id)||(hintRetry[h.id]&&W.time<hintRetry[h.id]))continue;",
    "  const petting=petRecent();\n"
    "  for(const h of HINTS){ if(hintDone.has(h.id)||(hintRetry[h.id]&&W.time<hintRetry[h.id]))continue; if(petting&&h.id!=='pet'&&h.id!=='belly')continue; /* don't cut into petting */")

# --- camera: far lesson targets get zoom out -> pan -> zoom in
rep("    if(key){ if(!was){ LF.want0=cam.want; LF.user0=cam.userT??-99; } LF.glide=2.5; } LF.offT=0; LF.back=false; }",
    "    if(key){ if(!was){ LF.want0=cam.want; LF.user0=cam.userT??-99; } LF.glide=2.5; } LF.offT=0; LF.back=false; LF.ph=null; }")
rep("  if(LF.glide<=0){ LF.back=false; return; } LF.glide-=dt; const f=fitFor(L[1],L[2]),",
    "  if(LF.glide<=0){ LF.back=false; LF.ph=null; return; }\n"
    "  if(L[0]!=='adoptIn'){ const f=fitFor(L[1],L[2]), far=Math.hypot(f.t.x-cam.target.x,f.t.z-cam.target.z);\n"
    "    if(LF.ph==null&&far>2.5){ LF.ph='out'; LF.outW=Math.min(LV().zoom*1.1,Math.max(cam.dist,LF.want0||0,f.d)+far*0.45); } // far away: zoom out, pan, then zoom in\n"
    "    if(LF.ph==='out'){ cam.want=lerp(cam.want,LF.outW,Math.min(1,dt*1.6)); if(cam.dist>LF.outW-0.35)LF.ph='pan'; return; }\n"
    "    if(LF.ph==='pan'){ const st=Math.min(far,Math.max(dt*1.2,far*(1-Math.exp(-dt*1.6)))); cam.target.x+=(f.t.x-cam.target.x)/(far||1)*st; cam.target.z+=(f.t.z-cam.target.z)/(far||1)*st; if(far<0.4){ LF.ph='in'; LF.glide=Math.max(LF.glide,2); } return; } }\n"
    "  LF.glide-=dt; const f=fitFor(L[1],L[2]),")
rep("  cam.target.lerp(f.t,k); if(!['blink','brush'].includes(L[0])||cam.want>f.d)cam.want=lerp(cam.want,f.d,k); }",
    "  cam.target.lerp(f.t,k); if(!['blink','brush'].includes(L[0])||cam.want>f.d)cam.want=lerp(cam.want,f.d,LF.ph==='in'?Math.min(1,dt*1.3):k); }")
# the lessons' own per-frame framing waits while the camera zooms out and pans
rep("function lessonFrame(dt){", "function camFree(){ return LF.ph!=='out'&&LF.ph!=='pan'; } // false while a lesson's zoom-out / pan is running\nfunction lessonFrame(dt){")
rep("const p=c.g.position; if(!camUser())cam.target.lerp(new V3(p.x,0.4,p.z),Math.min(1,dt*3));", "const p=c.g.position; if(!camUser()&&camFree())cam.target.lerp(new V3(p.x,0.4,p.z),Math.min(1,dt*3));", 2)
rep("if(!camUser())cam.target.lerp(new V3(mid.x,0.4,mid.z),Math.min(1,dt*2.5));", "if(!camUser()&&camFree())cam.target.lerp(new V3(mid.x,0.4,mid.z),Math.min(1,dt*2.5));")
open(P, 'w', encoding='utf-8').write(s)
print('v197 applied')
