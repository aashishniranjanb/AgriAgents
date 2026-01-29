# AgriAgents - API Reference

## Base URL
```
http://localhost:5000
```

---

## Endpoints

### POST /data
Receives telemetry from ESP32 or demo simulator.

**Request:**
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

**Response:**
```json
{
  "status": "ok",
  "decision": "HOLD",
  "agents": {
    "field_agent": {
      "soil_moisture": 28.5,
      "soil_status": "LOW",
      "temperature": 31.2,
      "heat_stress": "NORMAL",
      "pump_state": "OFF"
    },
    "climate_agent": {
      "rain_expected": true,
      "rain_eta_minutes": 45,
      "evaporation_risk": "MODERATE"
    },
    "decision_agent": {
      "decision": "HOLD",
      "confidence": 0.91,
      "utility_score": 42,
      "reason": "Rain expected soon despite dry soil"
    },
    "farmer_assistant": {
      "message": "🌧️ Rain is expected in 45 minutes. Irrigation is delayed..."
    }
  },
  "impact_metrics": {
    "water_saved_liters": 30.0,
    "pump_cycles_avoided": 3
  }
}
```

---

### GET /state
Returns current system state for dashboard polling.

**Response:**
```json
{
  "timestamp": "2026-01-29T18:05:00.000Z",
  "agents": {
    "field_agent": {...},
    "climate_agent": {...},
    "decision_agent": {...},
    "farmer_assistant": {...}
  },
  "impact_metrics": {
    "water_saved_liters": 30.0,
    "pump_cycles_avoided": 3
  }
}
```

---

### GET /timeline
Returns decision history (last 30 entries).

**Response:**
```json
{
  "timeline": [
    {
      "timestamp": "2026-01-29T18:05:00.000Z",
      "soil": 28.5,
      "rain_expected": true,
      "decision": "HOLD",
      "reason": "Rain expected soon despite dry soil",
      "water_saved": 30.0,
      "pump_cycles_avoided": 3
    },
    {
      "timestamp": "2026-01-29T18:04:55.000Z",
      "soil": 29.2,
      "rain_expected": true,
      "decision": "HOLD",
      "reason": "Rain expected soon despite dry soil",
      "water_saved": 20.0,
      "pump_cycles_avoided": 2
    }
  ]
}
```

---

### POST /scenario
Controls demo scenario mode.

**Request:**
```json
{
  "mode": "RAIN"
}
```

**Modes:**
| Mode | Effect |
|------|--------|
| `NORMAL` | Standard sensor-driven operation, resets metrics |
| `RAIN` | Simulates rain forecast (90 minute countdown) |
| `PUMP_FAIL` | Triggers emergency stop scenario |

**Response:**
```json
{
  "status": "ok",
  "scenario": {
    "mode": "RAIN",
    "rain_eta": 90
  }
}
```

---

## Status Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 400 | Bad request (invalid JSON) |
| 500 | Internal server error |

---

## CORS

All endpoints have CORS enabled for frontend access from any origin.

---

## Polling Recommendations

| Endpoint | Interval | Purpose |
|----------|----------|---------|
| /state | 2000ms | Live agent updates |
| /timeline | 3000ms | Decision history |
