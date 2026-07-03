# Pin Map

| Signal | Arduino pin | Terminal | Field conductor | Notes |
| --- | --- | --- | --- | --- |
| BME280 SDA | SDA | Local only | Short Qwiic/I2C lead | I2C stays inside enclosure |
| BME280 SCL | SCL | Local only | Short Qwiic/I2C lead | I2C stays inside enclosure |
| BME280 VIN | 3.3V or 5V | Local only | Follow sensor board instructions | Local environmental sensor |
| BME280 GND | GND | Local only | Common low-voltage reference | Local environmental sensor |
| Door/contact signal | D2 | TB-1 | DR-01 white | External 4.7k pull-up TB-1 to 5V |
| Door/contact return | GND | TB-2 | DR-01 black | Door return |
| Water leak digital out | D3 | TB-3 | WL-01 white | Leak sensor digital output |
| Water leak power | 5V | TB-4 | WL-01 red | Leak sensor power |
| Water leak return | GND | TB-5 | WL-01 black | Leak return |
| Shield drains | GND/shield bar | GND/shield bar | both drains | Shield lands at enclosure end only |
| Green normal LED | D5 | Internal | via 220 ohm resistor | Face LED normal |
| Red alert LED | D6 | Internal | via 220 ohm resistor | Face LED alert |
| Arduino power | USB-C | bulkhead | PWR-01 | Dedicated >= 2 A 5V supply |

## Notes

Keep all Arduino wiring low-voltage only. Use labels, ferrules, strain relief, and wire separation. Do not route Arduino conductors with line-voltage wiring.
