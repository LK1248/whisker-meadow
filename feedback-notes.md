# Whisker Meadow: feedback for the next pass

Round 1 feedback on v1 (2026-11-21). Not built yet.

## Mobile first (applies to everything below)
- Design every interaction for one finger first, then map it to the mouse. Never rely on right-click, hover, mouse wheel or keyboard.
- Touch vocabulary to use: **tap**, **drag**, **press-and-hold**, **flick/swipe** (fast release), **two-finger pinch** (zoom only).
- So the wand's "click to toss" becomes a **flick**, and "raise the wand" becomes **drag upward / hold**. Picking up a cat is press-and-hold with a visible fill ring.
- Hover-only feedback (cursor changes, cats looking at the cursor) needs a touch version, e.g. cats look at the last touch point.
- Big touch targets (44px+), controls in thumb reach (bottom of screen), portrait layout as the default.
- Camera: one-finger drag on empty grass pans, pinch zooms. No rotation needed, or a two-finger twist at most.
- Performance budget sized for mid-range phones (fewer meshes per cat, cap the shadows).

## Stats
- Too many stat bars (there are 7 now). Cut to 3: **Health, Trust, Affection**. Fold everything else into them:
  - Health: food, clean litter, play, grooming, space.
  - Trust: petting the right spots, feeding, gentle handling. Goes down from belly scratches and tail grabs.
  - Affection: petting, play, bonding with you.

## Bugs
- **Picking up a cat didn't work** for the user. Likely cause: the 450 ms hold gets cancelled by the small mouse jitter that counts as "moved" (7 px), or the hold check never runs. Fix it and add a visible "hold" progress ring.
- **Jingle ball is lifeless.** Cats walk right through it and it doesn't move. Fix: any cat (or the helper) that bumps the ball pushes it, so it rolls and jingles. Cats should also play with it on purpose more often and visibly: stalk, bat it with a paw, chase it, and sometimes hold it and kick it with their back legs.
- **Cats overlap each other.** Separation is too weak or gets skipped in some states. Add proper collision so bodies never pass through each other, including with items.

## Tutorials and text
- Too many words. Younger players won't read. Replace sentences with **signs**: icons, an animated hand or arrow pointing at the target, a short label of 1–3 words at most.
- Feeding and the litter box need their own small tutorials (a pointing hand at the bowl or box, with a pulse).
- Friendship should be a **big heart between two cats** when they're near each other, not a text tip.
- Generally: show it, don't tell it. Same for toasts (icon + number, e.g. a ribbon + "$90").

## Feather wand
- Feels clunky because it just follows the mouse.
- Ideas: it sways and waves on its own; click to flick or toss it; hold and drag up to **raise it so cats jump up for it**; flick to make it flutter.

## Picking up cats
- The current carry doesn't look realistic (the whole cat just floats up level).
- **Decision: follow vet guidance, no scruffing for any cat (kittens included).** The sanctuary should model good handling.
- Lift the way vets recommend: **one hand under the chest behind the front legs, the other supporting the hind legs and bottom**. Show two soft cartoon hands cradling the cat, held close and level.
- **Relaxed, trusting cat:** melts into the hold. Body soft, eyes half-closed, maybe a purr or a slow blink, tail hanging loosely.
- **Low trust starts a timer** while held. Hold too long and the cat goes stiff, then **wiggles**, harder and harder, and finally **hops free**: it lands on its feet and scampers off, with a small trust penalty. Never a drop or a fall.
- High-trust cats are happy to be carried much longer (or indefinitely).
- Show the timer visually, not as a number (growing wiggles, flattening ears, a swishing tail).
- Put the cat down gently: it's lowered to the grass and walks off normally.
- Tip for players (shown as a picture, not text): "support the chest and the back legs".

## Hand cursor
- Replace the mouse pointer with a **cartoon hand** that changes with the action: open palm (idle), stroking fingers (petting), scratching fingers (chin/ears), cupped hands (carrying), holding the brush or wand when that tool is active.
- Mobile: there's no cursor, so the hand **appears under the finger while touching** (drawn a bit above the fingertip so the finger doesn't hide it) and fades out on release.
- The cat reacts to the hand: headbutts it, bats at it, sniffs it.
- **When a cat scratches:** the user floated a small drop of blood, but wasn't sure it suits Poki. Safer for kids: the hand jerks back, cartoon red scratch lines on the back of the hand, then a **band-aid** appears on it for a while (cute, and a lasting reminder). Start without blood.

