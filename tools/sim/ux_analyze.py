"""Analyze persona play logs (tools/sim/out/ux_NNN.json) from the UX bot: timing consistency of lessons/hints,
overlaps between lessons, hints and modals, blocked taps (especially right after following a hint), time stuck,
wrong-tool time, and outcomes by persona. Usage: python tools/sim/ux_analyze.py [max_minutes]"""
import json, glob, sys, re, statistics as stx
from collections import defaultdict, Counter
LIM = float(sys.argv[1]) * 60 if len(sys.argv) > 1 else 1e9
runs = []
for f in sorted(glob.glob('tools/sim/out/ux_[0-9][0-9][0-9].json')):
    runs.append(json.load(open(f, encoding='utf-8')))
print(f'{len(runs)} sessions')
OWN = {'shop': {'shop', 'roof', 'helper', 'space'}, 'wand': {'wand', 'wand2'}, 'fair': {'show0', 'show'}, 'adopt': {'pick'}}
HAND = {'pet', 'blink', 'pair', 'adopt'}
def att(r): return r['cfg']['label'].split('-')[3]
def q(xs):
    if not xs: return '-'
    xs = sorted(xs); return f'{xs[0]:.0f} / {stx.median(xs):.0f} / {xs[-1]:.0f}'

first = defaultdict(dict)        # kind -> run index -> first game time
lessondur = defaultdict(list)    # lesson kind -> durations
multi = Counter(); hint_conf = Counter(); modal_in_lesson = Counter(); lesson_chain = Counter()
lockpans = Counter(); blocked = Counter(); blocked_after_hint = Counter(); wrongtool = defaultdict(list); integrity = Counter()
pause_d = []; per = defaultdict(lambda: defaultdict(list)); examples = defaultdict(list)
for i, r in enumerate(runs):
    L = [x for x in r['log'] if x[1] <= LIM]
    prev_wall = prev_game = -1; cur = None; cur_t = 0; prev_lessons = set(); lastbot = (None, -99); wt_t = None; paused_t = None
    nblk = 0; pend_lp = None
    for wall, gt, ev, d in L:
        if wall < prev_wall or gt < prev_game - 0.05: integrity['time went backwards'] += 1
        prev_wall, prev_game = wall, gt
        if ev == 'bot': lastbot = (d, gt)
        if ev == 'down' and 'LOCKPAN' in d: pend_lp = (gt, cur)
        if ev == 'up' and pend_lp:
            if 'moved' not in d: blocked[(pend_lp[1] or '?').split(' | ')[0]] += 1; nblk += 1
            else: lockpans[(pend_lp[1] or '?').split(' | ')[0]] += 1
            pend_lp = None
        if ev == 'down' and 'BLOCKED' in d:
            nblk += 1; st = cur.split(' | ')[0] if cur else '?'; blocked[st] += 1
            if lastbot[0] and lastbot[0].startswith('hint ') and gt - lastbot[1] < 1.5:
                k = f"hint {lastbot[0].split()[1]} during {st}"; blocked_after_hint[k] += 1
                if len(examples[k]) < 2: examples[k].append(f"{r['id']} t={gt}")
        if ev in ('toast', 'tooFast', 'stroke', 'skip', 'stuck', 'boterr'):
            if ev in ('stuck', 'boterr'): integrity[ev] += 1
            if ev == 'toast': first['toast ' + re.sub(r'[\d$+]+', '#', d)[:28]].setdefault(i, gt)
        if ev != 'state': continue
        parts = d.split(' | '); les = parts[0]; tool = parts[1][5:]; hint = parts[2][5:]; modal = parts[3][6:]; paused = len(parts) > 4 and parts[4] == 'paused'
        if paused and paused_t is None: paused_t = wall
        if not paused and paused_t is not None: pause_d.append(wall - paused_t); paused_t = None
        lset = set() if les in ('free', 'menu') else set(les.split(','))
        kinds = {x.split(':')[0] for x in lset}
        for x in lset: first['lesson ' + x].setdefault(i, gt)
        if hint != '-': first['hint ' + hint].setdefault(i, gt)
        if modal != '-': first['modal ' + modal].setdefault(i, gt)
        if len(lset) > 1: multi[les] += 1; examples['multi ' + les].append(f"{r['id']} t={gt}") if len(examples['multi ' + les]) < 2 else None
        for k in kinds:
            if hint != '-' and k in OWN and hint not in OWN[k]:
                hint_conf[f'hint {hint} shown under {k} lock'] += 1
                if len(examples[f'hc {hint} {k}']) < 2: examples[f'hc {hint} {k}'].append(f"{r['id']} t={gt}")
            if hint != '-' and k == 'tip':
                hint_conf[f'hint {hint} shown during tip {les}'] += 1
            if modal != '-' and k in ('pet', 'blink', 'pair', 'brush'): modal_in_lesson[f'{modal} over {k}'] += 1
        # lesson -> other lesson with no free moment between
        if prev_lessons and lset and not (prev_lessons & lset):
            lesson_chain[f"{','.join(sorted(prev_lessons))} -> {','.join(sorted(lset))}"] += 1
        # durations
        sig = ','.join(sorted(lset))
        if sig != cur:
            if cur: lessondur[cur].append(gt - cur_t)
            cur, cur_t = sig, gt
        # wrong tool while a hand lesson runs
        need = 'hand' if kinds & HAND else 'brush' if ('brush' in kinds and False) else None
        if need and tool != need:
            if wt_t is None: wt_t = (gt, sig)
        elif wt_t is not None: wrongtool[wt_t[1]].append(gt - wt_t[0]); wt_t = None
        prev_lessons = lset
    if cur: lessondur[cur].append(min(LIM, r['simT']) - cur_t)
    a = att(r); s = r['stat']
    per[a]['good'].append(s.get('good', 0)); per[a]['blocked'].append(nblk); per[a]['stars'].append(r['stars'])
    per[a]['tooFast'].append(sum(1 for x in L if x[2] == 'tooFast')); per[a]['skips'].append(sum(1 for x in L if x[2] == 'skip'))
    sp = r['cfg']['label'].split('-')[0]
    per['speed ' + sp]['tooFast'].append(sum(1 for x in L if x[2] == 'tooFast')); per['speed ' + sp]['good'].append(s.get('good', 0))
    od = r['cfg']['label'].split('-')[1]
    per['strokes ' + od]['good'].append(s.get('good', 0)); per['strokes ' + od]['rings'].append(sum(1 for x in L if x[2] == 'stroke' and 'ring' in x[3]))
    cm = r['cfg']['label'].split('-')[2]
    per[cm]['blocked'].append(nblk); per[cm]['good'].append(s.get('good', 0))

