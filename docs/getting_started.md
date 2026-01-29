# AgriAgents - Getting Started

## Prerequisites

- Python 3.8+
- Node.js (optional, for live server)
- ESP32 with Arduino IDE (optional, for hardware)

---

## Quick Start (Demo Mode)

### 1. Clone Repository
```bash
git clone https://github.com/aashishniranjanb/AgriAgents.git
cd AgriAgents
```

### 2. Install Dependencies
```bash
cd backend/server
pip install -r requirements.txt
```

### 3. Start Backend Server
```bash
python server.py
```

You should see:
```
==================================================
🌱 AgriAgents - Multi-Agent Backend
   Impact Metrics + Decision Timeline enabled
==================================================

🟢 Server running on http://localhost:5000
```

### 4. Start Demo Data Generator
Open a new terminal:
```bash
cd backend/server
python demo_scenario.py
```

### 5. Open Dashboard
Open `frontend/web/index.html` in your browser.

Or use Python's HTTP server:
```bash
cd frontend/web
python -m http.server 8080
# Open http://localhost:8080
```

---

## Hardware Setup (ESP32)

### 1. Wire Components
```
ESP32        Component
─────        ─────────
GPIO4   →    DHT11 Data
GPIO34  →    Soil Sensor (Analog)
GPIO35  →    LDR (Analog)
GPIO26  →    Relay IN
3.3V    →    DHT11 VCC, Soil VCC
GND     →    All GNDs
5V      →    Relay VCC
```

### 2. Configure Firmware
Edit `firmware/esp32/esp32_main.ino`:
```cpp
const char* WIFI_SSID = "YourWiFiName";
const char* WIFI_PASSWORD = "YourWiFiPassword";
const char* SERVER_URL = "http://192.168.1.x:5000/data";
```

### 3. Flash ESP32
1. Open Arduino IDE
2. Select Board: ESP32 Dev Module
3. Upload firmware

---

## Project Structure

```
agriagents/
├── backend/
│   └── server/
│       ├── server.py           # Main backend
│       ├── agentic_engine.py   # Decision engine
│       ├── demo_scenario.py    # Demo data generator
│       └── requirements.txt    # Python dependencies
├── frontend/
│   └── web/
│       └── index.html          # Dashboard UI
├── firmware/
│   └── esp32/
│       └── esp32_main.ino      # ESP32 firmware
├── docs/
│   ├── architecture.md
│   ├── agents.md
│   ├── api.md
│   ├── firmware.md
│   ├── demo_guide.md
│   └── getting_started.md
└── README.md
```

---

## Running Demos

### Scenario Buttons
| Button | Effect |
|--------|--------|
| 💧 Normal | Standard operation |
| 🌧️ Rain Incoming | Rain forecast override |
| ⚠️ Pump Failure | Emergency lockout |

### What to Watch
1. **Agent cards** update with sensor data
2. **Interaction arrows** change color on overrides
3. **Impact metrics** accumulate savings
4. **Timeline** shows decision history

---

## Troubleshooting

### Backend not starting
```bash
pip install flask flask-cors
```

### Dashboard shows "Backend unreachable"
- Ensure server is running on port 5000
- Check for CORS errors in browser console
- Verify API URL in localStorage

### No data appearing
- Run `demo_scenario.py` in separate terminal
- Check server terminal for incoming telemetry

---

## Next Steps

1. Read [Architecture](./architecture.md) for system overview
2. Read [Agents](./agents.md) for agent specifications
3. Read [Demo Guide](./demo_guide.md) for presentation tips
4. Read [API Reference](./api.md) for integration
