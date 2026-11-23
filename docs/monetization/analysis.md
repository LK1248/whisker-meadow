# Whisker Meadow: economy and monetization analysis

*Overnight analysis, 2026-11-23. The base game (`whisker-meadow.html`) was not changed. Every number below comes from a copy of the game driven by a scripted player (`tools/sim/`) or from the model in `tools/sim/model.py`.*

## 1. How the numbers were made

- `tools/sim/build_sim.py` copies the real game into `tools/sim/sim.html`. The copy uses its own save key, turns off rendering, and injects `tools/sim/bot.js`.
- The bot plays the real game logic at high speed. It feeds, scoops, pets, brushes, plays, enters fairs, shops, offers cats to families and searches for runaways.
- There are three player types:

  | Type | Seconds between actions | Time spent just watching | Fair entries | Laser toy | Helpers |
  |---|---|---|---|---|---|
  | Casual | 5.0 | 50% | sometimes | no | 1 |
  | Engaged | 2.6 | 30% | often | yes | up to 3 |
  | Optimizer | 1.6 | 10% | always | yes | up to 8 |

- Runs: 3 casual, 4 engaged (one 120 min), 2 optimizer (one 90 min), plus 3 "what if" runs with rewarded ads.
- Limits: the bot skips the tutorial, never makes mistakes with the controls, and a real player's attention is messier. Treat the numbers as a shape, not as exact minutes.

## 2. Pacing today

There is no target session length here: longer play is better. The aim is to understand how monetization, playtime and the player's experience affect each other. (A rough guess was that the current mechanics hold a typical player for 15–45 minutes before returns start to diminish. Nothing has measured that, so it is only a starting point.)

Median minutes to reach each meadow level (no ads):

| Player | L2 | L3 | L4 | L5 | L6 | L7 | L8 |
|---|---|---|---|---|---|---|---|
| Casual | 3.4 | 7.3 | 14.8 | 30.3 | 38.4 | 48.9 (1 of 3 runs) | not reached in 60 min |
| Engaged | 2.9 | 6.2 | 10.6 | 16.9 | 33.2 | 42.5 | 57.8 (1 of 4 runs) |
| Optimizer | 2.1 | 5.1 | 8.5 | 16.5 | 24.0 | 37.8 | 59.1 |

A new room every 3–10 minutes early on, then every 8–15 minutes. The pace itself feels steady. The problem is that it **stops**: an engaged player has unlocked everything after about an hour, and money stops mattering well before that (section 4). That is where returns diminish, and it is the first thing to fix if the goal is longer play. Costs and timings are unchanged for now, as asked.

## 3. What actually holds players back

Minutes spent waiting on each gate before each expansion:

- **Stars** gate levels 2–5 (2–9 minutes each).
- **Homes** (adoptions) gate levels 6–8 (5–16 minutes each).
- **Money almost never gates.** Only casual players wait on it a little around L5–L6.

Adoptions per minute in the second half hour: casual 0.15, engaged 0.25, optimizer 0.32. Families are the slow, "out of your hands" part of the late game.

## 4. Money snowballs and has nowhere to go

- Money earned in 60 minutes: casual ~9–10k, engaged 25–59k, optimizer ~140–149k.
- All expansions together cost $9,320. Engaged and optimizer players end the hour with many times that.
- Fair entries dominate income. The optimizer entered 1,255 fairs in an hour. Prize tiers rise with wins, so fairs grow faster than everything else.
- **There is no late-game money sink.** Once rooms are bought, money stops meaning anything.

Implication: selling money (or "gift" ads that give money) is worth almost nothing to most players, and would only matter to casual players for a few minutes.

## 5. Rewarded ads: only the right lever helps

| Run | Rewarded ads | Effect |
|---|---|---|
| Engaged + "call a family now" (≤1 per 3 min) | 17 | L6 at 20.7 min instead of ~33; L8 at 45.4 instead of 57.8; 19 homes instead of 9–17 |
| Casual + "call a family now" (≤1 per 5 min) | 8 | More homes (13) but **slower** levels (L4 at 28.9, L6 at 55.6). Adoptions shrink the cat count, which shrinks donations, so money became the gate. |
| Casual + "smart" offer (≤1 per 4 min) | 14 (9 gifts, 3 rescues, 2 families) | L6 at 40.6, L7 at 52.7, 13 homes: a modest gain |

Lessons:

1. A rewarded offer should target **whatever currently blocks the next room** (stars → a rescue arrives; homes → a family comes; money → a small donation). A single fixed lever can backfire.
2. The strongest offer is "a family visits now". It speeds up the slow part without breaking anything, because the cat still needs trust and health first.
3. Gains are real but not huge (about 10–15 minutes saved per hour). That is the right size: helpful, not "pay to escape a grind".

## 6. Long-term players: endless expansion

Today the meadow ends at level 8 (52 cats). Regular players will run out of goals. I modelled extra "acres" beyond L8 under four designs (engaged player, cumulative extra hours):

| Design | to L12 | to L16 | to L20 |
|---|---|---|---|
| Keep today's accelerating home requirement | 3.0 h | 8.1 h | 15.4 h |
| Flat +8 homes per acre | 2.2 h | 4.3 h | 6.5 h |
| Growing requirement, but more families visit as the meadow grows | 1.6 h | 3.3 h | 4.9 h |
| Same, plus a "call a family" rewarded ad | 1.0 h | 2.0 h | 3.0 h |

