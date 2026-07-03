# Enclosure & Home-Run Install

**Doc:** CEL-MPT-INS-001 · **Rev:** 1.0 · Helios Prime

Moves the Mobile Power Trailer Monitor from the bench into the trailer with remote long home-run door and leak sensors and a dedicated 5V USB-C feed.

## Scope and assumptions

| Parameter | Value / result |
| --- | --- |
| Door contact home run | 25 ft |
| Leak sensor home run | 15 ft |
| USB-C power run | 6 ft |
| Pull slack + service loops | +14% and 2 ft/end |
| Signal cable needed | ~54 ft → buy 100 ft spool 22/4 shielded |

## Design decisions

- **Non-metallic enclosure:** The UNO R4 WiFi uses a PCB trace antenna. A metal enclosure can block the on-board WiFi antenna and silently kill the Cloud link. Use polycarbonate NEMA 4X / IP66 style enclosure.
- **Shield single-point ground:** Land the shield drain at the enclosure GND bar only. Cut and tape it at each sensor end. Grounding both ends can create a loop and inject noise.
- **Door pull-up:** The Arduino internal `INPUT_PULLUP` is weak for a long line. Use an external 4.7k ohm pull-up from D2 to 5V for the door input.
- **Keep BME280 local:** I2C is not a long-run bus. Keep the BME280 inside or near the enclosure with a short Qwiic/I2C lead. For remote temperature later, use a DS18B20 1-Wire probe.
- **Power margin:** Feed the board from a dedicated >= 2 A 5V USB-C supply through an IP67 USB-C bulkhead. Avoid undersized supplies that brown out during WiFi bursts.
- **Mechanical protection:** Use bottom-entry glands, drip loops, DIN terminal blocks, ferrules, and anti-vibration enclosure mounting.

## Field home-runs

| Tag | From | To | Cable | Conductors | Length | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| DR-01 | ENC-01 TB D2 + GND | Door contact | 22/4 shielded | white=sig, black=return | 25 ft | Reed on frame, magnet on leaf. Shield lands at enclosure only. |
| WL-01 | ENC-01 TB D3, 5V, GND | Leak sensor | 22/4 shielded | red=V+, black=GND, white=DO | 15 ft | Mount at lowest point. Green spare. Shield lands at enclosure only. |
| PWR-01 | 5V USB-C supply | ENC-01 USB-C bulkhead | USB-C | USB-C | 6 ft | Dedicated >= 2 A supply. Enter through bulkhead, not a gland. |

## Internal termination map

| Board pin | Terminal | Field conductor | Notes |
| --- | --- | --- | --- |
| D2 | TB-1 DR sig | DR-01 white | Door signal; 4.7k pull-up TB-1 to 5V |
| GND | TB-2 DR ret | DR-01 black | Door return |
| D3 | TB-3 WL DO | WL-01 white | Leak digital output |
| 5V | TB-4 WL V+ | WL-01 red | Leak sensor power |
| GND | TB-5 WL GND | WL-01 black | Leak return |
| GND/shield bar | Shield bar | both drains | Shields land here at enclosure end only |
| D5 | via 220 ohm | green LED | Face LED normal |
| D6 | via 220 ohm | red LED | Face LED alert |
| USB-C | board USB-C port | bulkhead | Power from PWR-01 bulkhead |

## Firmware backstop

REV 2.0 firmware adds glitch filtering for long door/leak home runs and BME280 self-recovery if the sensor drops off the bus. These features matter in a vibrating, electrically noisy trailer environment.
