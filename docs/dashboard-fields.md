# Dashboard Fields

Planned Arduino Cloud dashboard fields:

| Field | Type | Purpose |
| --- | --- | --- |
| temperatureF | Float | Trailer/equipment-space temperature in °F |
| humidityPercent | Float | Trailer/equipment-space relative humidity |
| waterDetected | Boolean | Water/leak detected or dry |
| doorOpen | Boolean | Door/contact open or closed |
| systemAlert | Boolean | Overall alert state |
| batteryVoltage | Float | Planned V2 battery-voltage display using protected sensing hardware |
| ecoFlowStatus | String | Planned V2 EcoFlow status/manual entry/API integration |

## Suggested dashboard cards

- Battery bank status
- EcoFlow status
- Temperature
- Humidity
- Water leak status
- Door/contact status
- System health
- Last update time
