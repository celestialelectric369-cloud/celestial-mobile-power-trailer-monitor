/*
  thingProperties.h  —  REFERENCE COPY
  Celestial Electric Mobile Power Trailer Monitor (Arduino Cloud)

  IMPORTANT: Arduino Cloud GENERATES this file automatically when you create the
  Thing and add variables in the web editor. That generated version also carries
  your Device ID and connects the board's on-board crypto (ECC608) for secure
  auth. Prefer the generated file. Use THIS copy only as a structural reference,
  or for a fully manual build where the device is already provisioned.

  All five variables are READ (device -> cloud), so no callbacks are declared.

  REV 2.0 | Doc: CEL-MPT-FW-002 | pairs with firmware REV 2.0.
*/

#include <ArduinoIoTCloud.h>
#include <Arduino_ConnectionHandler.h>
#include "arduino_secrets.h"

const char SSID[] = SECRET_SSID;            // WiFi network name
const char PASS[] = SECRET_OPTIONAL_PASS;   // WiFi password

// -------- Cloud variables (names must match the dashboard fields) --------
float temperatureF;
float humidityPercent;
bool  waterDetected;
bool  doorOpen;
bool  systemAlert;

// -------- OPTIONAL diagnostics (uncomment here AND in the sketch) --------
// A moving trailer benefits from knowing WiFi signal at the install spot.
// int signalStrength;   // dBm RSSI; add a matching Int variable to the Thing

void initProperties() {
  // Telemetry split:
  //   Environmental floats -> 30 s time policy (steady trend + liveness heartbeat)
  //   Alert-state booleans -> ON_CHANGE (instant push the moment a state flips)
  //
  // The 30 s float publish doubles as a keep-alive: because at least one variable
  // reports every 30 s, the Thing's "last update" never looks stale even when
  // nothing is alarming. No separate heartbeat variable required.

  ArduinoCloud.addProperty(temperatureF,    READ, 30 * SECONDS, NULL);
  ArduinoCloud.addProperty(humidityPercent, READ, 30 * SECONDS, NULL);
  ArduinoCloud.addProperty(waterDetected,   READ, ON_CHANGE,    NULL);
  ArduinoCloud.addProperty(doorOpen,        READ, ON_CHANGE,    NULL);
  ArduinoCloud.addProperty(systemAlert,     READ, ON_CHANGE,    NULL);

  // Metered/cellular backhaul? Slow the float traffic further -> 60 * SECONDS.

  // OPTIONAL diagnostics:
  // ArduinoCloud.addProperty(signalStrength, READ, 60 * SECONDS, NULL);
}

WiFiConnectionHandler ArduinoIoTPreferredConnection(SSID, PASS);
