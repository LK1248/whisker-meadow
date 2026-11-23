"""Monetization & long-term model built on the sim runs. Produces charts + numbers for the report/deck.
All revenue figures are ILLUSTRATIVE: eCPMs, Poki's ad frequency and the revenue share are inputs, not facts."""
import json, pathlib, statistics as st
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = pathlib.Path(__file__).resolve().parents[2]
OUT = ROOT / 'tools/sim/out'; FIG = ROOT / 'docs/monetization'; FIG.mkdir(parents=True, exist_ok=True)
runs = {p.stem: json.loads(p.read_text()) for p in sorted(OUT.glob('*.json')) if not p.stem.endswith('_part')}
COL = {'casual': '#e0577f', 'engaged': '#5b9be6', 'optimizer': '#3f8f3d'}
plt.rcParams.update({'font.size': 11, 'axes.spines.top': False, 'axes.spines.right': False, 'figure.dpi': 150})
NUM = {}

def lvl_times(r):
    t = {1: 0}
    for e in r['events']:
        if e[1] == 'expand': t[e[2]] = e[0]
    return t
def arch(k): return k.split('_')[0]
base = {k: r for k, r in runs.items() if not r.get('ads') and 'adfam' not in k and 'smart' not in k}

# 1. progression: meadow level over time per run
fig, ax = plt.subplots(figsize=(8, 4.2))
for k, r in base.items():
    lt = lvl_times(r); xs, ys = [0], [1]
    for l in sorted(lt)[1:]: xs += [lt[l]/60, lt[l]/60]; ys += [ys[-1], l]
    xs.append(min(60, r['log'][-1]['t']/60)); ys.append(ys[-1])
    ax.plot(xs, ys, color=COL[arch(k)], alpha=.75, lw=2, label=arch(k).capitalize() if k.endswith('_1') else None)
ax.axvspan(15, 45, color='#f6c443', alpha=.12, label='Target session 15–45 min')
ax.set_xlim(0, 60); ax.set_xlabel('Minutes played'); ax.set_ylabel('Meadow level (1–8)'); ax.set_title('How fast players grow the sanctuary (sim, no ads)')
ax.legend(frameon=False, loc='lower right'); fig.tight_layout(); fig.savefig(FIG/'01_progression.png'); plt.close(fig)

# median time to each level per archetype
med = {}
for a in COL:
    med[a] = {}
    for l in range(2, 9):
        ts = [lvl_times(r).get(l) for k, r in base.items() if arch(k) == a]
        got = [t/60 for t in ts if t is not None and t <= 3600]
        med[a][l] = (round(st.median(got), 1) if got else None, f"{len(got)}/{len(ts)}")
NUM['median_level_minutes'] = med

# 2. what holds each expansion back
need = {2:(120,2,0),3:(300,3,0),4:(700,4,0),5:(1100,5,3),6:(1600,5,6),7:(2300,5,10),8:(3200,5,16)}
gate = {a: {l: {'money': 0, 'stars': 0, 'homes': 0} for l in range(2, 9)} for a in COL}
for k, r in base.items():
    lt = lvl_times(r); levels = sorted(lt)
    for a_, b_ in zip(levels, levels[1:]):
        for row in r['log']:
            if lt[a_] <= row['t'] < lt[b_]:
                n = need[b_]
                g = 'stars' if row['stars'] < n[1] else 'homes' if row['homes'] < n[2] else 'money' if row['money'] < n[0] else None
                if g: gate[arch(k)][b_][g] += 0.5
cnt = {a: sum(1 for k in base if arch(k) == a) for a in COL}
fig, axs = plt.subplots(1, 3, figsize=(11, 3.6), sharey=True)
for ax, a in zip(axs, COL):
    L = list(range(2, 9)); bot = [0]*7
    for g, c in (('stars', '#f6c443'), ('homes', '#e0577f'), ('money', '#5b9be6')):
        v = [gate[a][l][g]/cnt[a] for l in L]; ax.bar([f'L{l}' for l in L], v, bottom=bot, color=c, label=g.capitalize() if a == 'casual' else None); bot = [x+y for x, y in zip(bot, v)]
    ax.set_title(a.capitalize())
