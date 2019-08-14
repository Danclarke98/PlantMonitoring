#include <ArduinoJson.h>
#include <PubSubClient.h>
#include <WiFi.h>
#include <NTPClient.h>
#include <WiFiUdp.h>
#include "time.h"


#include "DHTesp.h"
 
DHTesp dht;

const int dhtpin = 22;
const int soilpin = 32;
const int POWER_PIN = 34;
const int LIGHT_PIN = 33;

const char* ssid = "{WIFI SSID}";
const char* password = "{WIFI PASSWORD}";

const char* mqtt_server = "{MQTT IP}";
const int mqtt_port = 1883;

const char* mqttUser = "{USERNAME}";
const char* mqttPassword = "{PASSWORD}";
const int   deviceID = {GENERATED DEVICE ID};


const char* ntpServer = "pool.ntp.org";
const long  gmtOffset_sec = -28800;
const int   daylightOffset_sec = 3600;



WiFiClient espClient;
PubSubClient client(espClient);

WiFiUDP ntpUDP;
NTPClient timeClient(ntpUDP);
String formattedDate;

String printLocalTime()
{
  struct tm timeinfo;
  if(!getLocalTime(&timeinfo)){
    Serial.println("Failed to obtain time");
    return "Failed to obtain time";
  }
  char timeStringBuff[50]; //50 chars should be enough
  strftime(timeStringBuff, sizeof(timeStringBuff), "%Y-%m-%d %H:%M:%S", &timeinfo);
  //print like "const char*"
  Serial.println(timeStringBuff);

  //Optional: Construct String object 
  String asString(timeStringBuff);
  return asString;
}

 
void setup()
{
  Serial.begin(115200);
  Serial.println();

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println("Connecting to WiFi..");
  }

  configTime(gmtOffset_sec, daylightOffset_sec, ntpServer);
  printLocalTime();

  Serial.println("Connected to the WiFi network;");

  client.setServer(mqtt_server, mqtt_port);
 
  dht.setup(22, DHTesp::DHT11);

  while (!client.connected()) {
    Serial.println("Connecting to MQTT...");
 
    if (client.connect("ESP32Client", mqttUser, mqttPassword )) {
 
      Serial.println("connected to MQTT");
 
    } else {
 
      Serial.print("failed with state");
      Serial.print(client.state());
      delay(2000);
 
    }
  }
}


 
void loop()
{

  printLocalTime();
  
  float humidity = dht.getHumidity(); 
  float temp = dht.getTemperature();


  int waterlevel = analogRead(soilpin);

  
  waterlevel = map(waterlevel, 3200, 1500, 0, 100);
  waterlevel = constrain(waterlevel, 0, 100);
  
 
  const size_t CAPACITY = JSON_ARRAY_SIZE(4);
  StaticJsonDocument<200> doc;
  JsonArray array = doc.to<JsonArray>();
  JsonObject nested = array.createNestedObject();
  nested["device_id"] = deviceID;
  nested["temp"] = temp;
  nested["humidity"] = humidity;
  nested["water"] = waterlevel;
  nested["date_posted"] = printLocalTime();

  
  char jsonChar[100];
  serializeJson(doc, jsonChar);
  Serial.println(jsonChar);

  client.publish("sensor/", jsonChar);
  

  delay(15000);
 
}
