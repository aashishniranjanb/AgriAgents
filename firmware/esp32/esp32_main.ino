/************************************************************
 * AgroSense AI - ESP32 Firmware (Production-Grade Showcase)
 * Architecture:
 * - Event-driven (millis)
 * - Finite State Machine (FSM)
 * - Hysteresis + Cooldown
 * - Sensor fault awareness
 * - Network-failure tolerant
 ************************************************************/

#include <WiFi.h>
#include <HTTPClient.h>
#include <DHT.h>
#include <ArduinoJson.h>

/* ===================== CONFIG ===================== */
const char* WIFI_SSID = "<WIFI_SSID>";
const char* WIFI_PASSWORD = "<WIFI_PASSWORD>";
const char* SERVER_URL = "http://<SERVER_IP>:5000/data";

const unsigned long SENSOR_INTERVAL = 2000;
const unsigned long TELEMETRY_INTERVAL = 10000;
const unsigned long WIFI_RETRY_INTERVAL = 15000;

const int SOIL_ON = 30;
const int SOIL_OFF = 40;

const unsigned long MAX_PUMP_RUNTIME = 15000;
const unsigned long COOLDOWN_TIME = 30000;

/* ===================== PINS ===================== */
#define DHT_PIN 4
#define DHT_TYPE DHT11
#define SOIL_PIN 34
#define LDR_PIN 35
#define RELAY_PIN 26
#define LED_STATUS 2

DHT dht(DHT_PIN, DHT_TYPE);

/* ===================== FSM ===================== */
enum PumpState {
  IDLE,
  IRRIGATING,
  COOLDOWN,
  FAULT
};

PumpState pumpState = IDLE;

/* ===================== SYSTEM STATE ===================== */
struct {
  float temp;
  float humidity;
  int soil;
  int light;
  bool sensorFault;
} sensors;

unsigned long lastSensorRead = 0;
unsigned long lastTelemetry = 0;
unsigned long lastWifiRetry = 0;
unsigned long pumpStart = 0;
unsigned long cooldownStart = 0;

/* ===================== WIFI ===================== */
void handleWiFi(unsigned long now) {
  if (WiFi.status() == WL_CONNECTED) return;

  if (now - lastWifiRetry > WIFI_RETRY_INTERVAL) {
    lastWifiRetry = now;
    WiFi.disconnect();
    WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
    Serial.println("📡 WiFi reconnect attempt");
  }
}

/* ===================== SENSORS ===================== */
void readSensors() {
  sensors.sensorFault = false;

  float t = dht.readTemperature();
  float h = dht.readHumidity();

  if (isnan(t) || isnan(h)) {
    sensors.sensorFault = true;
    return;
  }

  sensors.temp = t;
  sensors.humidity = h;

  int raw = analogRead(SOIL_PIN);
  sensors.soil = constrain(map(raw, 4095, 1500, 0, 100), 0, 100);
  sensors.light = analogRead(LDR_PIN);
}

/* ===================== EDGE CONTROL ===================== */
void runFSM(unsigned long now) {

  if (sensors.sensorFault) {
    pumpState = FAULT;
  }

  switch (pumpState) {

    case IDLE:
      if (sensors.soil < SOIL_ON) {
        digitalWrite(RELAY_PIN, HIGH);
        pumpStart = now;
        pumpState = IRRIGATING;
        Serial.println("💧 Pump ON");
      }
      break;

    case IRRIGATING:
      if (now - pumpStart > MAX_PUMP_RUNTIME) {
        digitalWrite(RELAY_PIN, LOW);
        cooldownStart = now;
        pumpState = COOLDOWN;
        Serial.println("⚠️ Safety cutoff → Cooldown");
      }
      else if (sensors.soil > SOIL_OFF) {
        digitalWrite(RELAY_PIN, LOW);
        pumpState = IDLE;
        Serial.println("🛑 Target reached");
      }
      break;

    case COOLDOWN:
      if (now - cooldownStart > COOLDOWN_TIME) {
        pumpState = IDLE;
        Serial.println("⏳ Cooldown complete");
      }
      break;

    case FAULT:
      digitalWrite(RELAY_PIN, LOW);
      Serial.println("❌ Sensor fault — irrigation locked");
      break;
  }
}

/* ===================== TELEMETRY ===================== */
void sendTelemetry() {
  if (WiFi.status() != WL_CONNECTED) return;

  StaticJsonDocument<256> doc;
  doc["soil"] = sensors.soil;
  doc["temp"] = sensors.temp;
  doc["light"] = sensors.light;
  doc["pump_state"] = pumpState;
  doc["sensor_fault"] = sensors.sensorFault;

  String payload;
  serializeJson(doc, payload);

  HTTPClient http;
  http.setTimeout(800);
  http.begin(SERVER_URL);
  http.addHeader("Content-Type", "application/json");
  http.POST(payload);
  http.end();

  digitalWrite(LED_STATUS, !digitalRead(LED_STATUS));
}

/* ===================== SETUP ===================== */
void setup() {
  Serial.begin(115200);
  pinMode(RELAY_PIN, OUTPUT);
  pinMode(LED_STATUS, OUTPUT);
  digitalWrite(RELAY_PIN, LOW);

  dht.begin();
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
}

/* ===================== LOOP ===================== */
void loop() {
  unsigned long now = millis();

  handleWiFi(now);

  if (now - lastSensorRead > SENSOR_INTERVAL) {
    lastSensorRead = now;
    readSensors();
    runFSM(now);
  }

  if (now - lastTelemetry > TELEMETRY_INTERVAL) {
    lastTelemetry = now;
    sendTelemetry();
  }
}
