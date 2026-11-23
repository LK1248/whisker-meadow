// Thumbnail scene variants for Whisker Meadow, built with tools/thumbstudio.js.
// Each returns { scene, cam, post } for TS.render(scene, cam, post).
const TS = window.TS; // set by the caller: window.TS = await import('/tools/thumbstudio.js')
const T = THREE, { COAT, rr, rnd, lin } = TS;
const add = (s, ...o) => { for (const x of o) s.add(x); };
const fireflies = (s, n, box, size = 1) => { for (let i = 0; i < n; i++) s.add(TS.firefly([rr(box[0], box[1]), rr(box[2], box[3]), rr(box[4], box[5])], rr(0.6, 1.3) * size)); };
const clouds = (s, list) => list.forEach(([x, y, z, k]) => { const g = new T.Group(); [[0, 0, 0, 1], [0.9, -0.15, 0.1, 0.75], [-0.85, -0.2, 0, 0.7], [0.3, 0.35, -0.1, 0.65]].forEach(([a, b, c, r]) => g.add(TS.ico(r, 0xffffff, 1, { p: [a, b, c], m: { roughness: 1 } }))); g.position.set(x, y, z); g.scale.setScalar(k); g.traverse(o => { o.castShadow = false; }); s.add(g); });

export const SCENES = {
  // A. The icon, in 3D: kitten peeking from a cardboard box with a knitted blanket, dusk and fireflies
  boxDusk() {
    rnd(11);
    const { scene } = TS.stage({ sky: TS.skyTex([[0, '#1d1a4a'], [0.42, '#4b3a7e'], [0.75, '#c9807f'], [1, '#f3b487']]), fog: [0x6a4f86, 7, 22],
      hemi: [0xb9a6ff, 0x3a2f4a, 0.55], sun: { hex: 0xffb37a, i: 1.1, p: [-4, 3.5, -6], shadow: 4 }, exposure: 1.0 });
    add(scene, TS.ground(40, [0x3f6b4a, 0x466f4c, 0x3a6345, 0x4a7650], 30, 0.08));
    const bx = TS.cardboardBox(1.5, 0.82, 1.1); add(scene, bx);
    const inner = TS.blanket(1.4, 1.0, 0xf08fab, 0.05); inner.position.set(0, 0.32, 0); add(scene, inner);
    const drape = TS.blanket(0.8, 0.42, 0xf08fab, 0.5); drape.position.set(-0.3, 0.86, 0.58); drape.rotation.y = 0.1; add(scene, drape);
    const k = TS.cat(COAT('orange', 'tabby', 0x8fd14f), { age: 0.75, state: 'idle', at: [0.05, 0.28, -0.1], yaw: -0.15 }); add(scene, k.g);
    TS.point(scene, [1.8, 1.8, 2.4], 0xffc98a, 2.2, 9, true);
    TS.point(scene, [-1.4, 1.2, -1.2], 0x9f8cff, 3, 6);
    for (let i = 0; i < 9; i++) { const p = TS.pine(rr(1.0, 1.8), 0x2d4a45); p.position.set(rr(-10, 10), 0, rr(-16, -10)); add(scene, p); }
    add(scene, TS.grassTufts(60, 4, [0, 0], 1.1, 0x3f7a4a));
    fireflies(scene, 16, [-2.2, 2.2, 0.4, 2.2, -2.5, 1.2]);
    add(scene, TS.stars(40, 30, 10));
    return { scene, cam: TS.camAt(30, [0.5, 1.55, 4.6], [0, 0.72, 0]), post: { bloom: 0.3, vignette: 0.42, sat: 1.2 } };
  },

  // B. Sunny diorama: the whole sanctuary on a floating island, tilt-shift
  diorama() {
    rnd(23);
    const { scene } = TS.stage({ sky: TS.skyTex([[0, '#7ec8f0'], [0.7, '#cdeefa'], [1, '#fff7e6']]), hemi: [0xfff6e8, 0x7aa860, 0.75], sun: { hex: 0xfff1d6, i: 2.0, p: [8, 14, 6], shadow: 9 }, exposure: 0.95 });
    const top = new T.Mesh(new T.CylinderGeometry(6.2, 6.2, 0.35, 16), TS.ico(1, 0x7cc35e).material); top.position.y = -0.17; top.receiveShadow = true;
    const dirt = new T.Mesh(new T.CylinderGeometry(6.2, 3.2, 2.6, 16), TS.ico(1, 0xa8754a).material); dirt.position.y = -1.6; dirt.castShadow = true;
    const rock = new T.Mesh(new T.ConeGeometry(3.2, 2.4, 12), TS.ico(1, 0x8a5d3a).material); rock.rotation.x = Math.PI; rock.position.y = -4.1;
    add(scene, top, dirt, rock);
    const h = TS.house(); h.position.set(-1.2, 0, -3.1); h.scale.setScalar(0.85); add(scene, h);
    add(scene, TS.fenceRing(5.3, 34, Math.PI / 2));
    [[3.8, -3.2, 1.1], [-4.4, -1.2, 0.9], [4.6, 1.4, 0.8], [-3.6, 3.2, 0.75]].forEach(([x, z, s]) => { const t = TS.tree(s, [0x5eae4f, 0x6fbf5a, 0x76b85c][Math.floor(rnd() * 3)]); t.position.set(x, 0, z); add(scene, t); });
    [[2.2, -3.6], [-3.2, -2.9], [0.8, 3.9]].forEach(([x, z]) => { const b = TS.bush(0.8); b.position.set(x, 0, z); add(scene, b); });
    add(scene, TS.flowers(70, 5, [0, 0], 1.2), TS.grassTufts(40, 5, [0, 0], 1.5));
    const pond = new T.Mesh(new T.CylinderGeometry(1.1, 1.1, 0.05, 12), new T.MeshStandardMaterial({ color: lin(0x6ec3f0), roughness: 0.15, metalness: 0.1, flatShading: true })); pond.position.set(2.6, 0.02, 1.6); pond.scale.set(1, 1, 0.7); add(scene, pond);
    const bed = TS.item('bed', 3); bed.position.set(-1.6, 0, 0.9); add(scene, bed);
    const tr = TS.item('tree', 3); tr.position.set(1.4, 0, -1.6); add(scene, tr);
    const ball = TS.item('ball', 2); ball.position.set(0.9, 0, 2.2); add(scene, ball);
    add(scene, TS.cat(COAT('orange', 'tabby'), { state: 'sleep', at: [-1.6, 0.18, 0.9], yaw: 0.6 }).g);
    add(scene, TS.cat(COAT('black', 'tuxedo', 0xf2b632), { state: 'flop', flop: 1, at: [-0.2, 0, 0.5], yaw: 0.5 }).g);
    add(scene, TS.cat(COAT('grey', 'tabby', 0x6ec3f0), { state: 'idle', at: [2.2, 0, 0.2], yaw: -0.9 }).g);
    add(scene, TS.cat(COAT('cream', 'socks'), { age: 0.45, state: 'idle', at: [0.4, 0, 2.6], yaw: 0.3 }).g);
    add(scene, TS.cat(COAT('white', 'solid', 0x6ec3f0), { state: 'idle', at: [-0.3, 0, -1.6], yaw: 0.2 }).g);
    clouds(scene, [[-9, 5, -14, 1.6], [8, 7, -16, 2], [-14, 2, -6, 1.2], [13, 1.5, -4, 1.3]]);
    return { scene, cam: TS.camAt(28, [12, 10.5, 14], [0, -0.4, 0]), post: { tilt: 5, tiltBand: [0.36, 0.66], bloom: 0.16, vignette: 0.22 } };
  },

  // C. Golden hour belly-up: tuxedo flopped in the grass, orange friend, long shadows and floating seeds
  goldenFlop() {
    rnd(37);
    const { scene } = TS.stage({ sky: TS.skyTex([[0, '#f0a868'], [0.5, '#f9cf8f'], [1, '#ffe9c0']]), fog: [0xf6d49a, 6, 20], hemi: [0xffe9c4, 0x6f8a3c, 0.5],
      sun: { hex: 0xffb866, i: 2.6, p: [-6, 2.6, -5], shadow: 4, target: [0, 0, 0.5] }, exposure: 1.0 });
    add(scene, TS.ground(40, [0x9cc35a, 0x8fbb52, 0xa8cb62, 0x94bf56], 40, 0.06));
    add(scene, TS.cat(COAT('black', 'tuxedo', 0xf2b632), { state: 'flop', flop: 1, at: [-0.15, 0, 0.3], yaw: 0.35 }).g);
    add(scene, TS.cat(COAT('orange', 'tabby'), { state: 'idle', at: [1.05, 0, -0.45], yaw: -0.55 }).g);
    add(scene, TS.flowers(90, 4.5, [0, 0], 1.0, [0xffffff, 0xffd84d, 0xfff2a8]), TS.grassTufts(120, 5, [0, 0], 0.9, 0x7faa3e));
    for (let i = 0; i < 7; i++) { const t = TS.tree(rr(1.1, 1.6), 0x6aa648); t.position.set(rr(-8, 8), 0, rr(-12, -6)); add(scene, t); }
    for (let i = 0; i < 26; i++) scene.add(TS.glow([rr(-2.5, 2.5), rr(0.3, 2.2), rr(-2, 1.8)], rr(0.08, 0.2), 0xfff1c4, rr(0.5, 1)));
    add(scene, TS.glow([-6, 2.6, -9], 9, 0xffc070, 0.55));
    return { scene, cam: TS.camAt(33, [0.45, 1.15, 4.5], [0.3, 0.4, 0]), post: { bloom: 0.34, vignette: 0.3, warm: 0.12, sat: 1.12 } };
  },

  // D. The adoption moment: a family at the gate, the cat shows its belly, hearts rise
  adoption() {
    rnd(41);
    const { scene } = TS.stage({ sky: TS.skyTex([[0, '#8fb6ea'], [0.5, '#f1b7c8'], [1, '#ffd9b0']]), fog: [0xf2c4c4, 9, 26], hemi: [0xfff0f0, 0x7aa860, 0.6],
      sun: { hex: 0xffcf9a, i: 2.0, p: [-5, 6, 6], shadow: 5 }, exposure: 0.98 });
    add(scene, TS.ground(40, [0x86c766, 0x7cc35e, 0x90cf6e, 0x78bd59], 34, 0.08));
    // gate: two posts + an arch with a heart
    const gate = new T.Group(); [-1.6, 1.6].forEach(x => gate.add(TS.box(0.18, 1.9, 0.18, 0xc99a6b, { p: [x, 0.95, 0] }))); gate.add(TS.box(3.6, 0.2, 0.22, 0xa5754a, { p: [0, 1.95, 0] }));
    const hh = TS.heart3d(0.28, 0xff6f96); hh.position.set(0, 2.3, 0.05); gate.add(hh);
    gate.position.set(0, 0, -0.6); add(scene, gate);
    for (const sx of [-1, 1]) { const f = new T.Group(); for (let i = 0; i < 5; i++) { f.add(TS.box(0.1, 0.7, 0.1, 0xe2b67f, { p: [sx * (2.0 + i * 0.7), 0.35, -0.6] })); f.add(TS.box(0.7, 0.07, 0.05, 0xf0cb93, { p: [sx * (2.35 + i * 0.7), 0.5, -0.6] })); f.add(TS.box(0.7, 0.07, 0.05, 0xf0cb93, { p: [sx * (2.35 + i * 0.7), 0.25, -0.6] })); } add(scene, f); }
    const mom = TS.person({ woman: true, shirt: 0xe58fb5, skin: 0xd9a27b, hair: 0x2a2421, at: [-0.55, 0, -1.6], yaw: 0.15 });
    const dad = TS.person({ shirt: 0x7fb2e5, skin: 0xf0c8a0, hair: 0x7a4a2a, at: [0.75, 0, -1.8], yaw: -0.25 });
    const kid = TS.person({ shirt: 0xffd84d, skin: 0xd9a27b, hair: 0x2a2421, scale: 0.66, at: [0.15, 0, -1.15], yaw: 0 });
    add(scene, mom.g, dad.g, kid.g);
    add(scene, TS.cat(COAT('orange', 'tabby'), { state: 'flop', flop: 1, at: [0.0, 0, 0.55], yaw: 0.25 }).g);
    for (let i = 0; i < 4; i++) { const h = TS.heart3d([0.15, 0.11, 0.09, 0.07][i], [0xff6f96, 0xff8fb0, 0xff5c86][i % 3]); h.position.set([0.75, 1.0, 0.55, 1.15][i], [0.95, 1.25, 1.35, 1.6][i], [1.1, 1.0, 1.2, 0.9][i]); h.rotation.set(rr(-.3, .3), rr(-.6, .6), rr(-.4, .4)); add(scene, h); }
    for (let i = 0; i < 6; i++) { const t = TS.tree(rr(1.0, 1.5)); t.position.set(rr(-9, 9), 0, rr(-11, -5)); add(scene, t); }
    add(scene, TS.flowers(50, 4, [0, 1], 0.8));
    return { scene, cam: TS.camAt(34, [0.9, 1.25, 4.9], [0, 0.85, -0.5]), post: { bloom: 0.26, vignette: 0.28, warm: 0.06 } };
  },

  // E. Zoomies: a grey tabby leaping a bench, dust puffs, a friend watching
  zoomies() {
    rnd(53);
    const { scene } = TS.stage({ sky: TS.skyTex([[0, '#4fa8e8'], [0.6, '#a9dcf7'], [1, '#e9f8ff']]), hemi: [0xffffff, 0x7aa860, 0.7], sun: { hex: 0xfff4dc, i: 2.3, p: [5, 12, 7], shadow: 5 }, exposure: 0.95 });
    add(scene, TS.ground(40, [0x7cc35e, 0x6fb853, 0x86cb66, 0x74bd58], 34, 0.08));
    const b = TS.bench(1.6); b.position.set(0, 0, 0); b.rotation.y = 0.15; add(scene, b);
    const c = TS.cat(COAT('grey', 'tabby', 0x6ec3f0), { state: 'romp', speed: 3.2, set: { leap: 1, hopT: 0.25, hopDur: 0.5, hopH: 0.6 }, at: [0.1, 0.72, 0.1], yaw: Math.PI / 2 + 0.1 }); add(scene, c.g);
    c.g.rotation.z = 0.12;
    [[-1.5, 0.12, 0.25, 0.22], [-1.85, 0.08, 0.1, 0.16], [-1.25, 0.06, 0.45, 0.13], [-2.15, 0.05, 0.3, 0.1]].forEach(([x, y, z, r]) => add(scene, TS.ico(r, 0xf4ead8, 0, { p: [x, y, z], m: { roughness: 1 } })));
    add(scene, TS.cat(COAT('orange', 'tabby'), { state: 'idle', at: [1.6, 0, -1.9], yaw: -0.6 }).g);
    add(scene, TS.cat(COAT('white', 'calico', 0xf2b632), { age: 0.45, state: 'idle', at: [-2.3, 0, -1.2], yaw: 0.7 }).g);
    add(scene, TS.flowers(60, 5, [0, 0], 1.2), TS.grassTufts(70, 5, [0, 0], 1.0));
    for (let i = 0; i < 6; i++) { const t = TS.tree(rr(1.1, 1.6)); t.position.set([-11, -7, 6, 10, 13, -14][i], 0, rr(-15, -10)); add(scene, t); }
    clouds(scene, [[-6, 6, -20, 1.5], [7, 8, -22, 1.8]]);
    return { scene, cam: TS.camAt(34, [2.4, 0.8, 5.0], [0.1, 0.75, 0]), post: { bloom: 0.15, vignette: 0.22, sat: 1.18 } };
  },

  // F. Night: three cats asleep together in a bed, moonlight, lantern and fireflies
  nightCozy() {
    rnd(67);
    const { scene } = TS.stage({ sky: TS.skyTex([[0, '#0c1030'], [0.6, '#1f2a5a'], [1, '#3b3f78']]), fog: [0x1c2350, 6, 20], hemi: [0x9aa4e8, 0x2a2a24, 0.35],
      sun: { hex: 0xb8c8ff, i: 0.55, p: [-5, 9, -4], shadow: 4 }, exposure: 1.0 });
    add(scene, TS.ground(40, [0x2f5a48, 0x2a5243, 0x35614d, 0x2c5546], 30, 0.08));
    const bed = TS.item('bed', 1); bed.scale.setScalar(1.7); add(scene, bed);
    add(scene, TS.cat(COAT('orange', 'tabby'), { state: 'sleep', scale: 0.9, at: [-0.2, 0.2, -0.05], yaw: 0.9 }).g);
    add(scene, TS.cat(COAT('white', 'calico'), { age: 0.5, state: 'sleep', scale: 0.95, at: [0.42, 0.2, 0.3], yaw: 2.4 }).g);
    // lantern
    const lan = new T.Group(); lan.add(TS.cyl(0.03, 0.03, 1.3, 6, 0x5a4033, { p: [0, 0.65, 0] })); lan.add(TS.box(0.22, 0.26, 0.22, 0xffe2a0, { p: [0, 1.35, 0], m: { emissive: 0xffc260, emissiveIntensity: 1.6 } }));
    lan.position.set(1.05, 0, -0.55); add(scene, lan); add(scene, TS.glow([1.05, 1.35, -0.55], 1.6, 0xffb44a, 0.9)); TS.point(scene, [1.0, 1.3, -0.4], 0xffb45a, 11, 7, true);
    const moon = new T.Mesh(new T.IcosahedronGeometry(1.2, 1), new T.MeshBasicMaterial({ color: lin(0xfff6dc) })); moon.position.set(-7, 9, -18); add(scene, moon, TS.glow([-7, 9, -18], 9, 0xbfcfff, 0.6));
    add(scene, TS.stars(90, 28, 6));
    for (let i = 0; i < 8; i++) { const p = TS.pine(rr(1.3, 2.3), 0x1f3b3a); p.position.set(rr(-9, 9), 0, rr(-13, -6)); add(scene, p); }
    add(scene, TS.grassTufts(60, 4, [0, 0], 1.3, 0x2f6048));
    fireflies(scene, 14, [-2.5, 2.5, 0.3, 2, -2, 1.5]);
    return { scene, cam: TS.camAt(30, [0.2, 2.2, 3.9], [0.1, 0.3, 0]), post: { bloom: 0.42, vignette: 0.45, sat: 1.1 } };
  },

  // H. Face close-up: a tuxedo kitten looking right at you, flowers and soft bokeh
  tuxPortrait() {
    rnd(91);
    const { scene } = TS.stage({ sky: TS.skyTex([[0, '#9fd8f5'], [0.6, '#d9f1fb'], [1, '#fff5e4']]), fog: [0xd8eef5, 3, 12], hemi: [0xfffaf0, 0x86b860, 0.7],
      sun: { hex: 0xfff0d6, i: 2.0, p: [-3, 6, 5], shadow: 2.5 }, exposure: 0.95 });
    add(scene, TS.ground(30, [0x8fd06e, 0x86cb66, 0x9ad877, 0x80c460], 40, 0.05));
    add(scene, TS.cat(COAT('black', 'tuxedo', 0xf2b632), { age: 0.6, state: 'idle', at: [0, 0, 0], yaw: 0.2 }).g);
    add(scene, TS.flowers(140, 3.2, [0, 0], 0.55, [0xffffff, 0xffd84d, 0xff9ec7, 0xb89cff]), TS.grassTufts(90, 3, [0, 0], 0.5, 0x6fb853));
    for (let i = 0; i < 22; i++) add(scene, TS.glow([rr(-4, 4), rr(0.3, 3), rr(-6, -2.5)], rr(0.5, 1.3), [0xffffff, 0xffe6a8, 0xffc4dc, 0xc4f0ff][i % 4], rr(0.25, 0.55)));
    for (let i = 0; i < 4; i++) { const h = TS.heart3d(rr(0.05, 0.08)); h.position.set(rr(0.25, 0.6), rr(0.75, 1.05), rr(0.0, 0.3)); h.rotation.set(0, rr(-.5, .5), rr(-.3, .3)); add(scene, h); }
    return { scene, cam: TS.camAt(26, [0.25, 0.7, 2.9], [0, 0.5, 0]), post: { bloom: 0.25, vignette: 0.3, sat: 1.18 } };
  },

  // G. Show champion: groomed golden cat on a podium, rosette, confetti, spotlight
  champion() {
    rnd(79);
    const { scene } = TS.stage({ sky: TS.skyTex([[0, '#2a5a6a'], [1, '#5aa0a0']]), hemi: [0xdff6ff, 0x30454a, 0.45], sun: { hex: 0xfff0d8, i: 1.2, p: [3, 8, 5], shadow: 3 }, exposure: 0.82 });
    const pod = new T.Group(); pod.add(TS.cyl(0.95, 1.05, 0.55, 12, 0xffffff, { p: [0, 0.275, 0] })); pod.add(TS.cyl(0.97, 0.97, 0.06, 12, 0xf6c443, { p: [0, 0.57, 0], m: { metalness: 0.6, roughness: 0.3 } })); add(scene, pod);
    for (const [x, hex, h] of [[-1.9, 0xc0c8d6, 0.38], [1.9, 0xd9925a, 0.26]]) { const p = TS.cyl(0.8, 0.88, h, 12, 0xffffff, { p: [x, h / 2, -0.4] }); add(scene, p, TS.cyl(0.82, 0.82, 0.05, 12, hex, { p: [x, h + 0.02, -0.4], m: { metalness: 0.5, roughness: 0.35 } })); }
    add(scene, TS.cat(COAT('golden', 'tabby', 0x6ec3f0), { state: 'idle', at: [0, 0.6, 0], yaw: 0.25 }).g);
    // rosette
    const ro = new T.Group(); ro.add(TS.cyl(0.32, 0.32, 0.05, 14, 0x2f6fd0, { r: [Math.PI / 2, 0, 0] })); ro.add(TS.cyl(0.2, 0.2, 0.07, 12, 0xf6c443, { r: [Math.PI / 2, 0, 0], m: { metalness: 0.5, roughness: 0.3 } }));
    for (const sx of [-1, 1]) ro.add(TS.box(0.13, 0.45, 0.03, 0x2f6fd0, { p: [sx * 0.09, -0.38, 0], r: [0, 0, sx * 0.25] }));
    ro.position.set(0.95, 1.25, 0.55); ro.rotation.y = -0.3; add(scene, ro);
    for (let i = 0; i < 70; i++) { const cf = TS.box(0.07, 0.012, 0.045, [0xff6f96, 0xf6c443, 0x5b9be6, 0x8ce99a, 0xffffff][i % 5], { p: [rr(-2.4, 2.4), rr(0.4, 3.2), rr(-1.8, 1.4)], m: { roughness: 0.4 } }); cf.rotation.set(rr(0, 6), rr(0, 6), rr(0, 6)); add(scene, cf); }
    for (let i = 0; i < 18; i++) add(scene, TS.glow([rr(-7, 7), rr(0.5, 6), rr(-9, -6)], rr(0.6, 1.8), [0xfff1c4, 0x9ff0ff, 0xffc4dc][i % 3], rr(0.25, 0.6)));
    const spot = new T.SpotLight(lin(0xfff6e0), 9, 14, 0.42, 0.6, 1.5); spot.position.set(0.5, 6.5, 2); spot.target.position.set(0, 0.8, 0); spot.castShadow = true; spot.shadow.mapSize.set(2048, 2048); add(scene, spot, spot.target);
    const floor = new T.Mesh(new T.CircleGeometry(14, 28), new T.MeshStandardMaterial({ color: lin(0x356a72), roughness: 0.6, flatShading: true })); floor.rotation.x = -Math.PI / 2; floor.receiveShadow = true; add(scene, floor);
    return { scene, cam: TS.camAt(32, [0.8, 1.7, 5.2], [0, 0.95, 0]), post: { bloom: 0.26, vignette: 0.4, sat: 1.25 } };
  },
};
