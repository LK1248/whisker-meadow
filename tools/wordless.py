"""Wordless variant: no language anywhere on screen. Icons, pictures, symbols and numbers only.
Run on a fresh copy of main's whisker-meadow.html (branch `wordless`):  python tools/wordless.py
Kept on purpose: aria-labels/alt text (invisible, for screen readers), the page <title>, the dev panel (?dev only)."""
import re, sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    if s.count(old) != count: sys.exit(f'match count {s.count(old)} != {count} for: {old[:90]}')
    s = s.replace(old, new)
def cut(start, end, new):
    """replace s[start:end) (end marker kept)"""
    global s
    i0 = s.index(start); i1 = s.index(end, i0)
    s = s[:i0] + new + s[i1:]

# ---------------- static page ----------------
s = re.sub(r' title="(?!\$\{)[^"]*"', '', s)                      # hover tooltips
for t in ['Pet', 'Brush', 'Wand', 'Laser']:                          # dock labels
    s = re.sub(r'(data-tool="%s"[^\n]*?</svg>)%s(</button>)' % ({'Pet':'hand'}.get(t,t.lower()), t), r'\1\2', s)
rep('<span class="lbl">Shop</span>', '')
s = re.sub(r'<span class="lbl">[A-Za-z ]+</span>', '', s)
rep('<button class="big" id="mOk">Hello!</button>', '<button class="big" id="mOk" aria-label="OK">👋</button>')
LOGO = ('<svg viewBox="0 0 160 110" width="200" height="138" style="display:block;margin:0 auto 6px" aria-label="Whisker Meadow"><g transform="translate(80,62) scale(2.3)">'
        '<path d="M-13 -3L-12 -18-3 -11zM13 -3L12 -18 3 -11z" fill="#f3a64a"/><circle r="13" fill="#f3a64a"/>'
        '<path d="M-4 -1q-2.5 2.5-5 0M9 -1q-2.5 2.5-5 0" stroke="#4a3426" stroke-width="1.6" fill="none" stroke-linecap="round"/>'
        '<path d="M-2 4h4l-2 2z" fill="#ff8fa3"/></g>'
        '<path transform="translate(136,26) scale(1.3)" d="M0 9s-8.5-5.2-8.5-11a4.5 4.5 0 0 1 8.5-2.5 4.5 4.5 0 0 1 8.5 2.5c0 5.8-8.5 11-8.5 11z" fill="#ff6f99"/>'
        '<path transform="translate(24,30) scale(0.9)" d="M0 9s-8.5-5.2-8.5-11a4.5 4.5 0 0 1 8.5-2.5 4.5 4.5 0 0 1 8.5 2.5c0 5.8-8.5 11-8.5 11z" fill="#ff9ec0"/></svg>')
rep('<h1>Whisker <em>Meadow</em></h1>\n    <p>Make shy cats happy.</p>', LOGO)
rep('<button class="play" id="bPlay">Play</button><br><button class="play new" id="bNew" hidden>New meadow</button>',
    '<button class="play" id="bPlay" aria-label="Play">▶</button><br><button class="play new" id="bNew" hidden aria-label="New meadow">✚</button>')
rep("if(prev)$('#lastRun').textContent=`Last time: ${prev.cats} cats · score ${prev.score}`;", "if(prev)$('#lastRun').textContent=`🐈 ${prev.cats} · 🏆 ${prev.score}`;")
rep("if(hasSave){ $('#bPlay').textContent='Continue'; $('#bNew').hidden=false; }", "if(hasSave){ $('#bNew').hidden=false; }")