## Petting should feel alive
- Cats react and interact while being petted. Right now they mostly just stand there and purr.
- Playful moments: batting at your hand, a little nibble, kneading, a tail curling around the cursor.
- **Offer a belly:** roll onto their side to invite a belly rub. Good trust means the offer is real; low trust means it's a trap.
- **Headbutts:** they bump into your hand or cursor when affection is high.
- **Abrupt walk-offs:** when trust or affection is low, they cut a petting session short and stalk off (tail flick, maybe a glance back).
- Overall: more back-and-forth between you and the cat, less one-way stroking.
- **Petting rhythm (replaces "more strokes = more stats").** There's an ideal pace, starting around **1 slow stroke every ~3 seconds** (tune in playtests; each cat could have its own preferred pace).
  - On rhythm: Trust and Affection rise, and the purr gets louder.
  - Off rhythm (too slow, or erratic): no gain.
  - Too fast / frantic: the cat gets overstimulated. **High trust:** it walks or trots away. **Low trust:** it snaps or nips at the hand (scratch/band-aid reaction from the Hand cursor section) and loses some trust.
  - Warning signs before it boils over, so players can learn: tail starts twitching, ears turn sideways, skin ripples. These are real cat overstimulation cues and teach good habits.
  - Show the rhythm without words: e.g. the purr pulses or a soft glow on the cat beats at the ideal pace, and the stroke "lands" with a little sparkle when it's on time.

## Helper
- Today the helper is invisible and only refills bowls and scoops litter.
- Make the helper a **visible person** (same cartoon style) who walks around the enclosure.
- They still do chores (walk to the bowl to fill it, walk to the litter box to scoop it), and now they also **care for the cats**: periodically walk up to a cat, **kneel down**, pet it or play with it briefly (a little wand or ball), then stand up and move on.
- Their care gives small gains in Affection, Trust and Health, smaller than what the player gets, so the player's own attention still matters most.
- Shy, low-trust cats may walk away from the helper too, which shows trust is earned.
- Later: more helpers for bigger meadows, each one visibly busy.

## New shop items
- **Laser pointer:** a red dot the cats sprint to, very fast, with frantic pouncing.
- **Shelter / overhang / gazebo:** covers part of the meadow, and cats run under it when it rains.

## Keep
- Rain looks good.
- More notes to come from the user.

---
# Round 2 (built in v2, 2026-11-21)
Everything above was built in v2, plus: birds and butterflies (cats stalk, leap and swat, never catch); cats look up and slow-blink at you (tap to blink back); a sanctuary house, sign and gate outside the fence; new cats come from kittens (related cats never pair up) or strays at the gate; a "meet" sheet pauses play and shows every cat's stats.

# Next pass (from playtesting v1)
- **Item tiers:** every shop item gets upgrades. E.g. Cat tree, then Super cat tree (3 floors, hidey-holes, more scratching posts, dangling toys). Same for beds, balls (ball track, tunnel), roofs (gazebo), bowls (fountain), litter (self-cleaning).
- **Endgame:** the shop was maxed out in 10–15 min. Ideas: more meadow levels / new biomes (pond garden, barn loft), adoption (happy cats go to loving homes for big rewards and a "family photo" wall), cosmetics (collars, bandanas), seasonal events, prestige shows, decorations for the house.
- **Badge tiers:** bronze, silver and gold for each badge (e.g. Gentle Hands 10/50/200 strokes, Big Family 10/20/40).
- **Brush vs pet:** make the difference obvious, or merge them. See the answer in chat.

---
# Round 3 design: adoption, tiers, endgame (2026-11-21, not built yet)

