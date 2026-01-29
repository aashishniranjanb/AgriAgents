# AgroSense AI 🌱  
**Agentic AI–Driven Smart Irrigation (Production-Grade Showcase)**

AgroSense AI is a full-stack IoT + AI showcase that demonstrates how
**edge safety logic**, **utility-based agentic reasoning**, and
**explainable AI** can work together in a real hardware system.

This repository is intentionally designed to reflect
**real-world engineering practices**, not tutorial code.

---

## 🎯 Project Objective

To demonstrate a **safe, explainable, and state-aware smart irrigation system** that:

- Collects live data from real sensors (ESP32)
- Maintains a cloud-side **device shadow (digital twin)**
- Uses **utility-based agentic AI** for decision-making
- Explains every decision in human-readable form
- Visualizes the system through a web dashboard

---

## 🧠 System Architecture

```
ESP32 (Sensors + Relay)
        ↓
Telemetry (HTTP / JSON)
        ↓
Backend Orchestrator (Flask)
  • Device Shadow
  • Agentic AI Engine
        ↓
    Web Dashboard
  • Live Data
  • Decisions
  • Explanations
```

This mirrors the **AWS IoT Core + Lambda + Device Shadow** pattern,
implemented locally for demonstration.

---

## 🔧 Hardware Used (Actual, Not Assumed)

- ESP32
- DHT11 (Temperature & Humidity)
- Capacitive Soil Moisture Sensor
- LDR (Light Intensity)
- Relay Module (Water Pump)

> ⚠️ Note: Sensors are hobby-grade and used **only for demonstration**.
The architecture supports industrial sensors without changes.

---

## 🤖 AI Design (No Overclaim)

### Edge Layer (ESP32)
- Finite State Machine (FSM)
- Hysteresis (prevents relay chatter)
- Safety cutoff (max pump runtime)
- Operates independently of the cloud

### Agentic AI Layer (Backend)
- Utility-based decision scoring
- State-aware (uses time memory)
- Avoids threshold-only logic
- Produces confidence + reasoning trace

### Explainability
- Every decision is accompanied by:
  - Utility score
  - Confidence
  - Human-readable explanation

> Generative AI is used for **explanation**, not control.

---

## 📂 Repository Structure

```
firmware/
└── esp32/
    └── esp32_main.ino

backend/
└── server/
    ├── server.py
    └── agentic_engine.py

frontend/
└── web/
    └── index.html   (next step)

docs/
```

---

## 🚀 How to Run (Local Demo)

### Backend
```bash
cd backend/server
pip install flask flask-cors
python server.py
```

### ESP32
* Flash `esp32_main.ino`
* Set WiFi credentials
* Point `SERVER_URL` to your PC IP

### Dashboard
* Open `index.html`
* Backend must be running

---

## 🛡️ Safety & Reliability

* Relay chatter prevented via hysteresis
* Pump runtime hard-limited
* Sensor faults lock actuation
* Cloud failures cannot force unsafe behavior

---

## 📌 Disclaimer

This project is a **production-grade showcase**, not an agricultural product.
It demonstrates **architecture, safety, and reasoning**, not agronomic guarantees.

---

## 👤 Author

Built as a **serious engineering demonstration** of
IoT + Agentic AI + Explainable Systems.
