"""
AgroSense AI - Agentic Backend Orchestrator
Architecture:
- Device Shadow (Digital Twin)
- Tool-using Agent (Explicit Orchestration)
- Explainable AI
- Demo-safe (Fake or Real Data)

TOOLS:
1. Weather Forecast (OpenWeather)
2. Crop Doctor (Gemini GenAI)
3. Hardware Diagnostics
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime, timedelta
import requests
import google.generativeai as genai

from agentic_engine import agentic_decision, generate_explanation

# ==================================================
# 🔐 API KEYS (SET YOURS)
# ==================================================
OPENWEATHER_KEY = "YOUR_OPENWEATHER_API_KEY"
GOOGLE_API_KEY = "YOUR_GOOGLE_API_KEY"

genai.configure(api_key=GOOGLE_API_KEY)
genai_model = genai.GenerativeModel("gemini-pro")

# ==================================================
# 🌐 APP INIT
# ==================================================
app = Flask(__name__)
CORS(app)

# ==================================================
# 🧠 DEVICE SHADOW (STATE MEMORY)
# ==================================================
SYSTEM_STATE = {
    "last_action_time": None,
    "last_pump_command": None,
    "soil_history": [],
    "latest_snapshot": {
        "status": "WAITING_FOR_DATA"
    }
}

# ==================================================
# 🛠️ TOOL 1 — WEATHER FORECAST
# ==================================================
def check_rain_forecast(lat=12.97, lon=77.59):
    url = "https://api.openweathermap.org/data/2.5/forecast"
    params = {
        "lat": lat,
        "lon": lon,
        "appid": OPENWEATHER_KEY,
        "units": "metric"
    }

    try:
        data = requests.get(url, params=params, timeout=3).json()
        for entry in data.get("list", [])[:4]:  # ~12 hours
            if "rain" in entry:
                return True, entry["dt_txt"]
    except Exception:
        pass

    return False, None

# ==================================================
# �️ TOOL 2 — CROP DOCTOR (GENAI)
# ==================================================
def crop_doctor(soil_trend):
    prompt = f"""
You are an agronomy assistant.
Given this soil moisture trend over time:

{soil_trend}

Identify ONE meaningful insight and ONE practical recommendation.
Do not mention AI or models.
"""

    try:
        response = genai_model.generate_content(prompt)
        return response.text.strip()
    except Exception:
        return "Trend analysis unavailable at the moment."

# ==================================================
# �️ TOOL 3 — HARDWARE DIAGNOSTICS
# ==================================================
def diagnose_hardware(soil_history, last_command):
    if last_command != "IRRIGATE":
        return None

    if len(soil_history) < 3:
        return None

    # Check if soil hasn't increased after irrigation
    if soil_history[-1] <= soil_history[-3]:
        return "⚠️ Possible pump failure or empty water tank detected."

    return None

# ==================================================
# 📡 TELEMETRY INGEST
# ==================================================
@app.route("/data", methods=["POST"])
def ingest_data():
    payload = request.get_json(force=True)
    print("📡 Incoming:", payload)

    sensors_raw = payload.get("sensors", {})

    sensor_data = {
        "soil": float(sensors_raw.get("soil", 0)),
        "temperature": float(sensors_raw.get("temp", 0)),
        "light": int(sensors_raw.get("light", 0))
    }

    # ----------------------------
    # Update history
    # ----------------------------
    SYSTEM_STATE["soil_history"].append(sensor_data["soil"])
    SYSTEM_STATE["soil_history"] = SYSTEM_STATE["soil_history"][-20:]

    # ----------------------------
    # BASE AGENT DECISION
    # ----------------------------
    agent_output = agentic_decision(
        sensor_data=sensor_data,
        last_action_time=SYSTEM_STATE["last_action_time"]
    )

    decision = agent_output["decision"]
    agent_logs = []

    # ----------------------------
    # TOOL 1: WEATHER AWARENESS
    # ----------------------------
    if decision == "IRRIGATE" and sensor_data["soil"] < 35:
        rain, time = check_rain_forecast()
        if rain:
            decision = "HOLD"
            agent_logs.append(f"🌧️ Rain forecast detected ({time}) → Skipping irrigation")

    # ----------------------------
    # TOOL 2: CROP DOCTOR (GENAI)
    # ----------------------------
    insight = None
    if len(SYSTEM_STATE["soil_history"]) >= 6:
        insight = crop_doctor(SYSTEM_STATE["soil_history"][-6:])
        agent_logs.append("🌱 Crop Doctor analysis completed")

    # ----------------------------
    # TOOL 3: HARDWARE DIAGNOSTICS
    # ----------------------------
    diagnostic_alert = diagnose_hardware(
        SYSTEM_STATE["soil_history"],
        SYSTEM_STATE["last_pump_command"]
    )

    if diagnostic_alert:
        decision = "EMERGENCY_STOP"
        agent_logs.append(diagnostic_alert)

    # ----------------------------
    # STATE MEMORY UPDATE
    # ----------------------------
    if decision == "IRRIGATE":
        SYSTEM_STATE["last_action_time"] = datetime.utcnow()

    SYSTEM_STATE["last_pump_command"] = decision

    # ----------------------------
    # EXPLANATION
    # ----------------------------
    explanation = generate_explanation(agent_output)

    # ----------------------------
    # UPDATE DEVICE SHADOW
    # ----------------------------
    SYSTEM_STATE["latest_snapshot"] = {
        "device_id": payload.get("device_id", "simulator"),
        "sensors": sensor_data,
        "agent_analysis": {
            **agent_output,
            "decision": decision
        },
        "agent_logs": agent_logs,
        "crop_insight": insight,
        "explanation": explanation,
        "last_updated": datetime.utcnow().isoformat()
    }

    return jsonify({"status": "ok", "decision": decision}), 200

# ==================================================
# 🌐 DASHBOARD API
# ==================================================
@app.route("/state", methods=["GET"])
def get_state():
    return jsonify(SYSTEM_STATE["latest_snapshot"]), 200

# ==================================================
# 🚀 ENTRYPOINT
# ==================================================
if __name__ == "__main__":
    print("🟢 AgroSense AI Agentic Backend Running (Port 5000)")
    app.run(host="0.0.0.0", port=5000, debug=True)
