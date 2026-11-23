"""Summarise sim runs in tools/sim/out: milestone times, walls, income curves, spend breakdown."""
import json, pathlib, statistics as st, sys
OUT = pathlib.Path(__file__).resolve().parent / 'out'
runs = {p.stem: json.loads(p.read_text()) for p in sorted(OUT.glob('*.json')) if not p.stem.endswith('_part')}

def lvl_times(r):
    t = {1: 0}
    for e in r['events']:
        if e[1] == 'expand': t[e[2]] = e[0]
    return t

def at(r, sec, key):
    best = None
    for row in r['log']:
        if row['t'] <= sec: best = row
    return best[key] if best else None

print(f"{'run':14} {'L2':>5} {'L3':>5} {'L4':>5} {'L5':>5} {'L6':>5} {'L7':>5} {'L8':>5} | {'homes60':>7} {'earn60':>7} {'cash60':>7} {'happy60':>7} | walls(min) money/stars/homes")
for k, r in runs.items():
    lt = lvl_times(r)
    cells = ' '.join(f"{(lt[l]/60 if l in lt else float('nan')):5.1f}" for l in range(2, 9))
    print(f"{k:14} {cells} | {at(r,3600,'homes'):7} {at(r,3600,'earned'):7} {at(r,3600,'money'):7} {at(r,3600,'happy'):7} | {r['wallMoney']/60:.0f}/{r['wallStars']/60:.0f}/{r['wallHomes']/60:.0f}")

# which gate held each level back: for each level transition, the dominant wall in that window
print('\nGate per level (minutes waiting on money / stars / homes before each expansion):')
for k, r in runs.items():
    lt = lvl_times(r); levels = sorted(lt)
    # recompute from logs
    rows = r['log']; out = []
    for a, b in zip(levels, levels[1:]):
        w = {'money': 0, 'stars': 0, 'homes': 0}
        for row in rows:
            if lt[a] <= row['t'] < lt[b]:
                need = {2:(120,2,0),3:(300,3,0),4:(700,4,0),5:(1100,5,3),6:(1600,5,6),7:(2300,5,10),8:(3200,5,16)}[b]
                if row['stars'] < need[1]: w['stars'] += .5
                elif row['homes'] < need[2]: w['homes'] += .5
                elif row['money'] < need[0]: w['money'] += .5
        out.append(f"L{b}:" + '/'.join(f"{w[x]:.0f}" for x in ('money', 'stars', 'homes')))
    print(f"  {k:14} " + '  '.join(out))

print('\nIncome $/min at minutes 5,10,20,30,45,60:')
for k, r in runs.items():
    print(f"  {k:14} " + ' '.join(f"{at(r, m*60, 'inc') or 0:6}" for m in (5, 10, 20, 30, 45, 60)))
print('\nSpend breakdown (first 60 min, $):')
for k, r in runs.items():
    sp = {}
    for t, i, c in r['buys']:
        if t <= 3600: sp[i] = sp.get(i, 0) + c
    sp['food'] = r['spend'].get('food', 0)
    print(f"  {k:14} " + ', '.join(f"{i}:{v}" for i, v in sorted(sp.items(), key=lambda x: -x[1])))
print('\nActions:')
for k, r in runs.items(): print(f"  {k:14} {r['acts']}")
print('\nFinal:')
for k, r in runs.items(): print(f"  {k:14} {json.dumps({x: r['final'][x] for x in ('homes','rescues','kittens','ribbons','found','runs','showTier','helpers','cats')})}")

print('\nRewarded-ad usage in variant runs:')
for k, r in runs.items():
    if r.get('ads'):
        kinds = {}
        for t, kd in r['ads']: kinds[kd] = kinds.get(kd, 0) + 1
        print(f"  {k:16} ads={len(r['ads'])} {kinds}  (+{len(r['ads'])*30/60:.0f} min of ad watching at 30 s each)")