The accelerating curve turns into a hopeless grind by L14–L16. A linear requirement, with family visits scaling with meadow size, keeps each new acre at roughly 15–25 minutes forever. The rewarded ad then feels like a shortcut, not an escape hatch.

## 7. How monetization, playtime and experience pull on each other

- **Speed-up ads and playtime work against each other while the game has an end.** With only 8 levels, a "call a family now" ad gets an engaged player to the last room about 12 minutes sooner, so they run out of goals sooner too. Every speed-up shortens the game.
- **With endless acres they stop working against each other.** If there is always another acre, saving 15 minutes on one acre just moves the player on to the next. Playtime stays, ad revenue goes up, and the ad feels like a kindness instead of a toll.
- **Commercial breaks cost experience directly.** Every break interrupts a calm game. Placed at natural pauses they cost little; placed mid-petting they hurt the game's main feeling. Poki sets how often they play, so the game's job is to offer good moments, not more moments.
- **Rewarded ads that fix a felt problem improve the experience.** Waiting for a family while a cat is ready is the most passive moment in the game. An optional "call a family" ad turns that wait into a choice. An ad that only gives money fixes nothing, because money isn't scarce.
- **What gets players to come back is goals, not speed.** Returning players need something new: more acres, decor to spend money on, a collection to complete (like the card wall), and events. Each of these adds playtime without adding ads, and gives more natural moments for the ads that exist.
- **Caveat:** the bot doesn't get bored. Real players may quit at a wall long before the bot does, so the walls in section 3 matter more for real players than the minutes suggest. Real Poki data (average playtime, return rate) is the only way to see where interest actually drops.

## 8. Poki rules that shape all of this

- No in-app purchases, no currency or "remove ads" purchases. Only Poki's own ads.
- The game must not run its own ad timers. It calls `commercialBreak()` at natural pauses and Poki decides whether an ad actually plays.
- Rewarded breaks (`rewardedBreak()`) must be clearly announced first, never give a double reward, and give no reward if the ad did not play.
- Call `gameplayStop()` before a break and `gameplayStart()` after.

Sources: [Poki HTML5 SDK](https://sdk.poki.com/html5.html), [new requirements](https://sdk.poki.com/new-requirements), [monetization guide](https://developers.poki.com/guide/monetization), [SDK docs](https://sdk.poki.com/sdk-documentation.html).

## 9. Illustrative revenue per 1,000 players

**These are assumptions, not Poki data.** Poki does not publish its revenue share or eCPMs.

- Session mix: 40% leave at ~2 min, 30% at ~6, 18% at ~18, 8% at ~38, 4% at ~70.
- Commercial breaks: first at 4 min, then every 4 min, 60% fill.
- Rewarded offers: only after 5 min, 70% of offers watched.
- eCPM (commercial / rewarded): low $1 / $4, mid $2.5 / $8, high $5 / $15.

| Scenario | Low | Mid | High |
|---|---|---|---|
| Commercial breaks only | $1.45 | $3.63 | $7.26 |
| Light rewarded (~6 per hour) | $3.66 | $8.04 | $15.53 |
| Heavier rewarded (~14 per hour) | $6.60 | $13.93 | $26.57 |

Rewarded offers roughly double to quadruple revenue, and they come mostly from the players who stay longest. Those are the same players who need a reason to keep going, so retention and revenue point the same way.

## 10. Recommendations

**Keep as is**
- Current costs and timings for L1–L8 for now (the issue is that progression ends, not its pace).
- No money for adoptions (keeps the game from feeling like selling cats).

**Ads, in a way that does not break the game**
1. Commercial breaks only at natural pauses: after closing an adoption postcard, after an expansion, when coming back from the shop. Never in the first 4–5 minutes.
2. Rewarded offers tied to game moments, never timers, and always optional:
   - "A family is on the way" when a ready cat is waiting and homes are the gate.
   - "A stray needs rescue" when stars are the gate.
   - "Welcome back: double donations for a while" for returning players.
   - Possibly "the family loves this cat" (guaranteed match) once per visit.
3. Never put a reward behind something players need to care for cats (food, health). That would feel like paying to stop suffering.

**Long-term retention**
4. Endless acres after L8 with a linear home requirement and more family visits as the meadow grows.
5. Money sinks for rich players: cosmetics, decor, themed areas, special beds. Nothing that gates progress.
6. "Sister sanctuaries" as a prestige option: start a new meadow, keep your collection and album, get a permanent reputation bonus.
7. Small offline accrual (donations while away, capped) and a welcome-back moment.
8. Seasonal events (winter coats, spring kittens at the gate) to bring players back.

**Balance notes for later (not urgent)**
- Fair income snowballs; consider a cooldown per cat or smaller prizes at high tiers.
- Casual players' cats sit at 40–50 happiness because they get less attention. Fine, but helpers could do a bit more.
- A hungry cat that is being petted never leaves to eat. A real player could starve a cat by accident.

## 11. Files

- Charts: `docs/monetization/01_progression.png` to `06_revenue.png`; raw figures in `numbers.json`.
- Presentation: `docs/monetization/Whisker-Meadow-Monetization.pptx` (opens in Google Slides).
- Simulator: `tools/sim/` (`build_sim.py`, `bot.js`, `receiver.py`, `analyze.py`, `model.py`, run data in `out/`).
