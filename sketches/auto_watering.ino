#include "arduino_secrets.h"
#include <stdio.h>
#include <ESP8266WiFi.h>

#define RELAY D0
#define MOISTURE_SENSOR D1
#define LIGHT_SENSOR A0

// Network config
const char *ssid = SECRET_SSID;
const char *password = SECRET_SSID_PASSWORD;
const char *host = SECRET_HOST;
const int port = SECRET_PORT;

// Message config
const String lightSensorId = String("LIGHT_001");
const String moistureSensorId = String("MOIST_001");
const String analogType = String("ANL");
const String digitalType = String("DGT");

// Pump control
const int wateringLimit = 2;
const int loopDelayWhileWatering = 1 * 1000;
const int loopDelayBetweenWatering = 60 * 60 * 1000; // 1 hour delay
const int loopsBetweenWatering = 2;

int wateringDuration = 0;
int iterationsWithoutWatering = 0;


struct Message {
  String SNSR;
  String TYP;
  int VAL;
  unsigned int EOM;
};

void initializeWifiConnection() {
  Serial.println();
  WiFi.begin(ssid, password);
  Serial.print("Connecting");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println();

  Serial.print("Connected, IP address: ");
  Serial.println(WiFi.localIP());
}

void sendMessages(Message messages[], int length) {
  WiFiClient client;
  if (client.connect(host, port)) {
    for (int i = 0; i < length; i++) {
      Message message = messages[i];
      String messageAsString = String(
                                 "SNSR:" + message.SNSR + "\r\n" +
                                 "TYP:" + message.TYP + "\r\n" +
                                 "VAL:" + String(message.VAL, DEC) + "\r\n" +
                                 "EOM:" + String(message.EOM, DEC) + "\r\n");
      Serial.print(messageAsString);
      client.print(messageAsString);
      Serial.println(client.readStringUntil('\r\n') + "\n");
      delay(500);
    }
  } else {
    Serial.println("Error while connecting with the host");
  }
}

void runWaterPump() {
  digitalWrite(RELAY, HIGH);
}

void stopWaterPump() {
  digitalWrite(RELAY, LOW);
  iterationsWithoutWatering = 0;
  wateringDuration = 0;
}

void setup() {
  Serial.begin(115200);
  initializeWifiConnection();
  pinMode(RELAY, OUTPUT);
  pinMode(MOISTURE_SENSOR, INPUT);
  pinMode(LIGHT_SENSOR, INPUT);
}

void loop() {
  int moistureLevel = digitalRead(MOISTURE_SENSOR);
  int lightLevel = analogRead(LIGHT_SENSOR);
  int waterPumpOn = digitalRead(RELAY);
  if (waterPumpOn) {
    wateringDuration++;
    Serial.println("WateringDuration: "); Serial.println(wateringDuration);
    delay(loopDelayWhileWatering);
  } else {
    iterationsWithoutWatering++;
    delay(loopDelayBetweenWatering);
    Serial.println("Time without watering: "); Serial.println(iterationsWithoutWatering);
  }

  Serial.println(moistureLevel);

  bool waterPumpShouldStart = (waterPumpOn == LOW && moistureLevel == HIGH &&
                               iterationsWithoutWatering > loopsBetweenWatering-1);
  bool waterPumpShouldStop = (moistureLevel == LOW) || (wateringDuration > wateringLimit);

  if (waterPumpShouldStart) {
    runWaterPump();
  } else if (waterPumpShouldStop) {
    stopWaterPump();
  }
  Message messages[2];
  messages[0] = {moistureSensorId, digitalType, moistureLevel, 0};
  messages[1] = {lightSensorId, analogType, lightLevel, 1};
  sendMessages(messages, 2);
}