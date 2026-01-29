"""
AgroSense AI - Fake Sensor Stream (Demo Mode)
Simulates ESP32 telemetry for testing without hardware.

Usage:
    python fake_sensor_stream.py

This sends realistic sensor data to the backend every 3 seconds.
"""

import requests
import time
import random
import math

SERVER_URL = "http://localhost:5000/data"

# Simulation state
soil_moisture = 45.0  # Start at mid-range
time_counter = 0

def simulate_sensors():
    global soil_moisture, time_counter

    # Simulate soil drying over time (natural evaporation)
    soil_moisture -= random.uniform(0.5, 2.0)
    soil_moisture = max(5, min(95, soil_moisture))

    # Temperature follows a daily sine wave pattern
    base_temp = 28
    temp_variation = 8 * math.sin(time_counter * 0.1)
    temperature = base_temp + temp_variation + random.uniform(-1, 1)

    # Light varies with "time of day"
    light = int(2000 + 1500 * math.sin(time_counter * 0.15) + random.randint(-200, 200))
    light = max(100, min(4095, light))

    time_counter += 1

    return {
        "soil": round(soil_moisture, 1),
        "temp": round(temperature, 1),
        "light": light
    }

def send_telemetry():
    global soil_moisture

    sensors = simulate_sensors()

    payload = {
        "device_id": "esp32_simulator",
        "sensors": sensors
    }

    try:
        response = requests.post(SERVER_URL, json=payload, timeout=2)
        result = response.json()

        print(f"📡 Sent: Soil={sensors['soil']}% Temp={sensors['temp']}°C Light={sensors['light']}")
        print(f"   → Decision: {result.get('decision', 'N/A')}")

        # Simulate irrigation effect: soil moisture increases if pump runs
        if result.get("decision") == "IRRIGATE":
            soil_moisture += random.uniform(8, 15)
            soil_moisture = min(95, soil_moisture)
            print(f"   💧 Pump activated! Soil now: {round(soil_moisture, 1)}%")

    except Exception as e:
        print(f"❌ Backend unreachable: {e}")

if __name__ == "__main__":
    print("🌱 AgroSense AI - Fake Sensor Stream Started")
    print(f"   Sending to: {SERVER_URL}")
    print("-" * 50)

    while True:
        send_telemetry()
        time.sleep(3)