# ---------------- generic filter for floating words and toasts ----------------
rep("function floatAt(x,y,text,cls=''){ const d=", """// wordless: known phrases become symbols; anything else loses its letters (and is dropped if nothing is left)
const WL={'Full':'✓','No food!':'🐟 0','Clean':'✨','Ouch!':'💢','Grown up!':'✨🐈✨','Treat!':'♥','To the fair!':'🏆','Forever home here':'🏠♥','Can find a home':'🏠',
  'Home safe':'🏠♥','Found you!':'♥','Loves butt taps!':'♥♥','Not a fan':'✗','Keeping this one':'🏠♥','Not ready yet':'⏳','Needs a brush':'✗','Not quite':'✗',
  'Purr!':'♥','Helpers back to work':'✓','Tap a cat to give it the collar':'👆🐈','Always daytime':'☀','Day & night: on':'☀☾','Bigger meadow!':'🌱⬆',
  'No one is ready yet':'⏳',"We'll come back!":'👋',"We'll keep looking!":'👋','Maybe another day!':'👋','Saying hello…':'👋','Not enough for wages: helpers are resting':'$ ✗'};
function wl(t){ t=String(t); if(WL[t]!=null)return WL[t]; const r=t.replace(/[A-Za-z\\u00C0-\\u024F]+(['’][A-Za-z]+)?/g,'').replace(/\\s+/g,' ').trim(); return /[0-9$★♥✓✗×+\\u{1F300}-\\u{1FAFF}\\u2600-\\u27BF]/u.test(r)?r:''; }
function floatAt(x,y,text,cls=''){ text=wl(text); if(!text)return; const d=""")
rep("floatAt(fx,fy,c.streak>=2?`Purr! ×${c.streak}`:'Purr!','good');", "floatAt(fx,fy,c.streak>=2?`♥ ×${c.streak}`:'♥','good');")
rep("function toast(html,cls='',ms=2600){ const d=", "function toast(html,cls='',ms=2600){ if(!/^</.test(html)){ html=wl(html); if(!html)return; } const d=")
rep("toast(`Collar returned: $${pr} back`);", "toast(`↩ $${pr}`);")
rep("toast(LV().name?LV().name+' open!':'Bigger meadow!');", "toast('🌱⬆');")
rep("toast('★'.repeat(st)+' Sanctuary!','badge',3600);", "toast('★'.repeat(st),'badge',3600);")
rep("toast(c.name+' slipped out!');", "toast('🐾 !');")

# ---------------- badges & goals: an emoji per badge ----------------
rep("const TIER_N=['','Bronze','Silver','Gold'];", """const TIER_N=['','🥉','🥈','🥇'];
const ACH_E={rhythm:'🎵',blink:'😌',homes:'🏡',pairs:'💞',patient:'🐢',rescues:'🚪',found:'🔦',quick:'⚡',ribbons:'🎀',kittens:'🍼',belly:'🤗',butt:'🍑',family:'🏘️',coats:'🌈',cards:'💌',rare:'💎',breeds:'🌍',spotless:'🧹',zoomies:'🔴',deluxe:'🛋️',ouch:'🩹',herd:'🐾'};
const GOAL_E=['🎵','🧹','🥣','✨','😌','🪶','🤝','🎀','🏡','🍑'];""")
rep("toast(`★ ${n} · ${TIER_N[t]} +$${rw}`,'badge',3400);", "toast(`${ACH_E[id]||'★'} ${TIER_N[t]} +$${rw}`,'badge',3400);")
rep("toast(`✓ ${n} +$15`,'badge',3000);", "toast(`✓ ${GOAL_E[g.i]} +$15`,'badge',3000);")
cut("function openBadges(tab='badges'){", "$('#bShop').onclick=", """function openBadges(tab='badges'){
  const tabs=`<div class="tabs"><button data-tab="badges" class="${tab==='badges'?'on':''}" aria-label="Badges">🏅</button><button data-tab="tails" class="${tab==='tails'?'on':''}" aria-label="Postcards">💌 ${W.homes.length}</button><button data-tab="goals" class="${tab==='goals'?'on':''}" aria-label="Goals">🎯</button></div>`;
  let body='';
  if(tab==='badges') body=`<div class="grid">${ACH.map(([id,n,d,f,th])=>{ const t=W.achT[id]||0, v=f(), nx=th[t]; return `<div class="badge-i ${t?'t'+t:''}"><div class="medal" style="font-size:24px">${ACH_E[id]}</div><div><b style="font-size:22px">${TIER_N[t]||'·'}</b><div class="pips">${nx!==undefined?`${Math.min(v,nx)} / ${nx}`:'🥇'}</div></div></div>`; }).join('')}</div>`;
  else if(tab==='tails') body=W.homes.length?`<div class="cards">${W.homes.map((hm,i)=>({hm,i})).reverse().map(({hm,i})=>{ const on=cardOn(hm,i), t=on?'button':'div'; return `<${t} class="pc"${on?` data-hi="${i}"`:''}>${hm.img?`<img src="${hm.img}" alt="">`:'<img alt="">'}<span>${FAM_SVG.replace('<svg ','<svg width="34" height="26" ')}</span></${t}>`; }).join('')}</div>`:'<p class="center" style="font-size:40px;margin:16px 0">💌</p>';
  else body=W.goals.map(g=>{ const [n,f,tg]=GOALS[g.i]; const v=Math.max(0,Math.min(tg,f()-g.base)); return `<div class="goal ${g.done?'done':''}"><span style="font-size:22px">${g.done?'✓ ':''}${GOAL_E[g.i]}</span><span>${g.done?'+$15':`${v} / ${tg}`}</span></div>`; }).join('');
  openModal(`<h3>${'★'.repeat(W.stars)}</h3>${tabs}${tab==='badges'?`<p style="margin:-4px 0 10px;color:var(--muted);font:700 15px var(--body)">🥉 +$10 \\u00b7 🥈 +$25 \\u00b7 🥇 +$60</p>`:''}${body}`);
  document.querySelectorAll('[data-tab]').forEach(b=>b.onclick=()=>openBadges(b.dataset.tab)); if(tab==='tails')bindCards(()=>openBadges('tails')); }
""")

