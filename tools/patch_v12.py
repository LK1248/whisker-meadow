"""v12: ease into the first pet lesson (longer pause, slow glide, overlay fades in, hand and hearts appear last)."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()

def rep(old, new, count=1):
    global s
    if s.count(old) != count:
        sys.exit(f'match count {s.count(old)} != {count} for: {old[:80]}')
    s = s.replace(old, new)

# let the meadow breathe for a moment before the lesson starts
rep("if((W.stat.good||0)<3)setTimeout(startIntro,700); }", "if((W.stat.good||0)<3)setTimeout(()=>{ if(W.started&&!W.paused)startIntro(); },2200); }")
# start from the current view; zoom happens gradually in updateIntro; overlay starts transparent and fades in
rep("Object.assign(intro,{c,t:0,g0:W.stat.good,want:cam.want});", "Object.assign(intro,{c,t:0,g0:W.stat.good,want:cam.want,w0:cam.want});")
rep("c.heading=cam.theta+Math.PI/2; } cam.want=3.5; hintDone.add('pet');", "c.heading=cam.theta+Math.PI/2; } hintDone.add('pet');")
rep("""document.body.classList.add('intro'); for(const id of ['#intro','#ghost','#pips','#introSkip'])$(id).hidden=false; $('#intro').classList.remove('off');
  $('#ghost').innerHTML""", """document.body.classList.add('intro'); for(const id of ['#intro','#ghost','#pips','#introSkip'])$(id).hidden=false; { const io=$('#intro'); io.classList.add('off','slow'); void io.offsetWidth; io.classList.remove('off'); }
  $('#pips').style.opacity=0; $('#introSkip').style.opacity=0; $('#ghost').innerHTML""")
rep("#intro.off{opacity:0}", "#intro.off{opacity:0}#intro.slow{transition:opacity 2s}#pips,#introSkip{transition:opacity .8s}")
# slow glide: ease the zoom and pan over ~2.6s, then show hearts and hand
rep("""intro.t+=dt;
  const p=c.g.position; cam.target.lerp(new V3(p.x,0.4,p.z),Math.min(1,dt*3));""", """intro.t+=dt;
  const p=c.g.position, ek=clamp(intro.t/2.6,0,1), ee=ek*ek*(3-2*ek); cam.want=lerp(intro.w0,3.5,ee); cam.target.lerp(new V3(p.x,0.4,p.z),Math.min(1,dt*(0.6+2.4*ee)));
  if(intro.t>2.2){ $('#pips').style.opacity=''; $('#introSkip').style.opacity=''; } if(intro.t>3.5)$('#intro').classList.remove('slow');""")
# the hand only appears once the camera has arrived; its stroke cycle starts then
rep("const cyc=intro.t%2.8,", "const ht=intro.t-2.8, cyc=Math.max(0,ht)%2.8,")
rep("gh.style.opacity=(handOn(c)||(P.mode&&P.mode!=='none'))?0:", "gh.style.opacity=(ht<0||handOn(c)||(P.mode&&P.mode!=='none'))?0:")
# endIntro clears the inline opacities
rep("function endIntro(){ const c=intro.c; if(!c)return; intro.c=null;", "function endIntro(){ const c=intro.c; if(!c)return; intro.c=null; $('#pips').style.opacity=''; $('#introSkip').style.opacity=''; $('#intro').classList.remove('slow');")
open(P, 'w', encoding='utf-8').write(s)
print('ok')
