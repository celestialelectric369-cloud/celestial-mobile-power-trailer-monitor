/*
  Celestial Electric - Mobile Power Trailer Monitor
  Arduino Cloud Edition  |  REV 2.0  |  Doc: CEL-MPT-FW-002
  Board: Arduino UNO R4 WiFi   |   Callsign: Helios Prime

  REV 2.0 field-hardening changes (over REV 1.0):
  - Glitch filter: door + leak inputs require N consecutive agreeing samples
    before a state change is accepted. Rejects EMI spikes on long home runs.
  - BME280 auto-recovery: NaN reads or a dropped sensor trigger a non-blocking
    re-init attempt each cycle, so a jostled Qwiic connector self-heals without
    a reboot.
  - Sensor-fault vs environment-alert kept distinct in logic (both still roll
    into systemAlert to preserve the 5-variable dashboard contract).
  - Optional blocks included (commented): hardware watchdog + WiFi RSSI
    diagnostic. Enable per notes below.

  Cloud variables (READ, device -> cloud):
    temperatureF, humidityPercent, waterDetected, doorOpen, systemAlert

  SAFETY: Low-voltage sensing/training/demo ONLY. Do NOT connect the Arduino to
  battery terminals, PV, inverter, generator, transfer switch, or any line
  voltage. Battery-voltage sensing is a V2 item behind a protected, isolated
  front end.
*/

#include "thingProperties.h"
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BME280.h>
#include <math.h>   // isnan()

// -------- Pin assignments (match hardware/pin-map.md) --------
const int DOOR_CONTACT_PIN = 2;   // Magnetic contact, closed = tied to GND
const int WATER_SENSOR_PIN = 3;   // Digital output from leak sensor
const int GREEN_LED_PIN    = 5;   // Normal-status LED via 220 ohm
const int RED_LED_PIN      = 6;   // Alert-status LED via 220 ohm

// Flip to LOW if your leak module drives its output LOW when wet.
const int WATER_DETECTED_STATE = HIGH;

// Demonstration alert thresholds.
const float HIGH_TEMP_F_THRESHOLD   = 95.0;
const float HIGH_HUMIDITY_THRESHOLD = 70.0;

// -------- Timing / filtering --------
const unsigned long SENSOR_INTERVAL_MS = 2000UL;   // read/publish cadence
const uint8_t       CONFIRM_COUNT      = 2;        // agreeing samples to accept a change
unsigned long lastSensorRead = 0;

Adafruit_BME280 bme;
bool  bmeReady = false;
bool  sensorFault = false;   // BME not responding (distinct from environment alert)

// -------- Glitch filter (confirm-N) --------
struct Debounced {
  bool    stable;
  bool    candidate;
  uint8_t count;
};
Debounced doorDb  = { false, false, 0 };
Debounced waterDb = { false, false, 0 };

// Returns the filtered (stable) state. A new raw value must repeat
// CONFIRM_COUNT times in a row before it is accepted.
bool updateDebounced(Debounced &d, bool raw) {
  if (raw == d.stable) {
    d.count = 0;
    d.candidate = raw;
  } else if (raw == d.candidate) {
    if (++d.count >= CONFIRM_COUNT) {
      d.stable = raw;
      d.count = 0;
    }
  } else {
    d.candidate = raw;
    d.count = 1;
  }
  return d.stable;
}

bool beginBME() {
  if (bme.begin(0x76)) { Serial.println("BME280 found at 0x76."); return true; }
  if (bme.begin(0x77)) { Serial.println("BME280 found at 0x77."); return true; }
  return false;
}

