# AgriAgents - Demo Scenarios Guide

## Overview

AgriAgents includes a scenario control system for demos. This allows you to show different agent behaviors without actual hardware or weather conditions.

---

## Scenario Modes

### 1. 💧 NORMAL Mode
**Purpose:** Standard sensor-driven operation

**Behavior:**
- Agents respond to incoming sensor data
- No weather override
- Impact metrics reset to zero

**How to trigger:**
```
Click "💧 Normal" button
```
or
```bash
curl -X POST http://localhost:5000/scenario \
  -H "Content-Type: application/json" \
  -d '{"mode": "NORMAL"}'
```

---

### 2. 🌧️ RAIN Mode
**Purpose:** Demonstrates climate-aware decision override

**Behavior:**
- Rain forecast injected (90-minute countdown)
- Climate Agent reports rain_expected = true
- Decision Agent overrides to HOLD
- Interaction arrow turns RED
- Water saved counter increases

**Timeline:**
```
T+0m:  Rain ETA: 90 min  → HOLD
T+1m:  Rain ETA: 87 min  → HOLD
T+2m:  Rain ETA: 84 min  → HOLD
...
T+30m: Rain ETA: 0 min   → HOLD
```

**How to trigger:**
```
Click "🌧️ Rain Incoming" button
```

**What to say:**
> "Watch how the Climate Agent detects incoming rain and overrides the irrigation decision. The arrow turns red, showing the override."

---

### 3. ⚠️ PUMP_FAIL Mode
**Purpose:** Demonstrates safety lockout

**Behavior:**
- Decision Agent immediately returns EMERGENCY_STOP
- Interaction arrow turns RED
- Farmer Assistant shows warning message

**How to trigger:**
```
Click "⚠️ Pump Failure" button
```

**What to say:**
> "The system detects a pump anomaly and immediately locks irrigation for safety. This is edge-level protection."

---

## Demo Flow (Recommended)

### Step 1: Start with Normal
1. Click **💧 Normal**
2. Show sensor data flowing
3. Explain agent cards

### Step 2: Trigger Rain Override
4. Click **🌧️ Rain Incoming**
5. Watch:
   - Climate Agent → "🌧️ YES"
   - Arrow turns RED
   - Decision → HOLD
   - Water Saved increases
   - Timeline fills with HOLD entries

### Step 3: Show Impact
6. Point to **Water Saved** counter
7. Point to **Pump Cycles Avoided**
8. Explain value creation

### Step 4: (Optional) Show Safety
9. Click **⚠️ Pump Failure**
10. Show EMERGENCY_STOP
11. Explain safety lockout

### Step 5: Return to Normal
12. Click **💧 Normal**
13. Show system recovery

---

## Demo Data Generator

### `demo_scenario.py`
Automatically cycles through a realistic scenario:

```
Phase 1-2:   Soil 32% → 28%    (Normal)
Phase 3-8:   Soil 24% → 15%    (Rain countdown)
Phase 9-12:  Soil 18% → 45%    (Rain occurred, recovery)
Phase 13-14: Soil 42% → 40%    (Post-rain stable)
```

**Run:**
```bash
cd backend/server
python demo_scenario.py
```

---

## Timeline Color Coding

| Decision | Color |
|----------|-------|
| IRRIGATE | 🟢 Green border |
| HOLD | 🔵 Blue border |
| EMERGENCY_STOP | 🔴 Red border |

---

## Key Demo Statements

### For Judges
> "This system prevented unnecessary irrigation because it predicted rain in 88 minutes. Traditional threshold systems would have wasted water."

### For VCs
> "AgriAgents quantifies value through avoided pump cycles and water savings. Each metric directly translates to cost savings."

### For Engineers
> "Each agent has explicit inputs and outputs. The override pattern is visible through the interaction flow."
