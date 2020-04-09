#ifndef GIMP_LED_PATTERN_H
#define GIMP_LED_PATTERN_H
#include <Adafruit_NeoPixel.h>

class GimpLedPattern
{
  public:
    GimpLedPattern(Adafruit_NeoPixel& strip): mStrip(strip) {}
    ~GimpLedPattern(){}
    
    virtual void playPattern() = 0 ;
    virtual void stopPattern() = 0;

  protected:
    Adafruit_NeoPixel& mStrip;
    bool mInterrupt = false;
};

#endif
		