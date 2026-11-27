"""v188: languages. English, Hebrew, French, Russian, Italian, Korean, Japanese.
A flag button at the top left of the title screen opens a language picker; picking one saves it and reloads.
Text is swapped as it reaches the screen (tools/i18n/engine.js), from the tables in tools/i18n/s_*.py."""
import sys, os, re, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'i18n'))
from s_ui import S, BASES, PATS, SOLID_JA, EXTRA
from s_help import H
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count: sys.exit(f'match count {n} != {count} for: {old[:80]}')
    s = s.replace(old, new)

LG = ['he', 'fr', 'ru', 'it', 'ko', 'ja']
D = dict(S); D.update(EXTRA)
EN_B = ['Ginger', 'Black', 'Grey', 'Cream', 'White', 'Lilac', 'Golden']
EN_P = ['', ' tabby', ' tuxedo', ' socks']
for bi, b in enumerate(EN_B):
    for pi, p in enumerate(EN_P):
        row = []
        for l in LG:
            base = SOLID_JA[bi] if (l == 'ja' and pi == 0) else BASES[l][bi]
            v = PATS[l][pi].replace('{b}', base)
            if l == 'ja' and pi == 1 and b == 'Grey': v = 'サバトラ'
            if l == 'ja' and pi == 1 and b == 'Ginger': v = '茶トラ'
            row.append(v)
        D[b + p] = tuple(row)
for k, v in D.items():
    if len(v) != 6: sys.exit('bad row ' + k)

# help paragraphs, keyed by their English inner HTML
a = s.index('function openHelp(){'); b = s.index("$('#hDay').onclick", a)
items = re.findall(r'<(li|p)>(.*?)</\1>', s[a:b])
if len(items) != len(H): sys.exit(f'help items {len(items)} != translations {len(H)}')
HT = {x: list(t) for (_, x), t in zip(items, H)}

eng = open(os.path.join(os.path.dirname(__file__), 'i18n', 'engine.js'), encoding='utf-8').read()
eng = eng.replace('__I18N__', json.dumps({k: list(v) for k, v in D.items()}, ensure_ascii=False)).replace('__I18N_HTML__', json.dumps(HT, ensure_ascii=False))
if '</script' in eng: sys.exit('script close in data')
rep("(()=>{\n'use strict';\n", "(()=>{\n'use strict';\n" + eng)

# flag button + picker on the title screen
rep("const musT={b:$('#bMusic')};",
    "(()=>{ const st=$('#start'), b=document.createElement('button'); b.id='bLang'; b.className='hbtn pill icon'; b.dataset.notr=''; b.setAttribute('aria-label',LANG_NAMES[LANG]); b.innerHTML=FLAGS[LANG]; st.appendChild(b);\n"
    "  b.onclick=()=>{ if($('#langPick'))return; const o=document.createElement('div'); o.id='langPick'; o.dataset.notr='';\n"
    "    o.innerHTML=`<div class=\"lp\">${LANGS.map(l=>`<button data-l=\"${l}\" class=\"${l===LANG?'on':''}\" lang=\"${l}\"><span class=\"fl\">${FLAGS[l]}</span><span>${LANG_NAMES[l]}</span></button>`).join('')}</div>`;\n"
    "    o.onclick=e=>{ const t=e.target.closest('[data-l]'); if(!t||t.dataset.l===LANG){ o.remove(); return; } const l=t.dataset.l; try{ localStorage.setItem('wm_lang',l); }catch(err){} location.hash='lang='+l; location.reload(); };\n"
    "    st.appendChild(o); }; })();\n"
    "const musT={b:$('#bMusic')};")
rep("#start .new{",
    "#bLang{position:absolute;top:calc(10px + env(safe-area-inset-top,0px));left:calc(10px + env(safe-area-inset-left,0px));padding:0;display:grid;place-items:center}"
    "#bLang svg{width:30px;height:20px;border-radius:4px;box-shadow:0 0 0 1.5px rgba(74,52,38,.18);display:block}"
    "#langPick{position:absolute;inset:0;z-index:3;display:grid;place-items:center;background:rgba(74,52,38,.32);padding:16px}"
    "#langPick .lp{background:var(--cream);border-radius:28px;padding:16px;display:grid;grid-template-columns:1fr 1fr;gap:10px;width:min(360px,100%);box-shadow:0 20px 60px rgba(74,52,38,.3)}"
    "#langPick button{display:flex;align-items:center;gap:10px;min-height:54px;padding:0 12px;border-radius:16px;background:#fff;font:700 17px 'Nunito',system-ui,sans-serif;color:var(--ink);box-shadow:0 3px 0 rgba(74,52,38,.1)}"
    "#langPick button:first-child{grid-column:1/-1;justify-content:center}"
    "#langPick button.on{box-shadow:0 0 0 3px var(--pink)}"
    "html.rtl *{unicode-bidi:plaintext}html.rtl svg *{unicode-bidi:normal}"
    "html.rtl #start .card,html.rtl #mbox,html.rtl #family,html.rtl #meet .sheet,html.rtl #toasts,html.rtl #tag{direction:rtl}"
    "html.rtl .help ul{padding-left:0;padding-right:18px}"
    "#langPick .fl svg{width:36px;height:24px;border-radius:5px;display:block;box-shadow:0 0 0 1px rgba(0,0,0,.14)}\n#start .new{")
# expose the miss list for testing
rep("window.__wm={", "window.__wm={i18nMiss:T.miss,LANG,")
open(P, 'w', encoding='utf-8').write(s)
print('v188 applied', len(D), 'strings', len(HT), 'help')
