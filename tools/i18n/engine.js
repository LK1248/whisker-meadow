/* ================= LANGUAGES ================= */
/* The game is written in English; T() swaps any English text for the chosen language as it reaches the screen
   (DOM text, a few attributes, canvas text). Cat and family names are left alone. */
const LANGS=['en','he','fr','ru','it','ko','ja'];
const LANG_NAMES={en:'English',he:'עברית',fr:'Français',ru:'Русский',it:'Italiano',ko:'한국어',ja:'日本語'};
const LANG=(()=>{ let l=null; try{ const m=location.hash.match(/lang=([a-z]{2})/); l=m?m[1]:localStorage.getItem('wm_lang'); }catch(e){} return LANGS.includes(l)?l:'en'; })();
const I18N=__I18N__, I18N_HTML=__I18N_HTML__;
const T=(()=>{ const id=s=>s; id.miss=new Set(); if(LANG==='en')return id;
  const li=LANGS.indexOf(LANG)-1, exact=new Map(), pats=[], html=new Map(), miss=new Set(), done=new Set(); let cache=new Map();
  const norm=s=>s.replace(/\s+/g,' ').trim();
  for(const k in I18N){ const v=I18N[k][li]; if(v==null||v==='')continue;
    if(/\{\d\}/.test(k)){ const re=new RegExp('^'+k.replace(/[.*+?^$()|[\]\\]/g,'\\$&').replace(/\{(\d)\}/g,'(?<g$1>[\\s\\S]+?)')+'$'); pats.push([re,v,k.replace(/\{\d\}/g,'').length]); }
    else { exact.set(k,v); done.add(v); } }
  pats.sort((a,b)=>b[2]-a[2]);
  for(const k in I18N_HTML){ const v=I18N_HTML[k][li]; if(v)html.set(norm(k),v); }
  const tr=s=>{ if(typeof s!=='string'||!/[A-Za-z]/.test(s))return s; let r=cache.get(s); if(r!==undefined)return r;
    const m=s.match(/^(\s*)([\s\S]*?)(\s*)$/), core=m[2]; if(done.has(core))return s; let v=exact.get(core);
    if(v===undefined) for(const [re,t] of pats){ const mm=core.match(re); if(mm){ v=t.replace(/\{(\d)\}/g,(_,i)=>tr(mm.groups['g'+i])); break; } }
    if(v===undefined){ miss.add(core); r=s; } else { r=m[1]+v+m[3]; done.add(v); }
    if(cache.size>4000)cache=new Map(); cache.set(s,r); return r; };
  tr.miss=miss;
  const ATTRS=['aria-label','title','alt','placeholder'];
  const skip=n=>{ const e=n.nodeType===1?n:n.parentElement; return !!(e&&(e.closest('[data-notr]')||e.closest('script,style'))); };
  const doText=n=>{ const v=n.nodeValue; if(!v||!/[A-Za-z]/.test(v)||skip(n))return; const t=tr(v); if(t!==v)n.nodeValue=t; };
  const doAttr=(e,a)=>{ const v=e.getAttribute(a); if(!v||!/[A-Za-z]/.test(v))return; const t=tr(v); if(t!==v)e.setAttribute(a,t); };
  const doEl=e=>{ for(const a of ATTRS)if(e.hasAttribute(a))doAttr(e,a);
    if((e.tagName==='LI'||e.tagName==='P')&&html.size){ const v=html.get(norm(e.innerHTML)); if(v!==undefined)e.innerHTML=v; } };
  const doNode=n=>{ if(n.nodeType===3){ doText(n); return; } if(n.nodeType!==1||skip(n))return; doEl(n);
    const w=document.createTreeWalker(n,5,{acceptNode:x=>x.nodeType===1&&(x.hasAttribute('data-notr')||x.tagName==='SCRIPT'||x.tagName==='STYLE')?2:1}); let x;
    while((x=w.nextNode())){ if(x.nodeType===3)doText(x); else doEl(x); } };
  new MutationObserver(ms=>{ for(const m of ms){ if(m.type==='characterData')doText(m.target); else if(m.type==='attributes')doAttr(m.target,m.attributeName); else for(const n of m.addedNodes)doNode(n); } })
    .observe(document.documentElement,{subtree:true,childList:true,characterData:true,attributes:true,attributeFilter:ATTRS});
  doNode(document.body); document.title=tr(document.title);
  const CP=CanvasRenderingContext2D.prototype; for(const f of ['fillText','strokeText','measureText']){ const o=CP[f]; CP[f]=function(t,...a){ let r=tr(t); if(LANG==='he'&&typeof r==='string'&&/[֐-׿]/.test(r))r='‫'+r+'‬'; return o.call(this,r,...a); }; }
  return tr; })();