axs[0].set_ylabel('Avg minutes waiting'); axs[0].legend(frameon=False)
fig.suptitle('What each expansion waits on: stars early, adoptions late, almost never money'); fig.tight_layout(); fig.savefig(FIG/'02_gates.png'); plt.close(fig)
NUM['gate_minutes_avg'] = {a: {l: {g: round(v/cnt[a], 1) for g, v in gate[a][l].items()} for l in gate[a]} for a in COL}

# 3. cash on hand over time (log scale): money stops mattering
fig, ax = plt.subplots(figsize=(8, 4.2))
for k, r in base.items():
    xs = [row['t']/60 for row in r['log'] if row['t'] <= 3600]; ys = [max(1, row['money']) for row in r['log'] if row['t'] <= 3600]
    ax.plot(xs, ys, color=COL[arch(k)], alpha=.75, lw=2, label=arch(k).capitalize() if k.endswith('_1') else None)
ax.axhline(3200, color='#888', ls='--', lw=1); ax.text(1, 3600, 'priciest thing in the game: Grand sanctuary $3,200', color='#666', fontsize=9)
ax.set_yscale('log'); ax.set_xlabel('Minutes played'); ax.set_ylabel('Cash on hand ($, log)'); ax.set_title('Cash piles up after ~20 min (fair prizes snowball)')
ax.legend(frameon=False); fig.tight_layout(); fig.savefig(FIG/'03_cash.png'); plt.close(fig)
NUM['earned_60'] = {k: r['log'][min(len(r['log'])-1, 119)]['earned'] for k, r in base.items()}
NUM['fairs'] = {k: r['acts'].get('fair', 0) for k, r in base.items()}

# 4. rewarded-ad variants vs baselines
def lv_at(r, sec):
    lt = lvl_times(r); return max(l for l, t in lt.items() if t <= sec)
rows = []
for k, r in runs.items():
    rows.append((k, lv_at(r, 1800), lv_at(r, 2700), lv_at(r, 3600), min(r['log'][-1]['homes'], [x for x in r['log'] if x['t'] <= 3600][-1]['homes']), len(r.get('ads', []))))
NUM['variants'] = rows
fig, ax = plt.subplots(figsize=(8.5, 4))
groups = [('Casual', [k for k in base if arch(k) == 'casual'], ['casual_adfam5', 'casual_smart4']), ('Engaged', [k for k in base if arch(k) == 'engaged'], ['engaged_adfam3'])]
labels, vals, cols = [], [], []
for g, bl, vs in groups:
    labels.append(f'{g}\nno ads'); vals.append(st.mean(lv_at(runs[k], 3600) for k in bl)); cols.append('#bbb')
    for v in vs:
        nm = {'casual_adfam5': 'family ad\n(≤1 per 5 min)', 'casual_smart4': 'smart ad\n(≤1 per 4 min)', 'engaged_adfam3': 'family ad\n(≤1 per 3 min)'}[v]
        labels.append(f'{g}\n{nm}'); vals.append(lv_at(runs[v], 3600)); cols.append(COL[g.lower()])
ax.bar(labels, vals, color=cols); ax.set_ylim(0, 8.5); ax.set_ylabel('Meadow level at 60 min')
for i, v in enumerate(vals): ax.text(i, v+0.1, f'{v:.1f}', ha='center')
ax.set_title('Rewarded ads only help if they target the real bottleneck'); fig.tight_layout(); fig.savefig(FIG/'04_ad_variants.png'); plt.close(fig)

