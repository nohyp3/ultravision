#include "esp_camera.h"
#include <WiFi.h>
#include <HTTPClient.h>

// Replace with your network credentials
const char* ssid     = "YOUR_WIFI_SSID";
const char* password = "bingchilling123";

// Camera pin configuration for AI‑Thinker ESP32-CAM module
#define PWDN_GPIO_NUM    -1
#define RESET_GPIO_NUM   -1
#define XCLK_GPIO_NUM    21
#define SIOD_GPIO_NUM    26
#define SIOC_GPIO_NUM    27

#define Y9_GPIO_NUM      35
#define Y8_GPIO_NUM      34
#define Y7_GPIO_NUM      39
#define Y6_GPIO_NUM      36
#define Y5_GPIO_NUM      19
#define Y4_GPIO_NUM      18
#define Y3_GPIO_NUM       5
#define Y2_GPIO_NUM       4
#define VSYNC_GPIO_NUM   25
#define HREF_GPIO_NUM    23
#define PCLK_GPIO_NUM    22

// Backend API URL (IP address of your PC)
const char* serverUrl = "http://100.66.5.25:5000/upload"; // Update with your machine's IP address

void setup() {
  Serial.begin(115200);
  Serial.setDebugOutput(true);
  Serial.println();

  // Camera configuration
  camera_config_t config;
  config.ledc_channel = LEDC_CHANNEL_0;
  config.ledc_timer   = LEDC_TIMER_0;
  config.pin_d0     = Y2_GPIO_NUM;
  config.pin_d1     = Y3_GPIO_NUM;
  config.pin_d2     = Y4_GPIO_NUM;
  config.pin_d3     = Y5_GPIO_NUM;
  config.pin_d4     = Y6_GPIO_NUM;
  config.pin_d5     = Y7_GPIO_NUM;
  config.pin_d6     = Y8_GPIO_NUM;
  config.pin_d7     = Y9_GPIO_NUM;
  config.pin_xclk   = XCLK_GPIO_NUM;
  config.pin_pclk   = PCLK_GPIO_NUM;
  config.pin_vsync  = VSYNC_GPIO_NUM;
  config.pin_href   = HREF_GPIO_NUM;
  config.pin_sscb_sda = SIOD_GPIO_NUM;
  config.pin_sscb_scl = SIOC_GPIO_NUM;
  config.pin_pwdn   = PWDN_GPIO_NUM;
  config.pin_reset  = RESET_GPIO_NUM;
  config.xclk_freq_hz = 20000000;
  config.pixel_format = PIXFORMAT_JPEG;

  // Set frame size and quality settings based on available PSRAM
  if (psramFound()) {
    config.frame_size = FRAMESIZE_UXGA;  // High resolution
    config.jpeg_quality = 10;            // Lower quality number means higher quality
    config.fb_count = 2;                 // Use 2 frame buffers for smoother streaming
  } else {
    config.frame_size = FRAMESIZE_SVGA;  // Lower resolution for boards without PSRAM
    config.jpeg_quality = 12;
    config.fb_count = 1;
  }

  // Initialize the camera
  esp_err_t err = esp_camera_init(&config);
  if (err != ESP_OK) {
    Serial.printf("Camera init failed with error 0x%x\n", err);
    return;
  }

  // Connect to Wi-Fi
  Serial.println("Connecting to WiFi...");
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi connected");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
}

void loop() {
  captureAndSendImage();
  delay(1000); // Adjust the delay as needed
}

void captureAndSendImage() {
  camera_fb_t* fb = esp_camera_fb_get();
  if (!fb) {
    Serial.println("Camera capture failed");
    return;
  }

  Serial.println("Sending image to server...");
  HTTPClient http;
  http.begin(serverUrl);
  http.addHeader("Content-Type", "image/jpeg");

  int httpResponseCode = http.POST(fb->buf, fb->len);
  if (httpResponseCode > 0) {
    String response = http.getString();
    Serial.println("Response: " + response);
  } else {
    Serial.printf("Error: %d\n", httpResponseCode);
  }
  http.end();

  esp_camera_fb_return(fb);
}