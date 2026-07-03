# Celestial Electric Mobile Power Trailer Monitor

A smart low-voltage monitoring concept for Celestial Electric’s mobile power trailer, tracking battery, EcoFlow, environmental, leak, and door status through Arduino Cloud.

## Project status

**Work in progress / active build.**  
The trailer is prepared for the monitoring system. This repository documents the bench prototype, Arduino Cloud firmware, enclosure install plan, home-run pull schedule, and field practices before final hardware installation and field testing.

## Project purpose

This project demonstrates how Celestial Electric can turn a mobile contractor trailer into a smart, monitored power platform. The first version focuses on low-voltage monitoring, clean documentation, and safe sensor integration.

The monitoring concept includes:

- Trailer interior temperature and humidity
- Water leak detection
- Door/contact status
- Normal/alert LED indication
- Arduino serial test output
- Planned Arduino Cloud dashboard integration
- Planned battery bank and EcoFlow visibility
- Serviceable enclosure wiring with terminal blocks and labeled home-runs

## Trailer power system notes

The trailer battery bank consists of two Duracell 12V lead-acid batteries rated **810 CCA each**, wired in **parallel**. Because the batteries are wired in parallel, the system remains a **12V nominal battery bank**, not a 24V system.

The trailer also includes an EcoFlow portable power system as a separate mobile power source.

> CCA is a starting-current rating, not an energy-capacity rating. Runtime calculations will require the battery group size, amp-hour rating, or reserve-capacity rating from the battery labels.

## Enclosure and home-run install concept

The field-install plan moves the monitor from breadboard into the trailer with a dedicated low-voltage enclosure, DIN terminal blocks, remote door/leak sensor home-runs, and a dedicated 5V USB-C feed.

Key install notes:

- Door contact home run: 25 ft
- Leak sensor home run: 15 ft
- USB-C power run: 6 ft
- Recommended cable: 100 ft spool of 22/4 shielded stranded cable
- Enclosure: non-metallic polycarbonate NEMA 4X / IP66 style enclosure
- Power entry: IP67 USB-C bulkhead pass-through
- Field terminations: DIN terminal blocks, not soldered field wires
- Shielding: shield/drain landed at enclosure end only
- Door input: external 4.7k pull-up to stiffen the long line against EMI

## Safety boundary

This project is for **low-voltage monitoring, training, and demonstration only**.

Do not connect an Arduino directly to service equipment, PV strings, battery terminals, inverter terminals, generator controls, transfer switches, utility equipment, fire alarm circuits, or line-voltage wiring.

Any real field installation must use proper listed equipment, isolation, fusing, overcurrent protection, enclosures, strain relief, wire separation, and code-compliant wiring methods. This project does not replace listed safety controls, manufacturer monitoring systems, battery management systems, utility-required equipment, generator/ATS controls, fire alarm systems, or code-required protective devices.

## Repository layout

```text
arduino/
  celestial_mobile_power_trailer_monitor/
    celestial_mobile_power_trailer_monitor.ino

  celestial_mobile_power_trailer_monitor_cloud/
    celestial_mobile_power_trailer_monitor_cloud.ino
    thingProperties.h
    arduino_secrets.h.example

data/
  bom.csv
  install_bom_addendum.csv
  pull_schedule.csv

docs/
  safety-note.md
  trailer-monitoring-overview.md
  dashboard-fields.md
  bom.md
  build-log.md
  enclosure-install.md
  install-bom-addendum.md
  pull-schedule.md
  assets/
    images/
    pdfs/

hardware/
  pin-map.md
  wiring-plan.md
  test-checklist.md
```

## Arduino sketches

### Bench test sketch

The bench sketch reads:

- BME280 temperature/humidity sensor
- Magnetic door/contact sensor
- Water leak sensor
- Red/green status LEDs

It prints status values to the Serial Monitor and can be used before Arduino Cloud variables are created.

### Arduino Cloud sketch

The Cloud sketch is a REV 2.0 field-hardening version intended for Arduino Cloud integration. It adds:

- Door/leak glitch filtering
- Consecutive agreeing samples before accepting state changes
- BME280 self-recovery if sensor reads drop out
- Cloud variable updates
- A reference `thingProperties.h`
- A safe `arduino_secrets.h.example` file without real WiFi credentials

## Planned Arduino Cloud variables

```text
temperatureF       float, read-only
humidityPercent   float, read-only
waterDetected     boolean, read-only
doorOpen          boolean, read-only
systemAlert       boolean, read-only
batteryVoltage    float, planned V2 with protected interface
ecoFlowStatus     string, planned V2/manual or API-based integration
```

## Current build phase

- [x] Concept documentation
- [x] Arduino Project Hub submission
- [x] Initial hardware test sketch
- [x] Arduino Cloud REV 2.0 sketch
- [x] Enclosure install plan
- [x] Pull schedule and install BOM addendum
- [ ] Purchase parts
- [ ] Build bench prototype
- [ ] Install monitoring enclosure
- [ ] Test sensors
- [ ] Create Arduino Cloud dashboard
- [ ] Add real trailer photos
- [ ] Update Project Hub page after first field test

## License

This repository is licensed under the Apache License 2.0 unless changed later to match the final Arduino Project Hub license selection.
