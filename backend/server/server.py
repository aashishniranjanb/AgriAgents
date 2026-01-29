"""
AgroSense AI - Agentic Backend Orchestrator (Demo-Optimized)
Architecture:
- Device Shadow (Digital Twin)
- Tool-using Agent (Weather, Diagnostics, GenAI)
- Explainable AI with clear causality
- Demo-safe with scenario support

DEMO STORY: "Rain prevents unnecessary irrigation"
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime

from agentic_engine import agentic_decision, generate_explanation

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
# 🛠️ WEATHER TOOL (Demo Mode)
# ==================================================
def check_rain_forecast(rain_minutes):
    """
    In demo mode, rain_minutes comes from the scenario generator.
    In production, this would call OpenWeather API.
    """
    if rain_minutes is None:
        return False, None, None
    
    if rain_minutes <= 0:
        return True, "Rain occurring now", 0
    
    hours = rain_minutes // 60
    mins = rain_minutes % 60
    
    if hours > 0:
        time_str = f"In {hours}h {mins}m"
    else:
        time_str = f"In {mins} minutes"
    
    return True, time_str, rain_minutes

# ==================================================
# 📡 TELEMETRY INGEST
# ==================================================
@app.route("/data", methods=["POST"])
def ingest_data():
    payload = request.get_json(force=True)
    print(f"📡 Incoming: {payload}")

    sensors_raw = payload.get("sensors", {})
    rain_minutes = payload.get("rain_minutes")

    sensor_data = {
        "soil": float(sensors_raw.get("soil", 0)),
        "temperature": float(sensors_raw.get("temp", 0)),
        "light": int(sensors_raw.get("light", 0))
    }

    # Track history
    SYSTEM_STATE["soil_history"].append(sensor_data["soil"])
    SYSTEM_STATE["soil_history"] = SYSTEM_STATE["soil_history"][-20:]

    # Base agent decision
    agent_output = agentic_decision(
        sensor_data=sensor_data,
        last_action_time=SYSTEM_STATE["last_action_time"]
    )

    decision = agent_output["decision"]
    agent_logs = []
    reason = ""
    impact = ""
    rain_forecast_display = None

    # ----------------------------
    # LOG: Sensor reading
    # ----------------------------
    agent_logs.append(f"Soil moisture: {sensor_data['soil']}% (threshold: 30%)")

    # ----------------------------
    # TOOL: Weather Forecast
    # ----------------------------
    rain_coming, rain_time_str, rain_mins = check_rain_forecast(rain_minutes)

    if rain_coming and rain_mins is not None:
        rain_forecast_display = rain_time_str
        
        if rain_mins == 0:
            agent_logs.append("🌧️ Rain detected - irrigation not needed")
            reason = "Rain is occurring now"
            impact = "Natural irrigation in progress"
            if decision == "IRRIGATE":
                decision = "HOLD"
        elif rain_mins > 0 and rain_mins <= 120:
            agent_logs.append(f"🌧️ Weather API: Rain forecast {rain_time_str}")
            agent_logs.append("🧠 Decision override: HOLD irrigation")
            
            # Calculate water savings
            water_saved = int((30 - sensor_data["soil"]) * 3)  # ~3L per % deficit
            
            reason = f"Rain expected {rain_time_str.lower()}"
            impact = f"~{water_saved} liters of water saved"
            
            if decision == "IRRIGATE":
                decision = "HOLD"
                agent_logs.append(f"💧 Estimated savings: {water_saved}L water")
        elif rain_mins < 0:
            agent_logs.append("🌧️ Recent rain detected - soil recovering")
            reason = "Soil recovering from recent rain"
            impact = "No irrigation needed"
            rain_forecast_display = "Rained recently"
    else:
        rain_forecast_display = "No rain expected"
        
        if decision == "IRRIGATE":
            reason = f"Soil critically dry ({sensor_data['soil']}%)"
            impact = "Irrigation recommended"
            agent_logs.append(f"💧 Soil below threshold - irrigation needed")
        elif decision == "HOLD":
            reason = "Soil moisture adequate"
            impact = "System monitoring"
        elif decision == "DELAY":
            reason = "Moderate dryness detected"
            impact = "Monitoring conditions"

    # ----------------------------
    # Final decision log
    # ----------------------------
    pump_status = "ON" if decision == "IRRIGATE" else "OFF"
    agent_logs.append(f"✅ Final decision: {decision} (Pump {pump_status})")

    # State memory
    if decision == "IRRIGATE":
        SYSTEM_STATE["last_action_time"] = datetime.utcnow()
    SYSTEM_STATE["last_pump_command"] = decision

    # Explanation
    explanation = generate_explanation(agent_output)

    # Update device shadow
    SYSTEM_STATE["latest_snapshot"] = {
        "device_id": payload.get("device_id", "demo"),
        "sensors": sensor_data,
        "agent_analysis": {
            **agent_output,
            "decision": decision
        },
        "agent_logs": agent_logs,
        "rain_forecast": rain_forecast_display,
        "reason": reason,
        "impact": impact,
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
    print("=" * 50)
    print("🌱 AgroSense AI - Demo Backend")
    print("   Story: Rain prevents unnecessary irrigation")
    print("=" * 50)
    print()
    print("🟢 Server running on http://localhost:5000")
    print()
    app.run(host="0.0.0.0", port=5000, debug=True)
