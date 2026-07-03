# Changelog

## v2.0 - 2026-07-02

### Firmware
- Added Cloud sketch REV 2.0 (`CEL-MPT-FW-002`): non-blocking loop,
  confirm-N glitch filter on door/leak, BME280 auto-recovery, offline-first
  local alerting, optional watchdog/RSSI blocks.
- Telemetry split: floats on 30 s time policy, booleans ON_CHANGE.

### Installation package
- CEL-MPT-INS-001 install packet (branded PDF): BOM addendum, pull/label
  schedule, internal termination map, field practices.
- Doc-controlled wiring drawings: DWG-001 (bench), DWG-002 (enclosure +
  home runs).
- `docs/enclosure-install.md` design-decision record.
- Machine-readable `data/install_bom_addendum.csv` + `data/pull_schedule.csv`.
- `tools/build_install_packet.py` single-source generator (CSV + MD + PDF).

### Repo hygiene
- `.gitignore` now blocks `arduino_secrets.h`; credentials ship only as
  `.example`.
- README rebuilt: quick start, Cloud go-live, install doctrine, doc-control
  table.

## v1.0
- Initial concept docs, bench test sketch, base BOM, wiring plan,
  test checklist, safety note, Project Hub assets.