# ---------------- shop ----------------
rep("""const lbl=!avail?(it.id==='laser'?'Owned':'Maxed'):have>=max?'Full':!starOk?`★${need} needed`:!hOk?`${hn} homes needed`:it.id==='fire'?'Let one go':`$${cost}`;""",
    """const lbl=!avail?'✓':have>=max?'✓':!starOk?`🔒 ★${need}`:!hOk?`🔒 🏡${hn}`:it.id==='fire'?'−1':`$${cost}`;""")
rep("""const desc=it.id==='expand'?(LEVELS[W.level+1]?`Room for ${LEVELS[W.level+1].cap} cats${LEVELS[W.level+1].ponds?' \\u00b7 new pond':''}`:'Biggest already'):it.desc;""",
    """const desc=it.id==='expand'?(LEVELS[W.level+1]?`🐈 ${LEVELS[W.level+1].cap}${LEVELS[W.level+1].ponds?' \\u00b7 💧':''}`:''):(SHOP_D[it.id]||'');""")
rep("<div class=\"ico\"><svg viewBox=\"0 0 24 24\">${IC[it.id]}</svg></div><b>${it.name()}</b><span>${desc}",
    "<div class=\"ico\"><svg viewBox=\"0 0 24 24\">${IC[it.id]}</svg></div><span>${[desc,it.max&&max<99?`${have}/${max}`:''].filter(Boolean).join(' · ')}")
rep("join(' \u00b7 ')}${it.max&&max<99?` · ${have}/${max}`:''}</span><button data-buy", "join(' \u00b7 ')}</span><button data-buy")
rep("<div class=\"ico\"><svg viewBox=\"0 0 24 24\">${IC[k]}</svg></div><b>${TIERS[k][n-1]}</b><span>${TIER_DESC[k][n-1]}</span><button data-up=\"${k}\" ${can?'':'disabled'}>${sOk?`$${cost}`:`★${starsFor(n)} needed`}</button>",
    "<div class=\"ico\"><svg viewBox=\"0 0 24 24\">${IC[k]}</svg></div><span style=\"font-size:16px;letter-spacing:2px\">${'●'.repeat(n)}${'○'.repeat(TIERS[k].length-n)}</span><button data-up=\"${k}\" ${can?'':'disabled'}>${sOk?`$${cost}`:`🔒 ★${starsFor(n)}`}</button>")
rep("openModal(`<h3>Shop</h3><div class=\"grid\">${cards}</div>${ups?`<h3 style=\"margin-top:18px\">Upgrades</h3><div class=\"grid\">${ups}</div>`:''}`);",
    "openModal(`<h3 aria-label=\"Shop\"><svg viewBox=\"0 0 24 24\" width=\"34\" height=\"34\">${H_BAG}</svg></h3><div class=\"grid\">${cards}</div>${ups?`<h3 style=\"margin-top:18px\" aria-label=\"Upgrades\">⬆</h3><div class=\"grid\">${ups}</div>`:''}`);")