# 5. endless meadow: time per extra level with linear homes requirement
thru = {'casual': 0.17, 'engaged': 0.27, 'optimizer': 0.30}   # adoptions/min measured late game (homes per minute)
for k, r in base.items():
    lg = [x for x in r['log'] if x['t'] <= 3600]
    a, b = lg[len(lg)//2], lg[-1]
    thru.setdefault(arch(k)+'_obs', []).append((b['homes']-a['homes'])/((b['t']-a['t'])/60))
obs = {a: round(st.mean(thru[a+'_obs']), 3) for a in COL}; NUM['adoptions_per_min_second_half'] = obs
L = list(range(9, 21)); T = obs['engaged']
def need_accel(l):   # extrapolate today's homes needs (3,6,10,16): the step grows by ~2 each level
    seq = {5: 3, 6: 6, 7: 10, 8: 16}; step = 6
    for k in range(9, l+1): step += 2; seq[k] = seq[k-1] + step
    return seq[l] - seq[l-1]
curves = {
  "Today's pattern continued (need grows faster each acre)": [need_accel(l)/T for l in L],
  'Flat need: +8 adoptions per acre': [8/T for l in L],
  'Growing need, but more families visit as the meadow grows': [need_accel(l)/(T*(1+(l-8)/3)) for l in L],
  'Same, plus an optional "call a family" rewarded ad': [need_accel(l)/(T*(1+(l-8)/3)*1.6) for l in L]}
fig, ax = plt.subplots(figsize=(8.5, 4.4))
for (name, per), c, ls in zip(curves.items(), ('#e0577f', '#5b9be6', '#3f8f3d', '#3f8f3d'), ('-', '-', '-', '--')):
    cum, acc = [], 0
    for p in per: acc += p/60; cum.append(acc)
    ax.plot(L, cum, color=c, ls=ls, lw=2.2, label=name)
ax.set_xlabel("Meadow level beyond today's max (8)"); ax.set_ylabel('Extra hours of play (engaged player)')
ax.set_title('Endless expansion: a growing need with fixed family visits becomes a grind'); ax.legend(frameon=False, fontsize=9); fig.tight_layout(); fig.savefig(FIG/'05_endless.png'); plt.close(fig)
NUM['endless_cum_hours_to_L12_L16_L20'] = {n: [round(sum(p[:k])/60, 1) for k in (4, 8, 12)] for n, p in curves.items()}

# 6. illustrative ad revenue per 1,000 players (Poki ads only; no IAP on Poki)
# session-length mix (assumption): share of players whose session ends in each bucket, and bucket midpoint minutes
mix = [(0.40, 2), (0.30, 6), (0.18, 18), (0.08, 38), (0.04, 70)]
def opportunities(minutes, rewarded_per_hr, first_cb=4.0, cb_gap=4.0):
    cb = 0 if minutes < first_cb else 1 + int((minutes-first_cb)//cb_gap)          # commercial breaks offered at natural pauses; Poki may skip some
    rw = rewarded_per_hr*max(0, minutes-5)/60                                         # rewarded offers only after the first 5 minutes
    return cb, rw
scen = {'Commercial breaks only': 0, 'Light rewarded (gate offers, ~6/h)': 6, 'Heavier rewarded (~14/h)': 14}
ecpm = {'low': (1.0, 4.0), 'mid': (2.5, 8.0), 'high': (5.0, 15.0)}               # (commercial, rewarded) $ per 1000 impressions
fill_cb = 0.6                                                                        # share of our commercialBreak calls Poki actually fills
res = {}
for s_name, rph in scen.items():
    for e_name, (ec, er) in ecpm.items():
        cb = sum(p*opportunities(m, rph)[0] for p, m in mix)*1000*fill_cb
        rw = sum(p*opportunities(m, rph)[1] for p, m in mix)*1000*0.7              # 70% of offered rewarded ads actually watched
        res[(s_name, e_name)] = round((cb*ec + rw*er)/1000, 2)
NUM['revenue_per_1000_players_gross'] = {f'{a} | {b}': v for (a, b), v in res.items()}
fig, ax = plt.subplots(figsize=(8.5, 4))
xs = list(scen); w = 0.26
for i, (e_name, c) in enumerate(zip(ecpm, ('#c9d3de', '#5b9be6', '#3f8f3d'))):
    ax.bar([j+i*w for j in range(len(xs))], [res[(s, e_name)] for s in xs], w, color=c, label=f'{e_name} eCPM')
ax.set_xticks([j+w for j in range(len(xs))], [x.replace(' (', '\n(') for x in xs]); ax.set_ylabel('Gross ad $ per 1,000 players')
ax.set_title('Illustrative only: inputs are assumptions, not Poki figures'); ax.legend(frameon=False); fig.tight_layout(); fig.savefig(FIG/'06_revenue.png'); plt.close(fig)

(FIG/'numbers.json').write_text(json.dumps(NUM, indent=1, default=str))
print(json.dumps(NUM, indent=1, default=str)[:4000])
