#include <Adafruit_NeoPixel.h>

#define PIN            6    // Data pin connected to NeoPixels
#define NUMPIXELS      20   // Number of LEDs

Adafruit_NeoPixel strip = Adafruit_NeoPixel(NUMPIXELS, PIN, NEO_GRB + NEO_KHZ800);

void setup() {
  strip.begin();  // Initialize the NeoPixel strip
  strip.show();   // Initialize all pixels to 'off'
}

void loop() {
  for(int i = 0; i < NUMPIXELS; i++) {
    strip.setPixelColor(i, strip.Color(255, 0, 0));  // Red
    strip.show();
    delay(500);
  }
}