// Whisker Meadow economy simulator: a scripted "player" drives the real game logic (no rendering) at high speed.
// Runs inside tools/sim/sim.html (a copy of the game with its own save key and the render loop disabled).
// Archetypes differ by attention (seconds between actions) and how well they use the systems.
(function(){
const ARCH={
  casual:   {over:0.5, act:5.0, fair:0.25, laser:false, helperAt:12, helperMax:1, savvy:0.4, searchTries:3, label:'Casual'},
  engaged:  {over:0.3, act:2.6, fair:0.7,  laser:true,  helperAt:9,  helperMax:3, savvy:0.75, searchTries:2, label:'Engaged'},
  optimizer:{over:0.1, act:1.6, fair:1.0,  laser:true,  helperAt:7,  helperMax:8, savvy:1.0, searchTries:1, label:'Optimizer'}};

function shopItem(id){ return SHOP.find(x=>x.id===id); }
function canBuy(id,reserve){ const it=shopItem(id); if(!it)return false; const av=it.avail?it.avail():true, mx=it.max?it.max():Infinity, have=id==='helper'?helpers.length:it.max?countItems(id):0;
  const need=it.need?it.need():0, hn=it.homes?it.homes():0; return av&&have<mx&&W.stars>=need&&W.homes.length>=hn&&W.money>=it.cost()+(reserve||0); }
function buy(id){ const it=shopItem(id), cost=it.cost(); W.money-=cost; it.buy(); W.stat.buys++; R.spend[id]=(R.spend[id]||0)+cost; R.buys.push([Math.round(W.time),id,cost]); }
function expandReq(){ const L=LEVELS[W.level+1]; if(!L)return null; return {cost:L.cost,stars:Math.min(5,W.level+1),homes:L.homes||0}; }

let R=null, B=null, nextAct=0, lastLog=-99, lastIncome=0, incomeWin=[];
function cats(){ return active().filter(c=>!c.outside&&!c.leaving); }

function start(arch,opts){
  B=Object.assign({},ARCH[arch],opts||{}); R={arch,label:B.label,log:[],events:[],buys:[],spend:{},idle:0,busy:0,acts:{},wallMoney:0,wallStars:0,wallHomes:0,maxed:null,ads:[],opts:opts||{}};
  // no lessons in the sim; quiet mode still holds events until the lessons would normally be over (~200 s)
  W.stat.good=3; W.stat.blinkBack=1; bt.skipped=true; W.stat.brushTut=1; br.done=true;
  begin(); nextAct=0; lastLog=-99; W.lastInput=0; R.t0=W.time; }

// humans also spend time just watching, exploring, reading: stretch every action by the archetype's overhead
function act(kind,cost){ R.acts[kind]=(R.acts[kind]||0)+1; R.busy+=cost; nextAct=W.time+cost/(1-B.over); W.lastInput=W.time; }

function decide(){
  const cs=cats(), n=cs.length, reserve=20+helpers.length*6;
  // rewarded-ad levers (what-if): summon a family now / guarantee the next match. Ads pause the game, so they cost real time only.
  // smart rewarded offer: help with whatever currently blocks the next room (stars -> a rescue arrives, homes -> a family comes, money -> a donation gift)
  if(B.adSmart&&W.stat.pairDone&&W.time-(R.lastAdS??-1e9)>B.adSmart){ const ex=expandReq(); if(ex){ let kind=null;
      if(W.stars<ex.stars){ if(!W.dropoff&&W.cats.length<LV().cap){ kind='rescue'; startDropoff(); } }
      else if(W.homes.length<ex.homes){ if(!W.family&&(W.night||0)<0.55&&!W.runaway&&cs.some(readyHome)){ kind='family'; visitT=0; } }
      else if(W.money<ex.cost){ const g=Math.max(60,Math.round(ex.cost*0.2)); W.money+=g; W.earned+=g; kind='gift'; }
      if(kind){ R.lastAdS=W.time; R.ads.push([Math.round(W.time),kind]); } } }
  if(B.adFamily&&!W.family&&W.stat.pairDone&&(W.night||0)<0.55&&!W.runaway&&cs.some(readyHome)&&W.time-(R.lastAdF??-1e9)>B.adFamily){ visitT=0; R.lastAdF=W.time; R.ads.push([Math.round(W.time),'family']); }
  // 1. a family is waiting: offer the best match
  const f=W.family; if(f&&(f.state==='wait'||(f.state==='arrive'&&f.t>8))&&!f.cat){ const ready=cs.filter(readyHome); if(ready.length){ const c=ready.find(k=>k.trait===f.want)||ready.sort((a,b)=>b.s.trust-a.s.trust)[0]; if(B.adMatch&&c.trait!==f.want&&W.time-(R.lastAdM??-1e9)>B.adMatch){ c.trait=f.want; R.lastAdM=W.time; R.ads.push([Math.round(W.time),'match']); } pickForHome(c); act('family',3); return; } }
  // 2. runaway: go and look
  if(W.runaway&&W.runaway.notified){ const c=W.runaway.c; R.search=(R.search||0)+1; if(R.search>=B.searchTries){ R.search=0; if(c.state==='hiding')foundCat(c); else if(c.pathEnd==='hide')caughtEarly(c); } act('search',6); return; }
  // 3. food: buy, then fill bowls
  const meals=(W.food||0)+(W.premium||0);
  if(meals<Math.max(12,n*2)&&W.money>=8){ W.money-=8; W.food+=12; R.spend.food=(R.spend.food||0)+8; act('buyfood',2); return; }
  const bowl=items.filter(i=>i.kind==='bowl'&&i.portions<i.cap/2).sort((a,b)=>a.portions-b.portions)[0];
  if(bowl&&meals>0){ useItem(bowl); act('feed',1.5); return; }
  // 4. litter
  const lit=items.filter(i=>i.kind==='litter'&&i.dirt>=2).sort((a,b)=>b.dirt-a.dirt)[0]; if(lit){ useItem(lit); act('scoop',1.5); return; }
  // 5. fair
  const fr=cs.filter(showReady); if(fr.length&&Math.random()<B.fair){ enterShow(fr.sort((a,b)=>b.s.groom-a.s.groom)[0]); act('fair',2); return; }
  // 6. shopping
  if(shopping(n,reserve))return;
  // 7. care: brush the scruffiest, play with the most bored, pet whoever needs trust
  const scruffy=cs.filter(c=>c.age>=0.3&&c.s.groom<50).sort((a,b)=>a.s.groom-b.s.groom)[0];
  if(scruffy&&Math.random()<0.5*B.savvy+0.2){ scruffy.s.groom=Math.min(100,scruffy.s.groom+21); W.stat.brush+=3; scruffy.s.aff=Math.min(100,scruffy.s.aff+1); act('brush',4); return; }
  const bored=cs.filter(c=>c.s.fun<40); if(bored.length&&Math.random()<0.6){ const k=W.laser&&B.laser?3:1; for(const c of bored.slice(0,k))c.s.fun=Math.min(100,c.s.fun+(k>1?15:12)); W.stat.pounces+=k*2; act(k>1?'laser':'wand',5); return; }
  const pet=cs.filter(c=>c.away<=0&&c.s.full>=35&&!['boop','path','greet','bye','hiding','carried'].includes(c.state)).sort((a,b)=>(a.s.trust+(a.age<1?20:0))-(b.s.trust+(b.age<1?20:0)));
  const tgt=pet.find(c=>c.s.trust<80)||pet[Math.floor(Math.random()*pet.length)];
  if(tgt){ for(let i=0;i<4;i++)onStroke(tgt,pick(['head','cheek','chin','back']),false,true); act('pet',6.5); if(tgt.s.trust>=80)R.idle+=3; return; }
  R.idle+=B.act; act('idle',B.act); }

function shopping(n,reserve){
  const ex=expandReq(), exReady=ex&&W.stars>=ex.stars&&W.homes.length>=ex.homes;
  if(ex&&exReady&&W.money>=ex.cost){ buy('expand'); R.events.push([Math.round(W.time),'expand',W.level]); act('shop',3); return true; }
  // savvy players save for the next room once the stars/homes are there
  const saving=exReady&&Math.random()<B.savvy;
  if(B.laser&&!W.laser&&canBuy('laser',reserve)){ buy('laser'); act('shop',3); return true; }
  const want=[['bowl',Math.ceil(n/3)],['litter',Math.ceil(n/4)],['bed',Math.ceil(n/4)],['ball',Math.ceil(n/4)],['tree',Math.ceil(n/6)],['shelter',Math.ceil(n/7)]];
  for(const [id,k] of want){ if(countItems(id)<k&&canBuy(id,reserve+(saving?ex.cost:0))){ buy(id); act('shop',3); return true; } }
  const inc=income();
  if(n>=B.helperAt&&helpers.length<B.helperMax&&canBuy('helper',reserve+60+(saving?ex.cost:0))&&inc>(helpers.length+1)*6*1.6){ buy('helper'); R.events.push([Math.round(W.time),'helper',helpers.length]); act('shop',3); return true; }
  return false; }

function income(){ // $ per minute over the last 3 minutes
  const w=incomeWin; if(w.length<2)return 0; const a=w[0], b=w[w.length-1]; return (b[1]-a[1])/Math.max(1,(b[0]-a[0])/60); }

function log(){ const cs=cats(), happy=cs.length?cs.reduce((s,c)=>s+(c.s.aff+c.s.health)/2,0)/cs.length:0, ex=expandReq();
  incomeWin.push([W.time,W.earned]); while(incomeWin.length&&W.time-incomeWin[0][0]>180)incomeWin.shift();
  // which gate is holding the next expansion back
  if(ex){ if(W.stars<ex.stars)R.wallStars+=30; else if(W.homes.length<ex.homes)R.wallHomes+=30; else if(W.money<ex.cost)R.wallMoney+=30; } else if(R.maxed==null)R.maxed=Math.round(W.time);
  R.log.push({t:Math.round(W.time),money:Math.round(W.money),earned:Math.round(W.earned||0),cats:cs.length,homes:W.homes.length,level:W.level,stars:W.stars,ribbons:W.ribbons,helpers:helpers.length,
    happy:Math.round(happy),inc:Math.round(income()),showTier:W.showTier,food:W.food,ach:Object.values(W.achT).reduce((a,b)=>a+b,0)}); }

function run(seconds,dt=0.05){
  const end=W.time+seconds; let guard=0;
  while(W.time<end&&guard++<1e7){
    if(!$('#meet').hidden||cam.meet)nextMeet(); if(!$('#modal').hidden)closeModal(); W.paused=false;
    if(W.time-R.t0>200&&!W.stat.pairDone){ W.stat.pairDone=1; W.stat.pairDoneT=W.time; }
    update(dt); updateFamilyMeshes(dt,W.time); updateBirds(dt,W.time);
    if(W.time>=nextAct)decide();
    if(W.time-lastLog>=30){ lastLog=W.time; log(); } }
  return R; }

async function post(name){ R.final={money:Math.round(W.money),earned:Math.round(W.earned||0),homes:W.homes.length,level:W.level,stars:W.stars,ribbons:W.ribbons,helpers:helpers.length,cats:cats().length,kittens:W.stat.kittens,rescues:W.stat.rescues,found:W.stat.found,runs:W.stat.runNotes||0,showTier:W.showTier,achT:W.achT,stat:{shows:W.stat.shows,good:W.stat.good}};
  const r=await fetch('http://127.0.0.1:8767/'+name,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(R)}); return r.status; }
async function chunk(id,arch,total,c=1200,opts){ if(!R||R.id!==id){ start(arch,opts); R.id=id; } const left=total-(W.time-R.t0); if(left>0)run(Math.min(c,left));
  const L=R.log[R.log.length-1]; const sum=`${id} t=${Math.round(W.time-R.t0)} lvl=${W.level} homes=${W.homes.length} cats=${L.cats} $=${L.money} earned=${L.earned} happy=${L.happy} ex=${R.events.filter(e=>e[1]==='expand').map(e=>e[0]).join(',')}`;
  if(W.time-R.t0>=total-0.5){ await post(id); return 'POSTED '+sum; } return sum; }
window.SIMBOT={start,run,post,chunk,ARCH,get R(){return R;}};
})();