## Pickup still looks stiff (v2 playtest)
- A relaxed cat should **drape**: body sags in a soft curve over the hands, hind legs and tail dangle loose, front paws rest on the hand, head tucks against your arm (or looks around calmly). Kittens go fully floppy.
- Stiffness comes ONLY from low trust (and builds over time): then legs splay, body goes rigid, the wiggle starts.
- Needs a bendable spine (2–3 body segments) instead of one rigid ellipsoid. Same rig helps flops, stretches and loafs.

## Core principle: a rescue, not a supplier
The loop is: **cat arrives in need → you help it heal and trust → it finds the right home → a new cat in need arrives.** Nothing is produced to be handed out.

### 1. Stop breeding inside the sanctuary
- In-meadow pairing + adopting kittens out = a kitten mill, however cute. Remove it.
- Real rescues spay/neuter. Model it lightly: new arrivals get a **vet check** in the cottage (a visit animation, a band-aid/cone moment, no surgery shown).
- Kittens still come, but **as rescues**: a pregnant stray who has her litter safely in the nursery, a box of kittens left at the gate, a mama with kittens under the cottage porch.
- Bonding stays (friendship hearts, best friends). Payoff: **bonded pairs get adopted together**, which is also real rescue practice.

### 2. No price, no fee, no reward per cat
- The family never pays for a cat. No coins pop when a cat leaves.
- Money comes from the sanctuary as a whole: **visitors and donations** (happy, healthy meadow, so people drop coins in the donation jar at the gate), cat fairs, sponsors. Homes found raise **Sanctuary Reputation**, which brings more visitors and also *more cats who need help*. The reward for adoption is more rescue work, not cash.

### 3. "Ready" means "ready to go home", not "good enough"
- No quality bar: coat, looks, show results and rare colors play no part. Age, shyness, a missing eye, being a grumpy old tom: every cat can find a home.
- The only gate is the cat's **comfort with people** (it's settled, eats well, lets a new person near it). That's about the cat's wellbeing, not its value. Shown as a little house icon on the tag: "Ready for a home".
- Some cats are happiest staying: the player can mark any cat a **Forever Resident**. The sanctuary is also a home. Never pressure the player to adopt out.

### 4. Matching, not selling
- Families visit (visible people at the gate). Each has a few **picture needs**: quiet home / lively kids / other pets / garden / apartment, senior couple, a kid who wants a lap cat.
- The player picks which cat to introduce. A shy cat fits the quiet retired couple; a zoomies cat fits the family with kids.
- **Meet-and-greet**: the visitor kneels, the cat decides. If it's not a match, the cat simply walks back to its friends and the family says "we'll find the right one". No penalty, no failure screen.
- Bonded pairs: the game suggests adopting them together.

### 5. The goodbye (the emotional hook)
- A short scene: the family waits at the gate with a carrier/blanket; the player gets a last pet; the cat **slow-blinks at you**, walks out, looks back once.
- Friends left behind get a little comfort moment (they sit together; the helper sits with them).
- The cat's spot gets a small photo frame in the cottage: the **Happy Tails wall**.

### 6. Postcards (the long tail)
- A few minutes later (and on later visits if we save), a **postcard** arrives: the cat in its new home (sunny window, in a kid's arms, on a dog's bed), with one line from the family.
- Collecting postcards is the long-term collection, much warmer than badges.

### 7. Shows, reframed
- "Best in show" judging on looks clashes with "every cat is good enough". Turn shows into a **Cat Fair** where every cat can win a category: Best Purr, Fluffiest, Bravest Rescue, Most Improved, Best Friends, Silliest Sleeper. Most Improved specially rewards the shy rescues.

## Item tiers (each one visibly changes the model + adds a behavior)
| Item | Tier 1 | Tier 2 | Tier 3 |
|---|---|---|---|
| Cat tree | Perch | Tall tree: 2 perches + hammock | Castle: 3 floors, hidey-holes, sisal posts, dangling toys, holds 3 cats |
| Bed | Cushion | Heated pad (rain days) | Sunny window box on the cottage |
| Ball | Jingle ball | Ball track (cats bat it alone) | Tunnel maze (hide-and-pounce) |
| Bowl | Bowl | Raised bowl | Water fountain (Health) |
| Litter | Box | Big box | Covered box (stays fresh longer) |
| Roof | Rain roof | Gazebo with cushions | Sunroom (cats play inside while it rains) |
| Wand | Feather | Ribbon wand | Mouse-on-a-string (cats carry it off) |
| Laser | Laser | | Laser + treat finish (ends on a real "catch", which is what vets advise) |
Max tier per item depends on sanctuary level, so upgrades unlock over time.