(()=>{ const h=document.documentElement; h.lang=LANG; h.classList.add('lang-'+LANG); if(LANG==='he')h.classList.add('rtl');
  const fam={ko:'Jua',ja:'M+PLUS+Rounded+1c:wght@500;700;800'}[LANG];
  if(fam){ const l=document.createElement('link'); l.rel='stylesheet'; l.href='https://fonts.googleapis.com/css2?family='+fam+'&display=swap'; document.head.appendChild(l);
    const f=LANG==='ko'?"'Jua'":"'M PLUS Rounded 1c'"; h.style.setProperty('--display',`'Fredoka',${f},ui-rounded,'Nunito',system-ui,sans-serif`); h.style.setProperty('--body',`'Nunito',${f},system-ui,sans-serif`); }
  if(LANG==='he')h.style.setProperty('--body',"'Nunito','Fredoka',system-ui,sans-serif"); })();
const FLAGS={
  en:'<svg viewBox="0 0 60 40" preserveAspectRatio="xMidYMid slice"><rect width="60" height="40" fill="#012169"/><path d="M0 0L60 40M60 0L0 40" stroke="#fff" stroke-width="8"/><path d="M0 0L60 40M60 0L0 40" stroke="#c8102e" stroke-width="3"/><path d="M30 0v40M0 20h60" stroke="#fff" stroke-width="12"/><path d="M30 0v40M0 20h60" stroke="#c8102e" stroke-width="7"/></svg>',
  he:'<svg viewBox="0 0 60 40"><rect width="60" height="40" fill="#fff"/><path d="M0 4.5h60v6H0zM0 29.5h60v6H0z" fill="#0038b8"/><path d="M30 12.2l7 12.1H23zM30 27.8l7-12.1H23z" fill="none" stroke="#0038b8" stroke-width="1.6"/></svg>',
  fr:'<svg viewBox="0 0 60 40"><rect width="20" height="40" fill="#002654"/><rect x="20" width="20" height="40" fill="#fff"/><rect x="40" width="20" height="40" fill="#ce1126"/></svg>',
  ru:'<svg viewBox="0 0 60 40"><rect width="60" height="13.4" fill="#fff"/><rect y="13.3" width="60" height="13.4" fill="#0039a6"/><rect y="26.6" width="60" height="13.4" fill="#d52b1e"/></svg>',
  it:'<svg viewBox="0 0 60 40"><rect width="20" height="40" fill="#009246"/><rect x="20" width="20" height="40" fill="#fff"/><rect x="40" width="20" height="40" fill="#ce2b37"/></svg>',
  ko:'<svg viewBox="0 0 60 40"><rect width="60" height="40" fill="#fff"/><g transform="rotate(33.7 30 20)"><circle cx="30" cy="20" r="10" fill="#0047a0"/><path d="M20 20a10 10 0 0 1 20 0a5 5 0 0 1-10 0a5 5 0 0 0-10 0z" fill="#cd2e3a"/></g><g fill="#000"><g transform="translate(12 8) rotate(-56.3)"><rect x="-4" y="-3" width="8" height="1.5"/><rect x="-4" y="-.75" width="8" height="1.5"/><rect x="-4" y="1.5" width="8" height="1.5"/></g><g transform="translate(48 32) rotate(-56.3)"><rect x="-4" y="-3" width="8" height="1.5"/><rect x="-4" y="-.75" width="8" height="1.5"/><rect x="-4" y="1.5" width="8" height="1.5"/></g><g transform="translate(48 8) rotate(56.3)"><rect x="-4" y="-3" width="8" height="1.5"/><rect x="-4" y="-.75" width="8" height="1.5"/><rect x="-4" y="1.5" width="8" height="1.5"/></g><g transform="translate(12 32) rotate(56.3)"><rect x="-4" y="-3" width="8" height="1.5"/><rect x="-4" y="-.75" width="8" height="1.5"/><rect x="-4" y="1.5" width="8" height="1.5"/></g></g></svg>',
  ja:'<svg viewBox="0 0 60 40"><rect width="60" height="40" fill="#fff"/><circle cx="30" cy="20" r="12" fill="#bc002d"/></svg>'};
