# Build, Wiring, and Test Checklist

## Before wiring

- [ ] Confirm Arduino UNO R4 WiFi
- [ ] Confirm BME280 sensor
- [ ] Confirm door/contact sensor
- [ ] Confirm water leak sensor
- [ ] Confirm LED resistor values
- [ ] Confirm non-metallic enclosure location
- [ ] Confirm low-voltage-only routing
- [ ] Confirm shielded 22/4 cable
- [ ] Confirm DIN terminal blocks and ferrules

## Bench test

- [ ] Upload bench sketch
- [ ] Open Serial Monitor at 115200 baud
- [ ] Confirm BME280 is detected
- [ ] Confirm temperature reading
- [ ] Confirm humidity reading
- [ ] Confirm door/contact open and closed states
- [ ] Confirm water leak dry and wet states
- [ ] Confirm green LED normal state
- [ ] Confirm red LED alert state

## Enclosure test

- [ ] Mount board in non-metallic enclosure
- [ ] Terminate door and leak home-runs on terminal blocks
- [ ] Confirm shield drains land at enclosure end only
- [ ] Confirm door 4.7k pull-up installed
- [ ] Confirm USB-C bulkhead power entry
- [ ] Confirm strain relief and drip loops
- [ ] Confirm WiFi signal through enclosure

## Arduino Cloud test

- [ ] Create Cloud Thing
- [ ] Create Cloud variables
- [ ] Upload Cloud sketch
- [ ] Confirm values update on dashboard
- [ ] Confirm alert state changes on door open
- [ ] Confirm alert state changes on water detection
- [ ] Confirm sensor fault handling

## Final trailer documentation

- [ ] Take real build photos
- [ ] Capture dashboard screenshots
- [ ] Update README
- [ ] Update Arduino Project Hub page
