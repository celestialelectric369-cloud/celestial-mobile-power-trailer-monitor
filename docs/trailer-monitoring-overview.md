# Trailer Monitoring Overview

## Project summary

The Celestial Electric Mobile Power Trailer Monitor is a low-voltage Arduino monitoring concept for a real mobile power trailer build.

The system is intended to provide visibility into trailer conditions and support equipment without controlling the trailer power system.

## Monitored assets

- Duracell 12V battery bank
- EcoFlow portable power system
- Trailer interior temperature
- Trailer interior humidity
- Water/leak status
- Door/contact status
- Local normal/alert indication
- Planned Arduino Cloud dashboard

## Battery bank

The trailer battery bank consists of two Duracell 12V lead-acid batteries rated 810 CCA each, wired in parallel.

Because the batteries are wired in parallel, the bank remains a 12V nominal system.

CCA is not an energy-capacity rating. Runtime estimates require the amp-hour rating, reserve-capacity rating, or battery group size.

## EcoFlow system

The EcoFlow unit is treated as a separate mobile power source. This first version documents EcoFlow status as part of the monitoring concept. Direct EcoFlow data integration may be added later if a safe and supported interface is available.

## Control boundary

The Arduino monitor does not control charging, discharging, inverting, transferring, generator operation, battery protection, or safety functions.
