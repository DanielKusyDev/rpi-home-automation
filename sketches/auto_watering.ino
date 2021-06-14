#include <stdio.h>
#include <ESP8266WiFi.h>

#define RELAY D1
#define MOISTURE_SENSOR D0
#define LIGHT_SENSOR A0

// Network config
const char *ssid = "Orange_Swiatlowod_516A";
const char *password = "CXN3H4S4WRCJ";
const char *host = "192.168.1.12";
const int port = 2998;

// Message config
const String lightSensorId = String("LIGHT_001");
const String moistureSensorId = String("MOIST_001");
const String analogType = String("ANL");
const String digitalType = String("DGT");

// Pump control
const int wateringLimit = 3;
const int minDelayBetweenWatering = 10;
int wateringDuration = 0;
int timeWithoutWatering = 0;

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
        for(int i=0; i<length; i++) {
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
    timeWithoutWatering = 0;
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

    Serial.print("\nMOISTURE: " + String(moistureLevel, DEC) + "\nLIGHT: " + String(lightLevel, DEC) +
                 "\nWater pump is on: " + String(waterPumpOn, DEC) + "\n\n");

    if (waterPumpOn) {
        wateringDuration++;
    } else {
        timeWithoutWatering++;
    }

    bool waterPumpShouldStart = (waterPumpOn == LOW && moistureLevel == HIGH &&
                                 timeWithoutWatering > minDelayBetweenWatering);
    bool waterPumpShouldStop = (moistureLevel == LOW) || (wateringDuration > wateringLimit);

    if(waterPumpShouldStart) {
        runWaterPump();
    } else if(waterPumpShouldStop) {
        stopWaterPump();
    }
    Message messages[2];
    messages[0] = {moistureSensorId, digitalType, moistureLevel, 0};
    messages[1] = {lightSensorId, analogType, lightLevel, 1};
    sendMessages(messages, 2);
    delay(10000);
}