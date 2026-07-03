# Wiring Plan

## Bench prototype

1. Power the Arduino UNO R4 WiFi through USB-C.
2. Connect the BME280 using STEMMA QT/Qwiic or short I2C wiring.
3. Wire the magnetic contact sensor to D2 and GND.
4. Wire the water leak sensor digital output to D3.
5. Wire the green LED to D5 through a 220 ohm resistor.
6. Wire the red LED to D6 through a 220 ohm resistor.
7. Open Serial Monitor at 115200 baud.
8. Confirm sensor readings and status messages.

## Enclosure install plan

- Use a non-metallic polycarbonate NEMA 4X / IP66 style enclosure.
- Mount DIN rail and terminal blocks inside the enclosure.
- Land field conductors on terminal blocks, not directly on the Arduino.
- Use a dedicated >= 2 A 5V USB-C power supply through an IP67 USB-C bulkhead.
- Route door and leak sensors as home-runs using 22/4 shielded stranded cable.
- Land shields/drains at the enclosure GND/shield bar only.
- Cut and tape shield/drain at the sensor end.
- Add drip loops and bottom-entry glands.
- Mount the enclosure on vibration isolators.

## Battery voltage note

Do not connect the Arduino analog input directly across the trailer battery bank. Add battery voltage monitoring only after selecting a proper protected sensing method with fusing, isolation where needed, and code-compliant low-voltage wiring.

## EcoFlow note

The EcoFlow system is documented as a monitored asset. Direct integration should only be added through a supported API, safe low-voltage signal, or manual dashboard field.
