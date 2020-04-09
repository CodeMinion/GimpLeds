#include <Adafruit_NeoPixel.h>
// 1 - Include at the top of Arduino sketch under your other #include statements.
#include "Pattern_TILED_MATRIX_16X16_EXAMPLE.h"

#define LED_PIN    7
#define LED_COUNT 256


Adafruit_NeoPixel strip(LED_COUNT, LED_PIN, NEO_GRB + NEO_KHZ800);
// 2 - Paste on top of setup() and under Adafruit NeoPixel declaration.
// Note: This assumes you named your pixel strip 'strip' as in the Adafruit sample
// from: https://learn.adafruit.com/adafruit-neopixel-uberguide?view=all#arduino-library-installation
// If you named it differently used that name here instead of 'strip'
GimpLedPattern * pattern_tiled_matrix_16x16_example = new Pattern_TILED_MATRIX_16X16_EXAMPLE(strip);

void setup() {
  // put your setup code here, to run once:
  // Setup Neopixels
  // Reduce brigthness 0-255
  strip.setBrightness(4);
  strip.begin();
  strip.show(); // Initialize all pixels to 'off'
}

void loop() {
  // put your main code here, to run repeatedly:

  // 3 - Paste inside loop() to run the pattern.
  pattern_tiled_matrix_16x16_example->playPattern();  

  // 4 - Optional: Use this to stop the pattern while it is in the middle of running.
  //pattern_tiled_matrix_16x16_example->stopPattern();
}
