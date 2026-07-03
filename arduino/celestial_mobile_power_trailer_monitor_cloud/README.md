# Arduino Cloud Firmware — REV 2.0

This folder contains the Arduino Cloud edition of the Celestial Electric Mobile Power Trailer Monitor firmware.

## Files

```text
celestial_mobile_power_trailer_monitor_cloud.ino
thingProperties.h
arduino_secrets.h.example
```

## Important Arduino Cloud note

Arduino Cloud normally generates `thingProperties.h` automatically when you create the Thing and variables in the web editor. The copy in this repository is a reference version so the public repo documents the expected variable structure.

Do not commit real WiFi credentials. Use `arduino_secrets.h.example` as a template only.

## Cloud variables

Create these READ variables in Arduino Cloud:

| Variable | Type | Policy | Purpose |
| --- | --- | --- | --- |
| `temperatureF` | Float | 30 seconds | Trailer/equipment temperature |
| `humidityPercent` | Float | 30 seconds | Relative humidity |
| `waterDetected` | Boolean | On change | Leak/water state |
| `doorOpen` | Boolean | On change | Door/contact state |
| `systemAlert` | Boolean | On change | Overall alert roll-up |

Optional diagnostic variable:

| Variable | Type | Policy | Purpose |
| --- | --- | --- | --- |
| `signalStrength` | Int | 60 seconds | WiFi RSSI for enclosure placement testing |

## REV 2.0 field-hardening

- Door and leak inputs use a confirm-count glitch filter for long home runs.
- BME280 sensor reads are checked for NaN and re-initialized if the sensor drops off the bus.
- Alert logic keeps sensor fault and environmental alert conditions distinct internally.
- Optional watchdog and RSSI diagnostic notes are included in comments.
