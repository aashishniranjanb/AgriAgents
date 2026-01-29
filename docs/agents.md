# AgriAgents - Agent Specifications

## Overview

AgriAgents uses a **4-agent architecture** where each agent has a single responsibility and explicit inputs/outputs. Agents interact through a defined pipeline, and override logic is transparent.

---

## Agent 1: Field Agent 🟫

### Purpose
Interprets raw sensor data into normalized, actionable field status.

### Inputs
| Field | Type | Source |
|-------|------|--------|
| soil | float | Capacitive soil sensor (0-100%) |
| temperature | float | DHT11 sensor (°C) |
| light | int | LDR sensor (raw ADC value) |

### Outputs
```json
{
  "soil_moisture": 28.5,
  "soil_status": "CRITICAL",
  "temperature": 31.2,
  "heat_stress": "HIGH",
  "pump_state": "OFF"
}
```

### Logic
| Soil % | Status |
|--------|--------|
| < 25 | CRITICAL |
| 25-35 | LOW |
| > 35 | OK |

| Temperature | Heat Stress |
|-------------|-------------|
| > 32°C | HIGH |
| ≤ 32°C | NORMAL |

---

## Agent 2: Climate Agent 🌦️

### Purpose
Reasons about upcoming weather events that affect irrigation decisions.

### Inputs
| Field | Type | Source |
|-------|------|--------|
| scenario_mode | string | Demo control or weather API |
| rain_eta | int | Minutes until rain (demo) |

### Outputs
```json
{
  "rain_expected": true,
  "rain_eta_minutes": 45,
  "evaporation_risk": "HIGH"
}
```

### Logic
- If rain is expected within 120 minutes → can override irrigation
- Evaporation risk based on temperature (>32°C = HIGH)

### Agent Interaction
**Climate Agent can OVERRIDE Field Agent:**
- If `rain_expected == true` AND `soil < 35%`
- Decision Agent receives override signal

---

## Agent 3: Decision Agent 🧠

### Purpose
Makes final irrigation decision using utility-based scoring and agent interactions.

### Inputs
| Field | Type | Source |
|-------|------|--------|
| sensor_data | object | Field Agent |
| climate_override | boolean | Climate Agent |
| last_action_time | datetime | System memory |

### Outputs
```json
{
  "decision": "HOLD",
  "confidence": 0.91,
  "utility_score": 42,
  "reason": "Rain expected soon despite dry soil"
}
```

### Decision States
| State | Meaning | Pump |
|-------|---------|------|
| IRRIGATE | Start watering | ON |
| HOLD | Wait for better conditions | OFF |
| DELAY | Temporary pause | OFF |
| EMERGENCY_STOP | Safety lockout | OFF |

### Utility Scoring
```python
utility = 0

# Soil contribution (0-50 points)
if soil < 30:
    utility += (30 - soil) * 2

# Temperature contribution (0-20 points)
if temp > 30:
    utility += (temp - 30) * 2

# Light contribution (0-10 points)
if light > 2000:
    utility += 10

# Decision thresholds
if utility > IRRIGATE_THRESHOLD:
    decision = "IRRIGATE"
elif utility > DELAY_THRESHOLD:
    decision = "DELAY"
else:
    decision = "HOLD"
```

### Override Logic
```python
if climate_agent["rain_expected"] and soil < 35:
    decision = "HOLD"  # Rain override
    
if scenario["mode"] == "PUMP_FAIL":
    decision = "EMERGENCY_STOP"  # Safety override
```

### Confidence Calculation
```python
# Distance from decision boundary
distance = abs(utility - threshold)
confidence = min(1.0, 0.5 + (distance / max_distance) * 0.5)
```

---

## Agent 4: Farmer Assistant 🧑‍🌾

### Purpose
Translates technical decisions into human-readable explanations for farmers.

### Inputs
| Field | Type | Source |
|-------|------|--------|
| decision | string | Decision Agent |
| rain_expected | boolean | Climate Agent |
| soil_status | string | Field Agent |

### Outputs
```json
{
  "message": "🌧️ Rain is expected in 45 minutes. Irrigation is delayed to save water and avoid unnecessary pump usage."
}
```

### Message Templates

| Scenario | Message |
|----------|---------|
| Rain Expected | "🌧️ Rain is expected in {eta}. Irrigation is delayed to save water..." |
| Irrigation Active | "💧 Soil moisture is critically low. Irrigation has been activated..." |
| System Normal | "✅ Soil moisture is adequate. System is monitoring..." |
| Pump Failure | "⚠️ Pump failure detected. Please check the water pump and tank..." |

---

## Agent Interaction Flow

```
Field Agent ──────┬──────▶ Decision Agent ──────▶ Farmer Assistant
                  │              ▲
Climate Agent ────┴──────────────┘
                     (override)
```

### Arrow Color Logic (UI)
| Condition | Arrow Color | Meaning |
|-----------|-------------|---------|
| Normal flow | 🟢 Green | Information passed |
| Soil critical | 🟡 Yellow | Warning state |
| Climate override | 🔴 Red | Decision blocked |
| Emergency | 🔴 Red | System locked |

---

## Impact Metrics

### Water Saved
```python
if soil < 30 and decision == "HOLD" and rain_expected:
    water_saved += PUMP_FLOW_LPM * 1  # 10L per avoided cycle
```

### Pump Cycles Avoided
```python
if would_irrigate and decision == "HOLD":
    cycles_avoided += 1
```

**Demo Assumption:** Pump flow rate = 10 liters/minute
