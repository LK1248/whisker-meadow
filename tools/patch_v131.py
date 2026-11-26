"""v131: goals are lifetime totals with Bronze / Silver / Gold tiers, shown only in the Sanctuary 'Goals' tab
(the on-screen goals strip is gone). Each tier pays once: $15 / $30 / $60. Tiers reached are kept in W.stat.goalT
(saved). On an old save (or a new game) tiers already reached are recorded silently, without pay or toasts."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count: sys.exit(f'match count {n} != {count} for: {old[:80]}')
    s = s.replace(old, new)

a = s.find("function updateGoals(){"); b = s.find("\n\n/* ================= UI")
if a < 0 or b < 0 or b < a or s.find("function goalStripTick(){", a) > b: sys.exit('goal block not found')
s = s[:a] + """const GOAL_TIERS=[[15,45,120],[3,10,25],[3,10,25],[8,25,60],[2,6,15],[10,30,80],[3,10,25],[1,5,15],[1,5,12],[2,8,20]], GOAL_PAY=[15,30,60];
function goalTier(i){ const v=GOALS[i][1]()||0; let t=0; while(t<3&&v>=GOAL_TIERS[i][t])t++; return t; }
function updateGoals(){ const st=W.stat; if(!Array.isArray(st.goalT)||st.goalT.length!==GOALS.length){ st.goalT=GOALS.map((g,i)=>goalTier(i)); return; }
  GOALS.forEach((g,i)=>{ const t=goalTier(i), was=st.goalT[i]||0; if(t<=was)return; let pay=0; for(let k=was;k<t;k++)pay+=GOAL_PAY[k]; st.goalT[i]=t; W.money+=pay; hud(); toast(`✓ ${g[0]} · ${TIER_N[t]} +$${pay}`,'badge',3000); Snd.coin(); rec('goal',`${g[0]} ${TIER_N[t]}`); }); }
function renderGoals(){}
function goalStripTick(){ const el=$('#goalStrip'); if(el&&!el.hidden)el.hidden=true; }""" + s[b:]

i = s.find("  else body=W.goals.map(g=>{"); key = '<p class="starHow">Each goal pays $15, and a new one takes its place.<br>'; j = s.find(key)
if i < 0 or j < 0 or j < i: sys.exit('goals tab not found')
j += len(key)
s = s[:i] + """  else body=GOALS.map((g,i)=>({g,i})).filter(({i})=>!GOAL_OPEN[i]||GOAL_OPEN[i]()||goalTier(i)>0).map(({g,i})=>{ const t=goalTier(i), v=g[1]()||0, nx=GOAL_TIERS[i][t]; return `<div class="goal ${t>=3?'done':''}"><i class="gm t${t}">${t?'★':''}</i>${g[0]}<span>${nx!==undefined?`${v} / ${nx}`:'Gold!'}</span></div>`; }).join('')+`<p class="starHow">Goals count everything you have ever done. Bronze +$15 · Silver +$30 · Gold +$60.<br>""" + s[j:]
rep("#lockTip{position:fixed;", ".goal .gm{display:inline-block;width:20px;height:20px;border-radius:50%;margin-right:7px;text-align:center;font:700 12px/20px var(--body);background:#eadfd3;color:#fff;vertical-align:-4px;font-style:normal}.goal .gm.t1{background:#e1a06a}.goal .gm.t2{background:#aab6c3}.goal .gm.t3{background:#f2bd2c}\n#lockTip{position:fixed;")
open(P, 'w', encoding='utf-8').write(s)
print('v131 applied')
