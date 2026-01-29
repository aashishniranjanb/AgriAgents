# 🌱 AgriAgents
## Multi-Agent AI for Climate-Aware Irrigation

AgriAgents is a **production-style multi-agent AI system** for intelligent irrigation that reasons over **field conditions, upcoming climate events, and system health** to make safe, explainable decisions.

Instead of relying on rigid thresholds, AgriAgents separates intelligence into **specialized AI agents**, each responsible for a specific aspect of farm decision-making.

---

## 🤖 Agent Architecture

AgriAgents uses four explicit AI agents:

| Agent | Responsibility |
|------|----------------|
| 🟫 Field Agent | Interprets real-time sensor conditions |
| 🌦️ Climate Agent | Reasons about upcoming weather events |
| 🧠 Decision Agent | Selects optimal actions using utility scoring |
| 🧑‍🌾 Farmer Assistant | Explains decisions and provides guidance |

This separation improves **safety, explainability, and extensibility**.

---

## 🎯 Core Value Proposition

> **"AgriAgents prevents unnecessary irrigation by reasoning about future weather instead of blindly reacting to dry soil."**

---

## 🧠 System Architecture

```
ESP32 (Sensors + Relay)
        ↓
Telemetry (HTTP / JSON)
        ↓
Backend Orchestrator (Flask)
  • Field Agent (sensor normalization)
  • Climate Agent (weather reasoning)
  • Decision Agent (utility scoring)
  • Farmer Assistant (GenAI explanations)
        ↓
    Web Dashboard
  • 4-Agent UI
  • Live Decisions
  • Explainable Reasoning
```

---

## 🔧 Hardware Used

- ESP32
- DHT11 (Temperature & Humidity)
- Capacitive Soil Moisture Sensor
- LDR (Light Intensity)
- Relay Module (Water Pump)

> ⚠️ Sensors are hobby-grade for demonstration. Architecture supports industrial sensors.

---

## 📂 Repository Structure

```
agriagents/
├── firmware/
│   └── esp32/
│       └── esp32_main.ino
├── backend/
│   └── server/
│       ├── server.py
│       ├── agentic_engine.py
│       ├── demo_scenario.py
│       └── requirements.txt
├── frontend/
│   └── web/
│       └── index.html
├── docs/
├── .gitignore
└── README.md
```

---

## 🚀 Quick Start

### Backend
```bash
cd backend/server
pip install -r requirements.txt
python server.py
```

### Demo Scenario
```bash
python demo_scenario.py
```

### Dashboard
Open `frontend/web/index.html` in your browser.

---

## 🛡️ Safety & Reliability

- ✅ Edge-level FSM prevents unsafe actuation
- ✅ Hysteresis prevents relay chatter
- ✅ Pump runtime hard-limited
- ✅ Sensor faults lock irrigation
- ✅ Cloud failures cannot cause unsafe behavior

---

## 📌 Disclaimer

This project is a **production-grade showcase**, not an agricultural product.
It demonstrates **architecture, safety, and reasoning**, not agronomic guarantees.

---

## 👤 Author

Built as a **serious engineering demonstration** of Multi-Agent AI + IoT Systems.
