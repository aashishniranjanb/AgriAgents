"""
AgroSense AI - Backend Orchestrator (Device Shadow Pattern)
File: backend/server/server.py

Purpose:
- Receive telemetry from ESP32
- Maintain a local "device shadow" (digital twin)
- Invoke utility-based agentic AI
- Serve state to frontend dashboard

This is LOCAL-FIRST and AWS-LAMBDA-READY.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
from agentic_engine import agentic_decision, generate_explanation

app = Flask(__name__)
CORS(app)  # Required for frontend access

# ==================================================
# 🧠 DEVICE SHADOW (IN-MEMORY)
# ==================================================
SYSTEM_STATE = {
    "last_action_time": None,
    "latest_snapshot": {
        "status": "WAITING_FOR_DATA",
        "timestamp": None
    }
}

# ==================================================
# 📡 TELEMETRY INGEST (FROM ESP32)
# ==================================================
@app.route("/data", methods=["POST"])
def ingest_data():
    try:
        payload = request.get_json(force=True)
        print(f"📡 Telemetry Received: {payload}")

        # --- Parse nested JSON exactly as ESP32 sends ---
        sensors_raw = payload.get("sensors", {})

        sensor_data = {
            "soil": float(sensors_raw.get("soil", 0)),
            "temperature": float(sensors_raw.get("temp", 0)),
            "light": int(sensors_raw.get("light", 0))
        }

        # --- Agentic Decision ---
        agent_output = agentic_decision(
            sensor_data=sensor_data,
            last_action_time=SYSTEM_STATE["last_action_time"]
        )

        # --- Update hysteresis memory ---
        if agent_output["decision"] == "IRRIGATE":
            SYSTEM_STATE["last_action_time"] = datetime.utcnow()

        # --- Explainability layer ---
        explanation = generate_explanation(agent_output)

        # --- Update Device Shadow ---
        SYSTEM_STATE["latest_snapshot"] = {
            "device_id": payload.get("device_id", "esp32_unknown"),
            "sensors": sensor_data,
            "agent_analysis": agent_output,
            "explanation": explanation,
            "last_updated": datetime.utcnow().isoformat()
        }

        return jsonify({
            "status": "success",
            "command": agent_output["decision"]
        }), 200

    except Exception as e:
        print(f"❌ Backend Error: {str(e)}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


# ==================================================
# 🌐 DASHBOARD ENDPOINT
# ==================================================
@app.route("/state", methods=["GET"])
def get_state():
    return jsonify(SYSTEM_STATE["latest_snapshot"]), 200


# ==================================================
# 🚀 ENTRYPOINT
# ==================================================
if __name__ == "__main__":
    print("🟢 AgroSense AI Backend running on http://0.0.0.0:5000")
    app.run(host="0.0.0.0", port=5000, debug=True)
