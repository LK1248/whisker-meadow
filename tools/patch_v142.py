"""v142: one place for progress.
- The top bar no longer shows the Stars and Ribbons chips; the star button opens the Sanctuary window, which shows
  stars (with a bar to the next star) and ribbons at the top.
- The star button shows the star count in a small bubble and a gold ring that fills toward the next star.
- Badge and goal medals are cat faces (bronze / silver / gold), not stars; badges not earned yet show a faint cat.
- Music leaves the top bar (it stays on the title screen); its On/Off switch is at the bottom of the Sanctuary
  window."""
import sys
P = 'whisker-meadow.html'
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count: sys.exit(f'match count {n} != {count} for: {old[:80]}')
    s = s.replace(old, new)

# top bar: hide ribbons + stars chips (hud() still writes to them)
rep('<div class="chip pill" title="Ribbons">', '<div class="chip pill" title="Ribbons" hidden>')
rep('<div class="chip pill" title="Sanctuary stars">', '<div class="chip pill" title="Sanctuary stars" hidden>')
# star button: round, count bubble, progress ring
rep('<button class="hbtn pill" id="bBadges" aria-label="Badges">', '<button class="hbtn pill icon" id="bBadges" aria-label="Sanctuary">')
rep('<span class="lbl">Badges</span></button>', '<span class="lbl">Badges</span><b class="sn" id="bStarN">1</b></button>')
rep(".hbtn .lbl{display:none}",
    ".hbtn .lbl{display:none}#bBadges{position:relative;overflow:visible}#bBadges::after{content:'';position:absolute;inset:-5px;border-radius:50%;pointer-events:none;"
    "background:conic-gradient(#f6c443 calc(var(--sp,0)*1turn),rgba(160,130,90,.28) 0);-webkit-mask:radial-gradient(circle,transparent 22.5px,#000 23.5px);mask:radial-gradient(circle,transparent 22.5px,#000 23.5px)}"
    "#bBadges .sn{position:absolute;right:-5px;bottom:-5px;min-width:19px;height:19px;padding:0 4px;box-sizing:border-box;border-radius:10px;background:var(--pink);color:#fff;font:800 11px/19px var(--body);text-align:center;box-shadow:0 0 0 2px var(--cream)}"
    ".cf{width:64%;height:64%;display:block}.gm .cf{width:15px;height:15px;margin:2.5px auto 0}.badge-i:not(.t1):not(.t2):not(.t3) .cf{opacity:.45}"
    ".sstat{display:flex;gap:10px;align-items:center;margin:-2px 0 12px;font:700 14px var(--body);color:var(--muted)}.sstat svg{width:20px;height:20px;vertical-align:-5px}.sstat .bar{flex:1;height:10px;border-radius:5px;background:#efe5d8;overflow:hidden}.sstat .bar i{display:block;height:100%;background:#f6c443;border-radius:5px}")
rep("$('#hStars').textContent=W.stars;",
    "$('#hStars').textContent=W.stars; { const st=W.stars, a=STAR_AT[st]||0, nx=STAR_AT[st+1]; $('#bBadges').style.setProperty('--sp',nx?clamp((starPts()-a)/(nx-a),0,1):1); $('#bStarN').textContent=st; }")
# cat-face medals
rep("function openBadges(tab='badges'){",
    "const CATF='<svg class=\"cf\" viewBox=\"0 0 24 24\"><path d=\"M3.5 3.5l5 4.2h7l5-4.2.6 9.3a9.1 8 0 0 1-18.2 0z\" fill=\"currentColor\"/><circle cx=\"8.7\" cy=\"13\" r=\"1.5\" fill=\"rgba(0,0,0,.4)\"/><circle cx=\"15.3\" cy=\"13\" r=\"1.5\" fill=\"rgba(0,0,0,.4)\"/><path d=\"M11 16.2h2l-1 1.1z\" fill=\"rgba(0,0,0,.4)\"/></svg>';\n"
    "function openBadges(tab='badges'){")
rep("<div class=\"medal\">${t?'★':'?'}</div>", "<div class=\"medal\">${CATF}</div>")
rep("<i class=\"gm t${t}\">${t?'★':''}</i>", "<i class=\"gm t${t}\">${t?CATF:''}</i>")
# window header stats + music row
rep("openModal(`<h3>Sanctuary ${'★'.repeat(W.stars)}</h3>${tabs}",
    "const RIB='<svg viewBox=\"0 0 24 24\"><path d=\"M8 13l-3 9 4-2 2 3 2-8zM16 13l3 9-4-2-2 3-2-8z\" fill=\"#5b8def\"/><circle cx=\"12\" cy=\"9\" r=\"6.5\" fill=\"#ffcf3f\" stroke=\"#e0a400\" stroke-width=\"1.5\"/></svg>', sa=STAR_AT[W.stars]||0, sn=STAR_AT[W.stars+1], sp=sn?clamp((starPts()-sa)/(sn-sa),0,1):1;\n"
    "  openModal(`<h3>Sanctuary ${'★'.repeat(W.stars)}</h3><div class=\"sstat\"><span>${W.stars} / 5</span><i class=\"bar\"><i style=\"width:${Math.round(sp*100)}%\"></i></i><span>${RIB} ${W.ribbons}</span></div>${tabs}")
rep("${body}`);\n  document.querySelectorAll('[data-tab]').forEach(b=>b.onclick=()=>openBadges(b.dataset.tab));",
    "${body}<div class=\"help\" style=\"margin-top:14px\"><div class=\"hrow\"><span>Music</span><button id=\"sMus\">${Snd.musicOn?'On':'Off'}</button></div></div>`);\n"
    "  $('#sMus').onclick=()=>{ Snd.toggleMusic(); $('#sMus').textContent=Snd.musicOn?'On':'Off'; $('#bMusic').classList.toggle('off',!Snd.musicOn); };\n"
    "  document.querySelectorAll('[data-tab]').forEach(b=>b.onclick=()=>openBadges(b.dataset.tab));")
# music button: title screen only
rep("musT.b.classList.remove('ontitle'); musT.home.insertBefore(musT.b,musT.next); }",
    "musT.b.classList.remove('ontitle'); musT.home.insertBefore(musT.b,musT.next); musT.b.hidden=true; }")
rep("toast(`★ ${n} · ${TIER_N[t", "toast(`<span class=\"tc\">${CATF}</span>${n} · ${TIER_N[t")
rep(".cf{width:64%;height:64%;display:block}", ".cf{width:64%;height:64%;display:block}.toast .tc .cf{display:inline-block;width:1.15em;height:1.15em;vertical-align:-.2em;margin-right:5px;color:#e1a06a}")
open(P, 'w', encoding='utf-8').write(s)
print('v142 applied')
