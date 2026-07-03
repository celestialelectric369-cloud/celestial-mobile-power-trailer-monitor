# Pull / Label Schedule

**Doc:** CEL-MPT-INS-001 (PLL) · **Rev:** 1.0 · **Date:** 2026-07-02 · Helios Prime

## Field home runs

| Tag | From | To | Signal | Cable | Conductors used | Len (ft) | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| DR-01 | ENC-01 TB D2 sig + GND | Door contact frame | Door open/close | 22/4 shielded | white=sig, black=return | 25 | Reed on frame, magnet on leaf. Shield to GND bar at enclosure end only; cut+tape at device. Drip loop at gland. |
| WL-01 | ENC-01 TB D3 DO, 5V, GND | Leak sensor floor/drip pan | Water/leak | 22/4 shielded | red=V+, black=GND, white=DO | 15 | Mount at lowest point. Green spare. Shield at enclosure end only; cut+tape at device. Drip loop at gland. |
| PWR-01 | 5V USB-C supply dedicated | ENC-01 USB-C bulkhead | 5V power | USB-C supply lead | USB-C | 6 | >= 2 A supply. Enter via IP67 bulkhead, not a gland. Short/quality cable; drip loop. |

## Label set

- ENC-01: Arduino monitoring enclosure
- DR-01: Door contact home run
- WL-01: Water leak sensor home run
- PWR-01: Dedicated 5V USB-C power feed

## Shielding rule

Shield drain is landed at the enclosure end only. Cut and tape shield/drain at the sensor/device end to prevent ground loops.
