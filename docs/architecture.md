# AgriAgents System Architecture

## Overview

AgriAgents is a multi-agent AI system for climate-aware irrigation that uses explicit agent boundaries, utility-based decision making, and transparent reasoning to make safe, explainable irrigation decisions.

---

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      ESP32 EDGE DEVICE                          │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐        │
│  │   DHT11  │  │  Soil    │  │   LDR    │  │  Relay   │        │
│  │  Sensor  │  │ Moisture │  │ (Light)  │  │  Module  │        │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘        │
│       │             │             │             │               │
│       └─────────────┴─────────────┴─────────────┘               │
│                         │                                       │
│  ┌──────────────────────▼────────────────────────────────────┐  │
│  │              Finite State Machine (FSM)                   │  │
│  │  States: IDLE → IRRIGATING → COOLDOWN → FAULT            │  │
│  │  Safety: Hysteresis, Max Runtime, Sensor Fault Detection │  │
│  └──────────────────────┬────────────────────────────────────┘  │
└─────────────────────────┼───────────────────────────────────────┘
                          │ HTTP POST (JSON)
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                    BACKEND ORCHESTRATOR                         │
│                      (Flask Server)                             │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                   AGENT PIPELINE                          │  │
│  │                                                           │  │
│  │  ┌─────────────┐   ┌─────────────┐   ┌─────────────┐      │  │
│  │  │   FIELD     │   │  CLIMATE    │   │  DECISION   │      │  │
│  │  │   AGENT     │──▶│   AGENT     │──▶│   AGENT     │      │  │
│  │  │             │   │             │   │             │      │  │
│  │  │ • Soil %    │   │ • Rain ETA  │   │ • HOLD      │      │  │
│  │  │ • Temp °C   │   │ • Override  │   │ • IRRIGATE  │      │  │
│  │  │ • Status    │   │ • Evap Risk │   │ • EMERGENCY │      │  │
│  │  └─────────────┘   └─────────────┘   └──────┬──────┘      │  │
│  │                                             │              │  │
│  │                                             ▼              │  │
│  │                                    ┌─────────────┐         │  │
│  │                                    │   FARMER    │         │  │
│  │                                    │  ASSISTANT  │         │  │
│  │                                    │  (GenAI)    │         │  │
│  │                                    └─────────────┘         │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
│  ┌─────────────────┐  ┌─────────────────┐                      │
│  │ Impact Metrics  │  │ Decision        │                      │
│  │ • Water Saved   │  │ Timeline        │                      │
│  │ • Cycles Avoided│  │ (Ring Buffer)   │                      │
│  └─────────────────┘  └─────────────────┘                      │
└─────────────────────────┬───────────────────────────────────────┘
                          │ REST API
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                    WEB DASHBOARD                                 │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐        ││
│  │ │  Field   │ │ Climate  │ │ Decision │ │  Farmer  │        ││
│  │ │  Agent   │ │  Agent   │ │  Agent   │ │ Assistant│        ││
│  │ └──────────┘ └──────────┘ └──────────┘ └──────────┘        ││
│  ├─────────────────────────────────────────────────────────────┤│
│  │           Agent Interaction Flow (Color-coded Arrows)       ││
│  ├─────────────────────────────────────────────────────────────┤│
│  │  ┌────────────────┐  ┌────────────────┐                    ││
│  │  │  Water Saved   │  │ Pump Cycles    │                    ││
│  │  │     X.X L      │  │   Avoided: N   │                    ││
│  │  └────────────────┘  └────────────────┘                    ││
│  ├─────────────────────────────────────────────────────────────┤│
│  │              Decision Timeline (Last 30 entries)            ││
│  └─────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────┘
```

---

## Data Flow

### 1. Sensor Telemetry Path
```
ESP32 sensors → JSON payload → POST /data → Agent Pipeline → Response
```

### 2. Dashboard Polling Path
```
Dashboard → GET /state → Agent outputs + Metrics → UI Update
```

### 3. Timeline Polling Path
```
Dashboard → GET /timeline → Decision history → Timeline UI
```

---

## Communication Protocol

### Telemetry Payload (ESP32 → Backend)
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

### State Response (Backend → Dashboard)
```json
{
  "timestamp": "2026-01-29T18:05:00Z",
  "agents": {
    "field_agent": {...},
    "climate_agent": {...},
    "decision_agent": {...},
    "farmer_assistant": {...}
  },
  "impact_metrics": {
    "water_saved_liters": 40.0,
    "pump_cycles_avoided": 4
  }
}
```

---

## Design Principles

1. **Edge-First Safety** — Critical decisions happen on ESP32
2. **Explicit Agent Boundaries** — Each agent has defined inputs/outputs
3. **Transparent Reasoning** — All decisions are explainable
4. **Fail-Safe Operation** — System fails to safe state
5. **Demo-Ready** — Scenario control for presentations
