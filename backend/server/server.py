"""
AgriAgents - Multi-Agent Backend Orchestrator
Architecture:
- Explicit per-agent outputs
- Scenario control for demos
- Clean agent boundaries

Agents:
1. Field Agent - Sensor interpretation
2. Climate Agent - Weather reasoning
3. Decision Agent - Utility-based decisions
4. Farmer Assistant - Human explanations
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime

from agentic_engine import agentic_decision

app = Flask(__name__)
CORS(app)

# ==================================================
# 🎭 DEMO SCENARIO STATE
# ==================================================
SCENARIO = {
    "mode": "NORMAL",  # NORMAL | RAIN | PUMP_FAIL
    "rain_eta": None
}

# ==================================================
# 🧠 SYSTEM MEMORY
# ==================================================
STATE = {
    "last_action_time": None,
    "last_decision": None,
    "latest_agents": {}
}

# ==================================================
# 🎭 SCENARIO CONTROL
# ==================================================
@app.route("/scenario", methods=["POST"])
def set_scenario():
    data = request.json
    SCENARIO["mode"] = data.get("mode", "NORMAL")

    if SCENARIO["mode"] == "RAIN":
        SCENARIO["rain_eta"] = 90
    elif SCENARIO["mode"] == "PUMP_FAIL":
        SCENARIO["rain_eta"] = None
    else:
        SCENARIO["rain_eta"] = None

    print(f"🎭 Scenario changed to: {SCENARIO['mode']}")
    return jsonify({"status": "ok", "scenario": SCENARIO})


# ==================================================
# 📡 DATA INGEST
# ==================================================
@app.route("/data", methods=["POST"])
def ingest():
    payload = request.json
    sensors = payload.get("sensors", {})

    soil = float(sensors.get("soil", 0))
    temp = float(sensors.get("temp", 0))
    light = int(sensors.get("light", 0))

    # ==================================================
    # 🟫 AGENT 1: FIELD AGENT
    # ==================================================
    field_agent = {
        "soil_moisture": round(soil, 1),
        "soil_status": "CRITICAL" if soil < 25 else ("LOW" if soil < 35 else "OK"),
        "temperature": round(temp, 1),
        "heat_stress": "HIGH" if temp > 32 else "NORMAL",
        "pump_state": "OFF"
    }

    # ==================================================
    # 🌦️ AGENT 2: CLIMATE AGENT
    # ==================================================
    rain_expected = SCENARIO["mode"] == "RAIN"
    rain_eta = SCENARIO["rain_eta"]
    
    # Countdown rain ETA during demo
    if rain_expected and rain_eta and rain_eta > 0:
        SCENARIO["rain_eta"] = max(0, rain_eta - 3)
    
    climate_agent = {
        "rain_expected": rain_expected,
        "rain_eta_minutes": SCENARIO["rain_eta"],
        "evaporation_risk": "HIGH" if temp > 32 else "MODERATE"
    }

    # ==================================================
    # 🧠 AGENT 3: DECISION AGENT
    # ==================================================
    base_decision = agentic_decision(
        sensor_data={
            "soil": soil,
            "temperature": temp,
            "light": light
        },
        last_action_time=STATE["last_action_time"]
    )

    decision = base_decision["decision"]
    reason = "Soil moisture within acceptable range"

    # Climate override (agentic interaction)
    if climate_agent["rain_expected"] and soil < 35:
        decision = "HOLD"
        reason = "Rain expected soon despite dry soil"
    elif SCENARIO["mode"] == "PUMP_FAIL":
        decision = "EMERGENCY_STOP"
        reason = "Pump failure detected - system locked"
    elif decision == "IRRIGATE":
        reason = "Soil critically dry - irrigation needed"
    elif soil < 35:
        reason = "Soil moisture below optimal range"

    if decision == "IRRIGATE":
        STATE["last_action_time"] = datetime.utcnow()
        field_agent["pump_state"] = "ON"

    decision_agent = {
        "decision": decision,
        "confidence": base_decision["confidence"],
        "utility_score": base_decision["utility"],
        "reason": reason
    }

    # ==================================================
    # 🧑‍🌾 AGENT 4: FARMER ASSISTANT
    # ==================================================
    if SCENARIO["mode"] == "PUMP_FAIL":
        farmer_message = (
            "⚠️ Pump failure detected. Please check the water pump and tank. "
            "System has locked irrigation for safety."
        )
    elif climate_agent["rain_expected"]:
        eta_text = f"{climate_agent['rain_eta_minutes']} minutes" if climate_agent['rain_eta_minutes'] else "soon"
        farmer_message = (
            f"🌧️ Rain is expected in {eta_text}. Irrigation is delayed to save water "
            "and avoid unnecessary pump usage."
        )
    elif decision == "IRRIGATE":
        farmer_message = (
            "💧 Soil moisture is critically low. Irrigation has been activated "
            "to maintain crop health."
        )
    else:
        farmer_message = (
            "✅ Soil moisture is adequate. System is monitoring field and "
            "climate conditions."
        )

    farmer_assistant = {
        "message": farmer_message
    }

    # ==================================================
    # 📤 STORE & RETURN
    # ==================================================
    STATE["latest_agents"] = {
        "field_agent": field_agent,
        "climate_agent": climate_agent,
        "decision_agent": decision_agent,
        "farmer_assistant": farmer_assistant
    }

    print(f"📡 {soil}% | {decision} | Rain: {rain_expected}")

    return jsonify({
        "status": "ok",
        "decision": decision,
        "agents": STATE["latest_agents"]
    })


# ==================================================
# 🌐 UI POLLING
# ==================================================
@app.route("/state", methods=["GET"])
def state():
    return jsonify({
        "timestamp": datetime.utcnow().isoformat(),
        "agents": STATE["latest_agents"]
    })


# ==================================================
# 🚀 ENTRYPOINT
# ==================================================
if __name__ == "__main__":
    print("=" * 50)
    print("🌱 AgriAgents - Multi-Agent Backend")
    print("   Explicit per-agent outputs enabled")
    print("=" * 50)
    print()
    app.run(host="0.0.0.0", port=5000, debug=True)
