#include <WiFi.h>
#include <WebSocketsServer.h>
#include <Wire.h>
#include <MPU6050.h>
#include <HTTPClient.h>

const char* ssid = "youWifiSSID";       // Replace with your WiFi SSID
const char* password = "yourWifiPassword"; // Replace with your WiFi password

// WebSocket Server
WebSocketsServer webSocket(12345);

// MPU6050
MPU6050 mpu;
float ax_offset = 0, ay_offset = 0, az_offset = 0;

void calibrateSensor() {
  int sampleCount = 1000;
  long ax_sum = 0, ay_sum = 0, az_sum = 0;

  for (int i = 0; i < sampleCount; i++) {
    int16_t ax, ay, az;
    mpu.getAcceleration(&ax, &ay, &az);
    ax_sum += ax;
    ay_sum += ay;
    az_sum += az;
    delay(1);
  }

  ax_offset = ax_sum / (float)sampleCount;
  ay_offset = ay_sum / (float)sampleCount;
  az_offset = (az_sum / (float)sampleCount) - 16384;  // Subtract gravity
  Serial.println("Calibration Complete");
}

void setup() {
  Serial.begin(115200);

  // Connect to WiFi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("WiFi connected!");
  Serial.println(WiFi.localIP());

  // Initialize MPU6050
  Wire.begin();
  mpu.initialize();
  if (mpu.testConnection()) {
    Serial.println("MPU6050 connected!");
    calibrateSensor();
  } else {
    Serial.println("MPU6050 connection failed!");
    while (1);
  }

  // Start WebSocket server
  webSocket.begin();
}

void loop() {
  webSocket.loop();

  int16_t ax, ay, az;
  mpu.getAcceleration(&ax, &ay, &az);

  // Apply calibration offsets
  float ax_corrected = (ax - ax_offset) / 16384.0;  // Convert to g
  float ay_corrected = (ay - ay_offset) / 16384.0;
  float az_corrected = (az - az_offset) / 16384.0;

  // Create JSON data
  String json = "{\"ax\":" + String(ax_corrected, 3) + 
                ",\"ay\":" + String(ay_corrected, 3) + 
                ",\"az\":" + String(az_corrected, 3) + "}";

  // Broadcast data via WebSocket
  webSocket.broadcastTXT(json);

  delay(50);  // Adjust for desired update frequency
}