rep("function openShop(guide){", "const SHOP_D={food:'+12',premium:'+12 ✨',fire:'−$6',helper:'−$6 ⏱'};\nfunction openShop(guide){")
rep("toast(W.dayOn?'Day & night: on':'Always daytime');", "toast(W.dayOn?'☀☾':'☀');")

# ---------------- collars ----------------
rep("openModal(`<h3>Choose a collar</h3><p style=\"margin:0 0 8px;color:var(--muted);font:700 14px var(--body)\">$15, then tap a cat to put it on.</p>",
    "openModal(`<h3 aria-label=\"Collars\"><svg viewBox=\"0 0 24 24\" width=\"34\" height=\"34\">${IC.collar}</svg></h3><p style=\"margin:0 0 8px;color:var(--muted);font:700 16px var(--body)\">$15 → 👆🐈</p>")
rep("<p style=\"margin:12px 0 6px;color:var(--muted);font:700 14px var(--body)\">Special collars ($30), unlocked by gold badges (you have ${g}):</p>",
    "<p style=\"margin:12px 0 6px;color:var(--muted);font:700 16px var(--body)\">$30 · 🥇 ${g}</p>")
rep("title=\"${sp.name}${g>=sp.gold?'':' · '+sp.gold+' gold'}\" ", "")

# ---------------- cat tag ----------------
rep("$('#tName').innerHTML=`${c.name}${c.age<1?' <small>kitten</small>':''}`;", "$('#tName').innerHTML=c.age<1?'🍼':'';")
rep("const lab=(W.tagShows||0)<=6;", "const lab=false;")
rep("$('#tTrait').textContent=c.trait+(c.forever?' · stays here':readyHome(c)?' · ready for a home':'');",
    "$('#tTrait').innerHTML=tsvg(c.trait)+(c.forever?' 🏠♥':readyHome(c)?' 🏠':'');")
rep("<button id=\"tStay\" hidden>${STAY_SVG}Keep</button>", "<button id=\"tStay\" hidden aria-label=\"Keep\">${STAY_SVG}</button>")

# ---------------- fair result ----------------
rep("const cats=[['Best Purr',s.aff],['Fluffiest Coat',s.groom],['Healthiest',s.health],['Most Improved',Math.min(100,(s.trust-c.trust0)*2.2)],['Bravest Rescue',c.origin==='stray'?Math.min(100,s.trust+25):0],['Best Friends',bv]];",
    "const cats=[['♥',s.aff],['✨',s.groom],['🌿',s.health],['📈',Math.min(100,(s.trust-c.trust0)*2.2)],['🦁',c.origin==='stray'?Math.min(100,s.trust+25):0],['💞',bv]];")
rep("if(COATS[c.coat.base].rare)cats.push(['Rarest Coat',80]); if(c.collar)cats.push(['Best Dressed',74]);", "if(COATS[c.coat.base].rare)cats.push(['💎',80]); if(c.collar)cats.push(['🎀',74]);")
rep("lbl=place+['','st','nd','rd'][place];", "lbl=String(place);")
rep("<h3 class=\"center\" style=\"margin:0\">${c.name}</h3><div class=\"center\" style=\"font:600 19px var(--display);color:var(--pinkd)\">${cat}</div><div class=\"prize\">+$${prize}</div><button class=\"big\" id=\"collect\">Collect</button>",
    "<div class=\"center\" style=\"font-size:34px\">${cat}</div><div class=\"prize\">+$${prize}</div><button class=\"big\" id=\"collect\" aria-label=\"Collect\">✓</button>")

# ---------------- meet sheet (new arrivals) ----------------
rep("$('#mName').textContent=m.c.name;", "$('#mName').textContent='';")
rep("$('#mOrg').innerHTML=(m.origin==='born'?`${heart}<span>${m.parents[0].name} + ${m.parents[1].name}</span>`:m.origin==='mama'?`${gate}<span>A mama cat at the gate</span>`:m.origin==='withmama'?`${heart}<span>${m.parents[0].name}'s kitten</span>`:`${gate}<span>Found at the gate</span>`)+`<span>\\u00b7 ${coatName(m.c.coat)}${m.c.age<1?' kitten':''} \\u00b7 ${m.c.trait}</span>`;",
    "$('#mOrg').innerHTML=(m.origin==='born'||m.origin==='withmama'?heart:gate)+`<span style=\"font-size:20px\">${m.c.age<1?'🍼':''}</span>${tsvg(m.c.trait)}`;")
