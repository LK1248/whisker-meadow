"""v93: a runaway's meows swell once it has settled in its hiding spot: they start at an ordinary meow's volume and
grow over about a minute to ~2.3x as loud (only gently quieter when the camera is far away), so it's easy to notice."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    if s.count(old) != count: sys.exit(f'match count {s.count(old)} != {count} for: {old[:80]}')
    s = s.replace(old, new)
rep("if(c.state==='hiding'){ R.meowT=(R.meowT||0)-dt; if(R.meowT<=0){ const urgency=Math.min(1,R.t/120);",
    "if(c.state==='hiding'){ R.hideT=(R.hideT||0)+dt; R.meowT=(R.meowT||0)-dt; if(R.meowT<=0){ const urgency=Math.min(1,R.t/120), swell=Math.min(1,R.hideT/RUN_SWELL);")
rep("const vol=clamp(1-d/18,0.06,1)*(0.7+1.1*urgency); Snd.meow(1.2-0.15*urgency,vol);",
    "const vol=clamp(1-d/40,0.6,1)*RUN_MEOW0*(1+(RUN_PEAK-1)*swell); Snd.meow(1.2-0.15*urgency,vol);")
rep("const mice=[];", "let RUN_MEOW0=0.3, RUN_PEAK=2.3, RUN_SWELL=60; // runaway meows: start at an everyday meow's volume, reach PEAK x after SWELL s in hiding\nconst mice=[];")
rep("window.__wm={Snd,", "window.__wm={Snd,runaway,setRunMeow:(a,b,c)=>{ RUN_MEOW0=a; RUN_PEAK=b; RUN_SWELL=c; },")
open(P, 'w', encoding='utf-8').write(s); print('ok')
