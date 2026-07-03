# Install BOM Addendum

Adds field-install enclosure and home-run materials to the base BOM; it does not replace the bench-build BOM.

| Qty | Item | Spec | Purpose | Notes |
| --- | --- | --- | --- | --- |
| 1 | Enclosure, polycarbonate NEMA 4X non-metallic | ~8x6x4 in, IP66/4X, clear or opaque lid | House board + DIN terminals; RF-transparent for WiFi | Must be non-metallic because a metal box blocks the on-board WiFi antenna. |
| 1 | DIN rail, 35 mm | steel/aluminum, cut to ~6 in | Mount terminal blocks + board carrier | Trim to enclosure interior width. |
| 10 | Feed-through terminal blocks, 2.5 mm² | screw or spring, DIN-mount | Land all field conductors | 7 used + spares. Do not solder field wires to the board. |
| 1 | Terminal end bracket + end plate set | 35 mm DIN | Retain terminal stack | 2 end brackets + 1 end plate typical. |
| 2 | Ground/shield terminal block | grounding type, DIN-mount | Single-point shield/GND landing bar | Shield lands here at enclosure end only. |
| 3 | Cable gland, IP68 | PG7 or M12, 3.0–6.5 mm cable OD | Seal + strain-relief signal home runs | 2 used plus 1 spare. Bottom entry. |
| 1 | USB-C panel-mount bulkhead pass-through | IP67, C-female to C-female | Power entry for dedicated 5V supply | Cleaner and sealed versus trying to gland a molded USB plug. |
| 1 | Shielded cable, 22 AWG / 4 conductor, stranded | overall foil shield + drain, ~5–6 mm OD | Door and leak home runs | ~54 ft needed; buy 100 ft spool. |
| 1 | Wire ferrules, 22 AWG + crimp tool | insulated ferrules assortment | Terminate stranded conductors into terminals | Prevents strand splay. |
| 2 | Resistor, 4.7k ohm 1/4 W | 5% carbon film | External pull-up for door line | 1 used + spare. |
| 2 | Panel-mount LED holder/bezel, 5 mm | chrome or black bezel | Face-mount green/red status LEDs | Uses 5 mm LEDs + 220 ohm resistors from base BOM. |
| 4 | Anti-vibration mount / rubber isolator | well-nut or grommet mount, M4/M5 | Isolate enclosure from trailer vibration | Prevents fatigue on solder joints and terminals. |
| 1 | Self-fusing silicone tape + heat-shrink assortment | — | Shield termination + far-end drain dressing | Cut and tape shield/drain at each sensor end. |
| 1 | Wire label set | heat-shrink or self-lam wrap | Both-end labels per pull schedule | Label DR-01, WL-01, PWR-01, ENC-01. |
| 1 | Cable ties + adhesive mounts | UV-rated | Dress conductors and form drip loops | Use UV-rated for mobile/outdoor environment. |
| 1 | Future waterproof DS18B20 1-Wire temp probe + 4.7k | 1-Wire, waterproof lead | Remote temperature without extending I2C | Optional. |
| 2 | Future clamp-on ferrite core | for 5–6 mm cable | Extra EMI suppression | Optional. |