n = len(runs)
print('\n== Log integrity =='); print(dict(integrity) or 'clean: wall and game clocks monotonic, no stuck sessions, no bot errors')
if pause_d: print(f'meet-sheet pauses: {len(pause_d)}, wall seconds min/median/max {q(pause_d)}')
print('\n== First appearance (game s): min / median / max, and share of sessions ==')
rows = sorted(first.items(), key=lambda kv: stx.median(kv[1].values()))
for k, v in rows:
    if len(v) < max(3, n * 0.05): continue
    print(f'  {k:42s} {q(list(v.values())):>17s}   {100*len(v)/n:4.0f}%')
print('\n== Lessons/tips/forced steps active at the same moment ==')
for k, c in multi.most_common(): print(f'  {c:4d}  {k}   e.g. {examples["multi "+k]}')
print('\n== Hints shown while a different lesson holds the lock ==')
for k, c in hint_conf.most_common(): print(f'  {c:4d}  {k}')
print('\n== Modal open while an opening lesson runs ==')
for k, c in modal_in_lesson.most_common(): print(f'  {c:4d}  {k}')
print('\n== One lesson handing straight to another (no free moment between) ==')
for k, c in lesson_chain.most_common(15): print(f'  {c:4d}  {k}')
print('\n== Taps blocked by a lock (by state) ==')
for k, c in blocked.most_common(12): print(f'  {c:5d}  {k}')
print('\n== Player followed a pointing hint and the tap was BLOCKED ==')
for k, c in blocked_after_hint.most_common(): print(f'  {c:4d}  {k}   e.g. {examples[k]}')
print('\n== Time in each lesson state (game s): min / median / max, count ==')
for k, v in sorted(lessondur.items(), key=lambda kv: -stx.median(kv[1])):
    if k and len(v) >= 3: print(f'  {k:28s} {q(v):>17s}  n={len(v)}')
print('\n== Hand lesson running while holding another tool (s) ==')
for k, v in wrongtool.items(): print(f'  {k:28s} {q(v):>17s}  n={len(v)}')
print('\n== Families, strays, volunteers, goals (per session, within the time limit) ==')
fam = defaultdict(list); famfirst = []; adoptfirst = []
for r in runs:
    L = [x for x in r['log'] if x[1] <= LIM]
    ev = Counter(); fa = ad = None
    for wall, gt, e, d in L:
        if e == 'family':
            k = 'arrive (none ready)' if d.startswith('arrive') and 'none' in d else 'arrive (cat ready)' if d.startswith('arrive') else 'adopt' if d.startswith('adopt') else 'leave: ' + d[7:]
            ev[k] += 1
            if d.startswith('arrive') and fa is None: fa = gt
            if d.startswith('adopt') and ad is None: ad = gt
        elif e in ('stray', 'volunteer', 'goal', 'dzoom', 'lockTip'): ev[e + (' ' + d.split()[0] if e in ('stray', 'volunteer') else '')] += 1
    if fa is not None: famfirst.append(fa)
    if ad is not None: adoptfirst.append(ad)
    for k in ev: fam[k].append(ev[k])
for k, v in sorted(fam.items()):
    v = v + [0] * (n - len(v)); print(f'  {k:34s} mean {stx.mean(v):5.2f}  sessions with any: {sum(1 for x in v if x)}/{n}')
print(f'  first family arrival (game s): {q(famfirst)}  n={len(famfirst)}')
print(f'  first adoption (game s):       {q(adoptfirst)}  n={len(adoptfirst)}')

print('\n== By persona ==')
for a, d in sorted(per.items()):
    print(f'  {a:18s} ' + '  '.join(f'{k}={stx.mean(v):.1f}' for k, v in d.items()) + f'  (n={len(next(iter(d.values())))})')