rep("<b>${c.name}${c.age<1?' <small>kitten</small>':''}</b>", "<b>${c===m.c?'✨':''}${c.age<1?'🍼':''}</b>")

# ---------------- family & runaway panels ----------------
rep("if(msg) el.innerHTML=`${x}<div class=\"fam\">${FAM_SVG}<div class=\"want\">${msg}</div></div>`;", "if(msg) el.innerHTML=`${x}<div class=\"fam\">${FAM_SVG}<div class=\"want\" style=\"font-size:28px\">${wl(msg)}</div></div>`;")
rep("<div><div class=\"want\">Tap a cat</div><div class=\"sub\">one with a little house</div></div></div><div class=\"fb\"><button id=\"fCancel\">Back</button></div>",
    "<div class=\"want\" style=\"font-size:28px\">👆 🏠</div></div><div class=\"fb\"><button id=\"fCancel\" aria-label=\"Back\">↩</button></div>")
rep("<div><div class=\"sub\">The ${f.name} family would love</div><div class=\"want\">${tsvg(f.want)} a ${f.want} cat</div></div></div><div class=\"fb\"><button id=\"fNo\">Not now</button><button class=\"go\" id=\"fPick\">Pick a cat</button></div>",
    "<div class=\"want\" style=\"font-size:26px\">♥ ${tsvg(f.want).replace(/22px/g,'34px')}</div></div><div class=\"fb\"><button id=\"fNo\" aria-label=\"Not now\">✗</button><button class=\"go\" id=\"fPick\" aria-label=\"Pick a cat\">👆 🏠</button></div>")
rep("<div><div class=\"want\">${R.c.name} is missing!</div><div class=\"sub\">slipped out the gate</div></div></div><button id=\"mGo\">Go look</button>",
    "<div class=\"want\" style=\"font-size:28px\">🐈 ?</div></div><button id=\"mGo\" aria-label=\"Go look\">🔍</button>")
rep("<div><div class=\"want\">Follow the paw prints</div><div class=\"sub\">listen for meows</div></div></div>", "<div class=\"want\" style=\"font-size:28px\">🐾 👂</div></div>")

# ---------------- postcards & card wall ----------------
rep("function cardHTML(hm){ return `<div class=\"postcard\">${hm.thanks?`<b class=\"ty\">Thank you!</b>`:''}${hm.img?`<img src=\"${hm.img}\" alt=\"${hm.name} in a new home\">`:''}<p>${hm.thanks?`Thank you for ${hm.name}! `:''}${hm.line}</p><small>Love, the ${hm.fam} family</small></div>`; }",
    "function cardHTML(hm){ return `<div class=\"postcard\">${hm.thanks?`<b class=\"ty\">♥</b>`:''}${hm.img?`<img src=\"${hm.img}\" alt=\"\">`:''}<p style=\"text-align:center\">${FAM_SVG.replace('<svg ','<svg width=\"52\" height=\"40\" ')} ♥</p></div>`; }")
rep("openModal(`<h3>Happy Tails<span class=\"cnt\">♥ ${L.length}</span></h3>", "openModal(`<h3>💌<span class=\"cnt\">♥ ${L.length}</span></h3>")
rep("<img src=\"${o.hm.img}\" alt=\"${o.hm.name} at home\"><b>${o.hm.name}</b><span>with the ${o.hm.fam} family</span>", "<img src=\"${o.hm.img}\" alt=\"\">")

# ---------------- 3D signs ----------------
rep("textTex([['Welcome!','700 96px Fredoka, sans-serif','#4a3426',100]],512,192)", "textTex([['🐾 ♥ 🐾','700 96px sans-serif','#e0577f',104]],512,192)")
rep("textTex([['Whisker Meadow','700 80px Fredoka, sans-serif','#4a3426',86],['Cat Sanctuary','700 58px Nunito, sans-serif','#e0577f',160]],680,224)",
    "textTex([['🐈 ♥ 🐈','700 96px sans-serif','#e0577f',116]],680,224)")
# sleepy icon: no letters
rep("case 'zzz': x.fillStyle='#5b8def'; x.font='800 40px Nunito, sans-serif'; x.fillText('z',50,66); x.font='800 30px Nunito, sans-serif'; x.fillText('z',76,42); break;",
    "case 'zzz': x.fillStyle='#5b8def'; x.font='800 64px sans-serif'; x.fillText('☾',64,60); break;")

