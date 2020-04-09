#include <Adafruit_NeoPixel.h>
// 1 - Include at the top of Arduino sketch under your other #include statements.
#include "Pattern_STRIP_14X1_EXAMPLE.h"

#define LED_PIN    7
#define LED_COUNT 14


Adafruit_NeoPixel strip(LED_COUNT, LED_PIN, NEO_GRB + NEO_KHZ800);
// 2 - Paste on top of setup() and under Adafruit NeoPixel declaration.
// Note: This assumes you named your pixel strip 'strip' as in the Adafruit sample
// from: https://learn.adafruit.com/adafruit-neopixel-uberguide?view=all#arduino-library-installation
// If you named it differently used that name here instead of 'strip'
GimpLedPattern * pattern_strip_14x1_example = new Pattern_STRIP_14X1_EXAMPLE(strip);

void setup() {
  // put your setup code here, to run once:
  // Reduce brigthness 0-255
  strip.setBrightness(32);
  // Setup Neopixels
  strip.begin();
  strip.show(); // Initialize all pixels to 'off'
  
}

void loop() {
  // put your main code here, to run repeatedly:
  // 3 - Paste inside loop() to run the pattern.
  pattern_strip_14x1_example->playPattern();  


  // 4 - Optional: Use this to stop the pattern while it is in the middle of running.
  //pattern_strip_14x1_example->stopPattern();

}