void setup() {
  Serial.begin(115200);
  delay(1500);

  pinMode(DOOR_CONTACT_PIN, INPUT_PULLUP);   // external 4.7k to 5V also fitted on long runs
  pinMode(WATER_SENSOR_PIN, INPUT);
  pinMode(GREEN_LED_PIN, OUTPUT);
  pinMode(RED_LED_PIN, OUTPUT);
  digitalWrite(GREEN_LED_PIN, LOW);
  digitalWrite(RED_LED_PIN, LOW);

  Serial.println("Celestial Electric Mobile Power Trailer Monitor - Cloud Edition REV 2.0");

  initProperties();
  ArduinoCloud.begin(ArduinoIoTPreferredConnection);
  setDebugMessageLevel(2);
  ArduinoCloud.printDebugInfo();

  bmeReady = beginBME();
  if (!bmeReady) Serial.println("BME280 NOT found at boot - will retry each cycle.");

  // --- OPTIONAL: hardware watchdog (auto-reset on a hung loop) ---
  // UNO R4 core provides a WDT. If your core version differs, comment out.
  //   #include "WDT.h"   // add near the top includes
  //   WDT.begin(4000);   // ~4 s timeout; call WDT.refresh() in loop()
}

void loop() {
  ArduinoCloud.update();     // service the radio every pass - keep OUTSIDE the timer gate
  // WDT.refresh();          // <- uncomment if watchdog enabled

  unsigned long now = millis();
  if (now - lastSensorRead < SENSOR_INTERVAL_MS) return;
  lastSensorRead = now;

  readAndPublish();
}

void readAndPublish() {
  // ---- BME280 read with NaN detection + auto-recovery ----
  if (bmeReady) {
    float tC = bme.readTemperature();
    float rh = bme.readHumidity();
    if (isnan(tC) || isnan(rh)) {
      bmeReady = false;      // sensor dropped off the bus; recover next cycle
    } else {
      temperatureF    = (tC * 9.0 / 5.0) + 32.0;
      humidityPercent = rh;
    }
  }
  if (!bmeReady) {
    bmeReady = beginBME();   // non-blocking retry
    if (bmeReady) Serial.println("BME280 recovered.");
  }
  sensorFault = !bmeReady;

  // ---- Discrete inputs through the glitch filter ----
  bool doorRaw  = (digitalRead(DOOR_CONTACT_PIN) == HIGH);              // HIGH = open
  bool waterRaw = (digitalRead(WATER_SENSOR_PIN) == WATER_DETECTED_STATE);
  doorOpen      = updateDebounced(doorDb,  doorRaw);
  waterDetected = updateDebounced(waterDb, waterRaw);

  // ---- Alert roll-up ----
  bool highTemp     = !sensorFault && (temperatureF   >= HIGH_TEMP_F_THRESHOLD);
  bool highHumidity = !sensorFault && (humidityPercent >= HIGH_HUMIDITY_THRESHOLD);
  systemAlert = waterDetected || doorOpen || highTemp || highHumidity || sensorFault;

  digitalWrite(GREEN_LED_PIN, systemAlert ? LOW : HIGH);
  digitalWrite(RED_LED_PIN,   systemAlert ? HIGH : LOW);

  // --- OPTIONAL: publish WiFi signal strength for field placement ---
  // Requires a 'signalStrength' (int) READ variable in thingProperties.h:
  //   signalStrength = WiFi.RSSI();

  // ---- Serial mirror (bench verification) ----
  Serial.println("----------------------------------------");
  if (!sensorFault) {
    Serial.print("Temp: ");     Serial.print(temperatureF, 1);    Serial.println(" F");
    Serial.print("Humidity: "); Serial.print(humidityPercent, 1); Serial.println(" %");
  } else {
    Serial.println("Temp/Humidity: SENSOR FAULT (retrying)");
  }
  Serial.print("Door: ");   Serial.println(doorOpen ? "OPEN" : "CLOSED");
  Serial.print("Water: ");  Serial.println(waterDetected ? "WATER DETECTED" : "DRY");
  Serial.print("Status: "); Serial.println(systemAlert ? "ALERT" : "NORMAL");
  Serial.print("Cloud: ");  Serial.println(ArduinoCloud.connected() ? "CONNECTED" : "OFFLINE (local monitoring active)");
}