# ---------------- snapshot ----------------
rep("x.fillText('Whisker Meadow',48,610);", "x.font='700 52px sans-serif'; x.fillText('🐈 ♥',48,612);")
rep("x.fillText(`Score ${r.score}`,48,656);", "x.fillText(`🏆 ${r.score}`,48,660);")
rep("x.fillText(`${r.minutes} min${prev?` · last time ${prev.score}`:''}`,48,694);", "x.fillText(`⏱ ${r.minutes}${prev?` · ↩ ${prev.score}`:''}`,48,700);")
rep("const cells=[['Cats',r.cats],['Homes',W.homes.length],['Health',r.health],['Love',r.trust],['Ribbons',r.ribbons],['Badges',`${r.badges}/${ACH.length}`]];",
    "const cells=[['🐈',r.cats],['🏡',W.homes.length],['🌿',r.health],['♥',r.trust],['🎀',r.ribbons],['🏅',`${r.badges}/${ACH.length}`]];")
rep("const summary=`My Whisker Meadow: ${r.cats} cats, ${r.ribbons} ribbons, score ${r.score}.`;", "const summary=`🐈 ${r.cats} · 🎀 ${r.ribbons} · 🏆 ${r.score}`;")
rep("<h3>My meadow</h3><img id=\"snapimg\"", "<img id=\"snapimg\"")
rep("<button id=\"copySum\">Copy</button><button id=\"keepPlay\" style=\"background:var(--pink);color:#fff\">Keep playing</button>",
    "<button id=\"copySum\" aria-label=\"Copy\">📋</button><button id=\"keepPlay\" style=\"background:var(--pink);color:#fff\" aria-label=\"Keep playing\">▶</button>")
rep("b.textContent='Copied!'", "b.textContent='✓'")

# ---------------- help: a picture guide ----------------
cut("function openHelp(){", "$('#bHints').onclick=openHelp;", r"""function openHelp(){
  const row=(...a)=>`<div style="display:flex;align-items:center;justify-content:center;gap:10px;padding:10px 6px;border-bottom:2px solid var(--line);flex-wrap:wrap">${a.join('')}</div>`;
  const ic=(svg,w=30)=>svg.replace('<svg ',`<svg width="${w}" height="${w}" style="vertical-align:middle" `);
  const big=t=>`<span style="font:700 22px var(--display)">${t}</span>`;
  const eq=h=>h.replace('class="eq"','class="eq" style="display:flex;justify-content:center"').replace('viewBox="0 0 150 46"','viewBox="0 0 150 46" width="150" height="46"');
  openModal(`<div class="help" style="max-width:420px;margin:auto">
  <div class="hrow" style="justify-content:center"><span style="font-size:26px">👆</span><button id="hTog" aria-label="Hints on/off">${W.hints?'✓':'✗'}</button></div>
  ${row(ic(HOURGLASS,26),big('→'),hIco(H_HEART,30))}
  ${row(eq(BLINK_EQ))}
  ${row(eq(PAIR_EQ))}
  ${row(`<div class="eq eq3" style="display:flex;align-items:center;gap:6px">${SCRUFF_SVG}${big('+')}${BRUSH_ICON}${big('=')}${SHINE_ICON}</div>`)}
  ${row(`<div style="width:160px">${BELLY_TIP}</div>`)}
  ${row(`<div style="width:160px">${BUTT_TIP}</div>`)}
  ${row(`<div style="width:160px">${FLEA_TIP}</div>`)}
  ${row(ic(ICO_A),big('55'),ic(ICO_T),big('50'),ic(ICO_H),big('60'),big('→'),fairBadge(0,30))}
  ${row(ic(ICO_A),big('50'),ic(ICO_H),big('55'),big('→'),ic(STAY_SVG,30),FAM_SVG.replace('<svg ','<svg width="40" height="30" style="vertical-align:middle" '))}
  </div>`);
  $('#hTog').onclick=()=>{ W.hints=!W.hints; store.set('wm_hints',W.hints); $('#hTog').textContent=W.hints?'✓':'✗'; if(!W.hints)hideHint(); };
}
""")
open(P, 'w', encoding='utf-8').write(s); print('ok')
