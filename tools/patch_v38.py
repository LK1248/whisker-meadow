"""v38: the adoption card wall. Every thank-you postcard gets pinned to a corkboard beside the sanctuary house.
Tap the board to open the wall of all cards; tap a card to see it full size again. Happy Tails cards reopen too."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    if s.count(old) != count: sys.exit(f'match count {s.count(old)} != {count} for: {old[:80]}')
    s = s.replace(old, new)

# CSS: cork wall gallery, clickable cards, big-card back button
rep(".pc img{width:100%;", """.wall{background:#c99560 radial-gradient(#b7834f 1px,transparent 1.6px) 0 0/9px 9px;border:10px solid #8a5a3b;border-radius:14px;padding:14px;box-shadow:inset 0 2px 8px rgba(0,0,0,.25)}
.wall .cards{gap:14px}
button.pc{border:0;font:inherit;color:inherit;text-align:left;cursor:pointer;position:relative;transition:transform .15s}
button.pc:hover,button.pc:focus-visible{transform:rotate(0) scale(1.04);z-index:1}
.wall .pc::before{content:'';position:absolute;top:-5px;left:50%;width:12px;height:12px;margin-left:-6px;border-radius:50%;background:#e0507a;box-shadow:0 2px 3px rgba(0,0,0,.3)}
.wall .pc:nth-child(3n)::before{background:#f6c443}.wall .pc:nth-child(3n+1)::before{background:#5b9be6}
.wempty{font-size:54px;text-align:center;padding:30px 0;opacity:.6}
h3 .cnt{color:#e0507a;font-size:20px;margin-left:6px}
.pc img{width:100%;""")

# board mesh + texture + wall UI, defined before the house
rep("function sanctuaryHouse(){", r"""// ---- adoption card wall: thank-you postcards pinned on a corkboard by the house ----
let cardBoard=null, boardSig='', boardT=0; const boardImgs={};
function boardRand(a){ return ()=>{ a=a+0x6D2B79F5|0; let t=Math.imul(a^a>>>15,1|a); t=t+Math.imul(t^t>>>7,61|t)^t; return ((t^t>>>14)>>>0)/4294967296; }; }
function cardOn(hm,i){ return !hm.noCard&&!!hm.img&&!W.postQ.some(q=>q.i===i); }
function wallCards(){ return W.homes.map((hm,i)=>({hm,i})).filter(o=>cardOn(o.hm,o.i)).reverse(); }
function drawBoard(){ if(!cardBoard)return; const cv=cardBoard.userData.cv, x=cv.getContext('2d'), w=cv.width, h=cv.height;
  x.fillStyle='#c99560'; x.fillRect(0,0,w,h); const rr=boardRand(7); x.fillStyle='rgba(120,75,35,.25)'; for(let i=0;i<500;i++){ x.beginPath(); x.arc(rr()*w,rr()*h,1+rr()*1.6,0,7); x.fill(); }
  x.strokeStyle='#8a5a3b'; x.lineWidth=22; x.strokeRect(11,11,w-22,h-22);
  const L=wallCards().slice(0,12), n=L.length, cols=n<=4?2:n<=9?3:4, rows=n<=4?2:3, cw=(w-60)/cols, ch=(h-60)/rows, pins=['#e0507a','#f6c443','#5b9be6'];
  if(!L.length){ x.font='700 120px sans-serif'; x.textAlign='center'; x.textBaseline='middle'; x.globalAlpha=.35; x.fillStyle='#fff'; x.fillText('♥',w/2,h/2+6); x.globalAlpha=1; }
  L.forEach((o,k)=>{ const r2=boardRand(o.i*31+5), cx=30+cw*(k%cols)+cw/2+(r2()-.5)*10, cy=30+ch*Math.floor(k/cols)+ch/2+(r2()-.5)*8, a=(r2()-.5)*0.22, pw=cw*0.86, ph=ch*0.86;
    x.save(); x.translate(cx,cy); x.rotate(a); x.shadowColor='rgba(0,0,0,.35)'; x.shadowBlur=8; x.shadowOffsetY=3; x.fillStyle='#fff'; x.fillRect(-pw/2,-ph/2,pw,ph); x.shadowColor='transparent';
    const im=boardImgs[o.i]; if(im&&im.complete&&im.naturalWidth){ const iw=pw-12, ih=ph-12; const sr=Math.max(iw/im.naturalWidth,ih/im.naturalHeight), sw=iw/sr, sh=ih/sr;
      x.drawImage(im,(im.naturalWidth-sw)/2,(im.naturalHeight-sh)/2,sw,sh,-iw/2,-ih/2,iw,ih); } else { x.fillStyle='#f3e7d6'; x.fillRect(-pw/2+6,-ph/2+6,pw-12,ph-12); }
    x.fillStyle=pins[k%3]; x.beginPath(); x.arc(0,-ph/2+4,7,0,7); x.fill(); x.restore(); });
  cardBoard.material.map.needsUpdate=true; }
function boardSync(force){ const L=wallCards(); let wait=false;
  for(const o of L.slice(0,12))if(!boardImgs[o.i]||boardImgs[o.i].src!==o.hm.img){ const im=new Image(); im.onload=()=>{ boardSig=''; }; im.src=o.hm.img; boardImgs[o.i]=im; wait=true; }
  const sig=L.slice(0,12).map(o=>o.i+(boardImgs[o.i]&&boardImgs[o.i].complete?'y':'n')).join(',');
  if(force||sig!==boardSig){ boardSig=sig; drawBoard(); } }
function cardBoardMesh(){ const g=new THREE.Group(); g.position.set(2.65,0,0.5); g.rotation.y=-0.22;
  for(const sx of [-0.78,0.78]) g.add(mesh(G.box,0x8a5a3b,{p:[sx,1.05,-0.03],s:[0.1,2.1,0.1]}));
  g.add(mesh(G.box,0xa5754a,{p:[0,2.14,0.02],s:[1.8,0.08,0.3]}));
  const cv=document.createElement('canvas'); cv.width=640; cv.height=480; const tex=new THREE.CanvasTexture(cv); if(renderer.capabilities)tex.anisotropy=Math.min(4,renderer.capabilities.getMaxAnisotropy());
  const b=new THREE.Mesh(new THREE.PlaneGeometry(1.5,1.125),new THREE.MeshBasicMaterial({map:tex})); b.position.set(0,1.5,0.03); b.userData.cv=cv; g.add(b);
  g.add(mesh(G.box,0x8a5a3b,{p:[0,1.5,0],s:[1.56,1.18,0.04]}));
  cardBoard=b; boardSig=''; boardSync(true); return g; }
function tapBoard(e){ if(!cardBoard)return false; setRay(e); if(!ray.intersectObject(cardBoard,false).length)return false; Snd.ding(); openWall(); return true; }
function cardHTML(hm){ return `<div class="postcard">${hm.thanks?`<b class="ty">Thank you!</b>`:''}${hm.img?`<img src="${hm.img}" alt="${hm.name} in a new home">`:''}<p>${hm.thanks?`Thank you for ${hm.name}! `:''}${hm.line}</p><small>Love, the ${hm.fam} family</small></div>`; }
function openCard(i,back){ const hm=W.homes[i]; if(!hm)return; openModal(cardHTML(hm)+`<button class="big" id="pcBack" aria-label="Back to the card wall">↩</button>`,true); $('#pcBack').onclick=back||closeModal; }
function bindCards(back){ document.querySelectorAll('#mbox [data-hi]').forEach(b=>b.onclick=()=>{ Snd.ding(); openCard(+b.dataset.hi,back); }); }
function openWall(){ const L=wallCards();
  openModal(`<h3>Happy Tails<span class="cnt">♥ ${L.length}</span></h3><div class="wall">${L.length?`<div class="cards">${L.map(o=>`<button class="pc" data-hi="${o.i}"><img src="${o.hm.img}" alt="${o.hm.name} at home"><b>${o.hm.name}</b><span>with the ${o.hm.fam} family</span></button>`).join('')}</div>`:'<div class="wempty">\u{1F48C}</div>'}</div>`);
  bindCards(openWall); }
function boardPop(){ boardSync(true); if(!cardBoard)return; const p=cardBoard.getWorldPosition(new V3()); p.y+=0.2; spawnFx('spark',p,8,.6); spawnFx('h',p,3,.4); }
function sanctuaryHouse(){""")
rep("  // bench, mailbox, hay\n", "  g.add(cardBoardMesh());\n  // bench, mailbox, hay\n")

# tapping the board in the world opens the wall
rep("else if(!tapWildlife(e)){ tag.c=null; leaveClose(true); }", "else if(!tapWildlife(e)&&!tapBoard(e)){ tag.c=null; leaveClose(true); }")

# postcard arrival: shared card HTML; pin it on the board when closed
rep("""openModal(`<div class="postcard">${hm.thanks?`<b class="ty">Thank you!</b>`:''}${hm.img?`<img src="${hm.img}" alt="${hm.name} in a new home">`:''}<p>${hm.thanks?`Thank you for ${hm.name}! `:''}${hm.line}</p><small>Love, the ${hm.fam} family</small></div><button class="big" id="pcOk">Aww</button>`,true); $('#pcOk').onclick=closeModal; Snd.chime(); } }""",
    """openModal(cardHTML(hm)+`<button class="big" id="pcOk">Aww</button>`,true); $('#pcOk').onclick=()=>{ closeModal(); boardPop(); }; Snd.chime(); } }
  if((boardT-=dt)<=0){ boardT=2; boardSync(); }""")

# Happy Tails tab: cards with a postcard reopen it
rep("""W.homes.slice().reverse().map(hm=>`<div class="pc">${hm.img?`<img src="${hm.img}" alt="${hm.name} at home">`:'<img alt="">'}<b>${hm.name}</b><span>with the ${hm.fam} family</span></div>`).join('')""",
    """W.homes.map((hm,i)=>({hm,i})).reverse().map(({hm,i})=>{ const on=cardOn(hm,i), t=on?'button':'div'; return `<${t} class="pc"${on?` data-hi="${i}"`:''}>${hm.img?`<img src="${hm.img}" alt="${hm.name} at home">`:'<img alt="">'}<b>${hm.name}</b><span>with the ${hm.fam} family</span></${t}>`; }).join('')""")
rep("  document.querySelectorAll('[data-tab]').forEach(b=>b.onclick=()=>openBadges(b.dataset.tab)); }",
    "  document.querySelectorAll('[data-tab]').forEach(b=>b.onclick=()=>openBadges(b.dataset.tab)); if(tab==='tails')bindCards(()=>openBadges('tails')); }")

rep("Postcards arrive later; see them in Badges → Happy Tails.", "Postcards arrive later and get pinned on the card board by the house: tap it to see them all. They're also in Badges → Happy Tails.")
rep("window.__wm={", "window.__wm={openWall,openCard,boardSync,drawBoard,wallCards,get cardBoard(){return cardBoard;},")
open(P, 'w', encoding='utf-8').write(s); print('ok')