## Endgame / long goals
- **Sanctuary stars (1–5)**, earned from homes found, average happiness and rescues helped. Each star unlocks a new area, item tiers and new kinds of rescues (seniors, a three-legged cat, a mama with kittens, a feral who takes ages to trust).
- **New areas** instead of just a bigger square: pond garden (fish, frogs), barn loft (climbing beams), cottage interior (vet room, nursery, adoption office).
- **Cottage grows** with the sanctuary: nursery, vet room, Happy Tails wall.
- **Badge tiers** (bronze/silver/gold): Gentle Hands 10/50/200, Happy Tails 1/10/30 homes, Bonded Pairs 1/3/10, Patient Friend (a cat that arrived with trust under 15 finds a home) 1/3/10.
- **Visit goals** (3 small ones per session): "Help a shy cat trust you", "Meet a family", "Brush 3 cats". Good for Poki's return visits.
- **Saving progress** becomes important once there are postcards and stars.

## Bug: cats vanished (v2 playtest)
- The user looked away for ~2 seconds and both cats were gone. Not reproduced yet.
- Suspects, in order: (1) a NaN creeping into a cat's position or heading (cat stops rendering), (2) both cats away at a show (hidden for 25 s, no visible "away" marker), (3) a cat pushed outside the fence by collision/hop-free and the camera can't see it, (4) the meet-card camera move.
- Fixes regardless: a NaN guard that snaps a cat back to a valid spot; an "away at the show" marker (ribbon icon on the HUD cat count, or a little bus at the gate); the HUD cat chip, when tapped, cycles the camera through every cat.

## Feature idea from that: the runaway
- A cat with **low trust** (and only then) can slip under the fence and wander off. It's never lost for good and never in danger.
- You **go find it**: a paw-print trail and a faint meow point the way; it's hiding somewhere outside (under the cottage porch, in a bush, on the bench, behind hay bales).
- Tap it gently (no grabbing a scared cat) and it follows you back, or a treat lures it home. Trust goes **up** afterward ("you came for me").
- Makes the world outside the fence matter, and gives a reason to keep shy cats' trust up.
- Keep it rare, and only while the player is actively playing (never "you were away and lost a cat").

## Decisions (user, 2026-11-21)
- **Keep some breeding**, alongside rescues. Everything else in the round 3 design is approved.
- Guardrails so it never reads as a mill:
  - Rescues stay the main way new cats arrive; kittens born here are the occasional, special event.
  - A pair raises **at most one litter**, then both get their vet visit (neutered). The game says so with a picture, not text.
  - Born-here kittens **stay with mum until grown**. They're never offered for adoption as kittens, and never with a reward tied to the birth.
  - Litters only happen when there's room and the meadow is happy (as now), and related cats never pair.

## New animations / interactions
- **Stretches**, now and then: the play-bow stretch (front legs reaching forward, bum up, tail high, big yawn) and the **arched "cat pose"** (back arched up, legs straight, fur fluffed slightly). Mostly after naps and on waking.
- **Tap a butterfly:** it flutters up and does a little loop; a nearby cat looks up and chatters or leaps.
- **Tap a bird:** it hops, cocks its head and chirps (or flutters to the fence if a cat is close); cats' ears swivel toward it.

## Stat icons aren't self-explanatory
- Heart reads fine as Affection. The blue paw doesn't say "Trust", and the green cross is only so-so for Health.
- Trust icon options: a **paw resting in an open hand** (best fit: the cat letting you close), or two half-closed "slow-blink" eyes.
- Health: keep green, maybe a leaf or a little sparkle-cat instead of a medical cross.
- Add **short word labels the first few times** the stat tag shows (Love · Trust · Health), then fade to icons only. Same labels on the meet card.
- When a stat changes, the matching icon pulses (the paw-in-hand bounces on a trust gain), so players learn which icon is which from what they just did.
