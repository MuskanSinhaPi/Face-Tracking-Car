#include "WifiCam.hpp"
#include <WiFi.h>
#include <Wire.h>             
#include "images.h"

static const char* WIFI_SSID = "Muskan";
static const char* WIFI_PASS = "muskan2002";

esp32cam::Resolution initialResolution;

WebServer server(80);


void setup()
{
  Serial.begin(115200);
  Serial.println();
  delay(2000);

  WiFi.persistent(false);
  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASS);
  if (WiFi.waitForConnectResult() != WL_CONNECTED) {
    Serial.println("WiFi failure");
    delay(5000);
    ESP.restart();
  }
  Serial.println("WiFi connected");
  delay(1000);
  {
    using namespace esp32cam;

    initialResolution = Resolution::find(1024, 768);

    Config cfg;
    cfg.setPins(pins::AiThinker);
    cfg.setResolution(initialResolution);
    cfg.setJpeg(80);

    bool ok = Camera.begin(cfg);
    if (!ok) {
      Serial.println("camera initialize failure");
      delay(5000);
      ESP.restart();
    }
    Serial.println("camera initialize success");
    delay(1000);
  }

  Serial.println("camera starting");
  delay(1000);
  Serial.print("http://");
  Serial.println(WiFi.localIP());
  addRequestHandlers();
  server.begin();
}

void
loop()
{
  server.handleClient();
}
