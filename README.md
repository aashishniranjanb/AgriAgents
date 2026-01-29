# AgroSense AI 🌱  
**Agentic AI + Edge ML Powered Smart Agriculture Platform**

AgroSense AI is a production-grade showcase project that demonstrates how
**Edge ML**, **Agentic AI**, and **Generative AI (Explainability)** can work
together in an IoT-based smart agriculture system.

This repository is structured to reflect **real-world software and hardware
engineering practices**, not a student prototype.

---

## 🎯 Project Objective

To build a **deployable, modular, and explainable** smart irrigation system that:

- Collects real-time sensor data using ESP32
- Makes **edge-level decisions** for safety and latency
- Uses **agentic AI** in the backend for goal-driven reasoning
- Uses **Generative AI** for human-readable explanations
- Displays everything on a professional web dashboard

---

## 🧠 System Architecture (High-Level)

```
[Sensors + ESP32]
       |
       |  JSON (HTTP)
       v
[Backend Server]
  • Agentic Decision Logic
  • GenAI Explainability
       |
       v
[Web Dashboard]
  • Live Sensor Data
  • AI Decisions
  • Reasoning Trace
```

---

## 🔧 Hardware Used (Current Stage)

- ESP32
- DHT11 (Temperature & Humidity)
- Capacitive Soil Moisture Sensor
- LDR (Light Sensor)
- Relay Module (Water Pump Control)

> ⚠️ Note: Some sensors are hobby-grade and are used **only for demonstration**.
The architecture is designed to support industrial-grade sensors.

---

## 🧪 AI Layers Explained (No Overclaim)

| Layer | Purpose |
|------|--------|
| Edge Logic | Fast, safe decisions (TinyML-ready) |
| Agentic AI | Goal-based reasoning (water efficiency) |
| GenAI | Explainable decisions (not control) |

---

## 📂 Repository Structure

```
firmware/   → ESP32 source code
backend/    → Agentic AI + API server
frontend/   → Web dashboard
docs/       → Architecture & diagrams
```

---

## 🚀 Roadmap (Incremental)

- [ ] ESP32 firmware (sensor → JSON)
- [ ] Backend API (receive + decide)
- [ ] Agentic AI logic
- [ ] GenAI explanations
- [ ] Web dashboard
- [ ] Edge ML (TinyML integration)

---

## 📜 Disclaimer

This project demonstrates **architecture and integration**.
It is **not claimed** to be an autonomous agronomy system.

---

## 👤 Author

Built as a **production-grade showcase** for AI + IoT system design.
