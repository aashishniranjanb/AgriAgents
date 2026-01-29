"""
AgroSense AI — Utility-Based Agentic Decision Engine
File: backend/server/agentic_engine.py

Agent Type:
- Utility-based
- State-aware (hysteresis)
- Explainable
- Cloud/Lambda compatible

This is NOT a rule engine.
This is a scoring-based decision agent.
"""

from datetime import datetime, timedelta

# ==================================================
# 🧠 AGENT KNOWLEDGE BASE (CONFIG)
# ==================================================
THRESHOLDS = {
    "SOIL_DRY": 30.0,        # %
    "SOIL_WET": 80.0,        # %
    "TEMP_HIGH": 35.0,       # °C
    "LIGHT_DAY": 2000,       # LDR units
    "MIN_INTERVAL_SEC": 300  # 5 min hysteresis
}

UTILITY_LIMITS = {
    "IRRIGATE": 60.0,
    "DELAY": 35.0
}


# ==================================================
# 🔢 HELPER FUNCTIONS (MATH, NOT MAGIC)
# ==================================================
def clamp(val, lo, hi):
    return max(lo, min(val, hi))


def confidence_from_distance(value, threshold, span=40.0):
    """
    Confidence is proportional to distance from decision boundary.
    Near threshold → low confidence
    Far from threshold → high confidence
    """
    dist = abs(value - threshold)
    return round(clamp(dist / span, 0.0, 1.0), 2)


# ==================================================
# 🤖 CORE AGENT
# ==================================================
def agentic_decision(
    sensor_data: dict,
    last_action_time: datetime = None,
    last_decision: str = None
) -> dict:
    """
    Inputs:
      sensor_data = {
          "soil": %, "temperature": °C, "light": int
      }
      last_action_time = datetime or None
      last_decision = previous agent decision

    Output:
      Decision dict with utility + explanation trace
    """

    # ----------------------------
    # 1. SENSE & NORMALIZE
    # ----------------------------
    soil = float(sensor_data.get("soil", -1))
    temp = float(sensor_data.get("temperature", -100))
    light = float(sensor_data.get("light", 0))

    now = datetime.utcnow()
    reasons = []

    # ----------------------------
    # 2. SAFETY GUARDRAILS
    # ----------------------------
    if not (0 <= soil <= 100):
        return {
            "decision": "EMERGENCY_STOP",
            "confidence": 1.0,
            "utility": 0.0,
            "reasons": ["Soil sensor out of physical bounds"],
            "timestamp": now.isoformat()
        }

    if not (-10 <= temp <= 60):
        return {
            "decision": "EMERGENCY_STOP",
            "confidence": 1.0,
            "utility": 0.0,
            "reasons": ["Temperature sensor out of physical bounds"],
            "timestamp": now.isoformat()
        }

    # ----------------------------
    # 3. HYSTERESIS (STATE MEMORY)
    # ----------------------------
    if last_action_time:
        elapsed = (now - last_action_time).total_seconds()
        if elapsed < THRESHOLDS["MIN_INTERVAL_SEC"]:
            return {
                "decision": last_decision or "HOLD",
                "confidence": 1.0,
                "utility": 0.0,
                "reasons": [f"Cooldown active ({int(elapsed)}s since last action)"],
                "timestamp": now.isoformat()
            }

    # ----------------------------
    # 4. UTILITY CALCULATION
    # ----------------------------
    # Soil urgency (0–100)
    soil_deficit = clamp(
        THRESHOLDS["SOIL_DRY"] - soil,
        0.0,
        THRESHOLDS["SOIL_DRY"]
    )
    soil_urgency = (soil_deficit / THRESHOLDS["SOIL_DRY"]) * 100

    # Temperature penalty
    temp_penalty = 1.0
    if temp > THRESHOLDS["TEMP_HIGH"]:
        temp_penalty = 0.5
        reasons.append(f"High temperature ({temp}°C) increases evaporation risk")

    # Light suitability
    light_factor = 1.0 if light >= THRESHOLDS["LIGHT_DAY"] else 0.6
    if light < THRESHOLDS["LIGHT_DAY"]:
        reasons.append("Low light detected (non-ideal irrigation window)")

    # Final utility score
    irrigation_utility = round(
        soil_urgency * temp_penalty * light_factor,
        2
    )

    # ----------------------------
    # 5. POLICY DECISION
    # ----------------------------
    if irrigation_utility >= UTILITY_LIMITS["IRRIGATE"]:
        decision = "IRRIGATE"
        confidence = confidence_from_distance(soil, THRESHOLDS["SOIL_DRY"])
        reasons.append(f"Soil critically dry ({soil}%)")

    elif irrigation_utility >= UTILITY_LIMITS["DELAY"]:
        decision = "DELAY"
        confidence = 0.7
        reasons.append("Moderate dryness — delaying irrigation")

    else:
        decision = "HOLD"
        confidence = 0.9
        reasons.append("Soil moisture within acceptable range")

    # ----------------------------
    # 6. OUTPUT
    # ----------------------------
    return {
        "goal": "Optimize irrigation using utility-based reasoning",
        "decision": decision,
        "confidence": round(confidence, 2),
        "utility": irrigation_utility,
        "reasons": reasons,
        "timestamp": now.isoformat()
    }


# ==================================================
# 🗣️ EXPLANATION LAYER (LLM-READY)
# ==================================================
def generate_explanation(agent_output: dict) -> str:
    decision = agent_output["decision"]
    conf = int(agent_output["confidence"] * 100)
    util = agent_output["utility"]

    header = f"🧠 AI Decision: {decision} | Confidence: {conf}% | Utility: {util}"

    explanation = "\n".join([f"- {r}" for r in agent_output["reasons"]])

    return f"{header}\nReasoning:\n{explanation}"
