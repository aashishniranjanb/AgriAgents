"""
AgroSense AI - Demo Scenario Generator
Creates a controlled narrative for compelling demos.

SCENARIO: Rain prevents unnecessary irrigation
Timeline:
  T0: Soil 30% → IRRIGATE (pump on briefly)
  T1: Soil 22%, Rain in 90min → HOLD (pump off)
  T2: Soil 20%, Rain in 30min → HOLD
  T3: Soil 25%, Rain occurred → HOLD

This proves temporal reasoning and tool usage.
"""

import requests
import time

SERVER_URL = "http://localhost:5000/data"

# Demo scenario timeline
SCENARIO = [
    # Phase 1: Normal irrigation (brief)
    {"soil": 32, "temp": 28, "light": 2800, "rain_minutes": None, "duration": 6},
    {"soil": 28, "temp": 29, "light": 2900, "rain_minutes": None, "duration": 6},
    
    # Phase 2: Rain forecast appears - agent holds
    {"soil": 24, "temp": 30, "light": 2700, "rain_minutes": 88, "duration": 9},
    {"soil": 22, "temp": 31, "light": 2500, "rain_minutes": 75, "duration": 9},
    {"soil": 20, "temp": 32, "light": 2300, "rain_minutes": 60, "duration": 9},
    {"soil": 18, "temp": 33, "light": 2100, "rain_minutes": 45, "duration": 9},
    {"soil": 16, "temp": 33, "light": 1800, "rain_minutes": 30, "duration": 9},
    {"soil": 15, "temp": 32, "light": 1500, "rain_minutes": 15, "duration": 9},
    
    # Phase 3: Rain occurs - soil recovers
    {"soil": 18, "temp": 28, "light": 800, "rain_minutes": 0, "duration": 9},
    {"soil": 28, "temp": 26, "light": 600, "rain_minutes": -10, "duration": 9},
    {"soil": 38, "temp": 25, "light": 900, "rain_minutes": -20, "duration": 9},
    {"soil": 45, "temp": 26, "light": 1200, "rain_minutes": -30, "duration": 9},
    
    # Phase 4: Post-rain - system stable
    {"soil": 42, "temp": 27, "light": 2000, "rain_minutes": None, "duration": 12},
    {"soil": 40, "temp": 28, "light": 2200, "rain_minutes": None, "duration": 12},
]

def format_rain_time(minutes):
    if minutes is None:
        return None
    if minutes <= 0:
        return "Rain occurring now" if minutes == 0 else "Rained recently"
    hours = minutes // 60
    mins = minutes % 60
    if hours > 0:
        return f"In {hours}h {mins}m"
    return f"In {mins} minutes"

def send_telemetry(data, rain_minutes):
    payload = {
        "device_id": "esp32_demo",
        "sensors": {
            "soil": data["soil"],
            "temp": data["temp"],
            "light": data["light"]
        },
        "rain_minutes": rain_minutes
    }

    try:
        response = requests.post(SERVER_URL, json=payload, timeout=2)
        result = response.json()
        return result.get("decision", "ERROR")
    except Exception as e:
        print(f"❌ Backend error: {e}")
        return "ERROR"

def run_demo():
    print("=" * 60)
    print("🌱 AgroSense AI - Demo Scenario: Rain Prevents Irrigation")
    print("=" * 60)
    print()

    cycle = 0
    while True:
        for i, phase in enumerate(SCENARIO):
            rain_display = format_rain_time(phase["rain_minutes"])
            
            print(f"📡 Phase {i+1}: Soil={phase['soil']}% Temp={phase['temp']}°C Light={phase['light']}")
            if rain_display:
                print(f"   🌧️  Weather: {rain_display}")

            decision = send_telemetry(phase, phase["rain_minutes"])
            
            # Visual decision indicator
            if decision == "HOLD":
                print(f"   ✅ Decision: HOLD (Pump OFF) - Water saved!")
            elif decision == "IRRIGATE":
                print(f"   💧 Decision: IRRIGATE (Pump ON)")
            elif decision == "DELAY":
                print(f"   ⏳ Decision: DELAY")
            else:
                print(f"   ⚠️  Decision: {decision}")
            
            print()
            time.sleep(phase["duration"])
        
        cycle += 1
        print(f"\n🔄 Demo cycle {cycle} complete. Restarting scenario...\n")
        time.sleep(3)

if __name__ == "__main__":
    run_demo()
