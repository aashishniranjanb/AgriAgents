# AgriAgents - ESP32 Firmware Documentation

## Overview

The ESP32 firmware implements a production-grade, fault-tolerant irrigation controller with edge-level safety mechanisms.

---

## Hardware Requirements

| Component | Model | Purpose |
|-----------|-------|---------|
| Microcontroller | ESP32 | WiFi + Processing |
| Temperature/Humidity | DHT11 | Climate monitoring |
| Soil Moisture | Capacitive | Irrigation trigger |
| Light Sensor | LDR | Day/night detection |
| Pump Control | 5V Relay | Water pump switching |

### Pin Configuration
```cpp
#define DHT_PIN         4     // DHT11 data pin
#define SOIL_PIN        34    // Analog input
#define LDR_PIN         35    // Analog input
#define RELAY_PIN       26    // Relay control (active LOW)
```

---

## Finite State Machine (FSM)

```
        ┌──────────────────────────────────────────────┐
        │                                              │
        ▼                                              │
    ┌───────┐     Soil < Threshold     ┌───────────┐  │
    │ IDLE  │ ────────────────────────▶│ IRRIGATING│  │
    └───────┘                          └─────┬─────┘  │
        ▲                                    │        │
        │                                    │        │
        │    Cooldown Complete         Max Runtime    │
        │         ◀────────────────────     │        │
        │                    │              ▼        │
        │              ┌─────┴─────┐                 │
        │              │ COOLDOWN  │                 │
        │              └───────────┘                 │
        │                                            │
        │              ┌───────────┐                 │
        └──────────────┤   FAULT   │◀────────────────┘
                       └───────────┘    Sensor Invalid
```

### States

| State | Description | Pump |
|-------|-------------|------|
| IDLE | Waiting for trigger | OFF |
| IRRIGATING | Active watering | ON |
| COOLDOWN | Post-irrigation delay | OFF |
| FAULT | Sensor error lockout | OFF |

---

## Safety Mechanisms

### 1. Hysteresis (Anti-Chatter)
```cpp
#define SOIL_ON         25    // Turn pump ON below this
#define SOIL_OFF        35    // Turn pump OFF above this
```
Prevents rapid on/off cycling near threshold.

### 2. Maximum Pump Runtime
```cpp
#define MAX_PUMP_RUNTIME    180000    // 3 minutes max
```
Automatically stops pump even if conditions persist.

### 3. Cooldown Period
```cpp
#define COOLDOWN_TIME       120000    // 2 minutes wait
```
Prevents immediate restart after pump stops.

### 4. Sensor Fault Detection
```cpp
if (isnan(temp) || isnan(humidity) || soil < 0 || soil > 100) {
    enterState(FAULT);
}
```
Invalid sensor readings lock the system.

### 5. Non-Blocking Operation
```cpp
// Uses millis() for timing, never blocks
if (millis() - lastSensorRead >= SENSOR_INTERVAL) {
    readSensors();
}
```

---

## Telemetry Protocol

### JSON Payload
```json
{
  "device_id": "esp32_main",
  "sensors": {
    "soil": 28.5,
    "temp": 31.2,
    "light": 2500
  }
}
```

### Transmission Interval
```cpp
#define TELEMETRY_INTERVAL  10000   // Every 10 seconds
```

---

## WiFi Reconnection

```cpp
// Non-blocking reconnection
if (WiFi.status() != WL_CONNECTED) {
    if (millis() - lastWifiRetry >= WIFI_RETRY_INTERVAL) {
        WiFi.reconnect();
        lastWifiRetry = millis();
    }
}
```

---

## Configuration

Edit these values in `esp32_main.ino`:

```cpp
const char* WIFI_SSID = "<WIFI_SSID>";
const char* WIFI_PASSWORD = "<WIFI_PASSWORD>";
const char* SERVER_URL = "http://<SERVER_IP>:5000/data";
```

---

## Dependencies

```
#include <WiFi.h>
#include <HTTPClient.h>
#include <DHT.h>
#include <ArduinoJson.h>
```

Install via Arduino Library Manager:
- DHT sensor library
- ArduinoJson (v6+)

---

## Flashing Instructions

1. Open `firmware/esp32/esp32_main.ino` in Arduino IDE
2. Select board: "ESP32 Dev Module"
3. Set WiFi credentials
4. Set backend server URL
5. Upload

---

## LED Indicators (Optional)

| LED State | Meaning |
|-----------|---------|
| Solid | System OK |
| Blinking | Connecting WiFi |
| Off | Fault state |
