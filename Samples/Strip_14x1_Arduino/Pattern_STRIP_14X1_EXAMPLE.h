#ifndef STRIP_14X1_EXAMPLE_H
#define STRIP_14X1_EXAMPLE_H
#include <avr/pgmspace.h>
#include <Adafruit_NeoPixel.h>
#include "GimpLedPattern.h"

#define STRIP_14X1_EXAMPLE_DELAY 300

#define STRIP_14X1_EXAMPLE_TOTAL_LEDS 14

namespace NS_STRIP_14X1_EXAMPLE {

	const uint32_t GLOW_START[] PROGMEM = { 
	0x001900, 0x001900, 0x001900, 0x001900, 0x001900, 0x001900, 0x001900, 0x001900, 0x001900, 0x001900, 
	0x001900, 0x001900, 0x001900, 0x001900
	};

	const uint32_t FRAME_2_43[] PROGMEM = { 
	0x003f00, 0x003f00, 0x003f00, 0x003f00, 0x003f00, 0x003f00, 0x003f00, 0x003f00, 0x003f00, 0x003f00, 
	0x003f00, 0x003f00, 0x003f00, 0x003f00
	};

	const uint32_t FRAME_2_44[] PROGMEM = { 
	0x007f00, 0x007f00, 0x007f00, 0x007f00, 0x007f00, 0x007f00, 0x007f00, 0x007f00, 0x007f00, 0x007f00, 
	0x007f00, 0x007f00, 0x007f00, 0x007f00
	};

	const uint32_t FRAME_2_45[] PROGMEM = { 
	0x00bf00, 0x00bf00, 0x00bf00, 0x00bf00, 0x00bf00, 0x00bf00, 0x00bf00, 0x00bf00, 0x00bf00, 0x00bf00, 
	0x00bf00, 0x00bf00, 0x00bf00, 0x00bf00
	};

	const uint32_t GLOW_FULL[] PROGMEM = { 
	0x00ff00, 0x00ff00, 0x00ff00, 0x00ff00, 0x00ff00, 0x00ff00, 0x00ff00, 0x00ff00, 0x00ff00, 0x00ff00, 
	0x00ff00, 0x00ff00, 0x00ff00, 0x00ff00
	};

	const uint32_t GLOW_FULL_2[] PROGMEM = { 
	0x00ff00, 0x00ff00, 0x00ff00, 0x00ff00, 0x00ff00, 0x00ff00, 0x00ff00, 0x00ff00, 0x00ff00, 0x00ff00, 
	0x00ff00, 0x00ff00, 0x00ff00, 0x00ff00
	};

	const uint32_t FRAME_2_38[] PROGMEM = { 
	0x00bf00, 0x00bf00, 0x00bf00, 0x00bf00, 0x00bf00, 0x00bf00, 0x00bf00, 0x00bf00, 0x00bf00, 0x00bf00, 
	0x00bf00, 0x00bf00, 0x00bf00, 0x00bf00
	};

	const uint32_t FRAME_2_37[] PROGMEM = { 
	0x007f00, 0x007f00, 0x007f00, 0x007f00, 0x007f00, 0x007f00, 0x007f00, 0x007f00, 0x007f00, 0x007f00, 
	0x007f00, 0x007f00, 0x007f00, 0x007f00
	};

	const uint32_t FRAME_2_40[] PROGMEM = { 
	0x003f00, 0x003f00, 0x003f00, 0x003f00, 0x003f00, 0x003f00, 0x003f00, 0x003f00, 0x003f00, 0x003f00, 
	0x003f00, 0x003f00, 0x003f00, 0x003f00
	};

	const uint32_t GLOW_END[] PROGMEM = { 
	0x001900, 0x001900, 0x001900, 0x001900, 0x001900, 0x001900, 0x001900, 0x001900, 0x001900, 0x001900, 
	0x001900, 0x001900, 0x001900, 0x001900
	};

	const uint32_t *const STRIP_14X1_EXAMPLE[] PROGMEM = { 
	GLOW_START,
	FRAME_2_43,
	FRAME_2_44,
	FRAME_2_45,
	GLOW_FULL,
	GLOW_FULL_2,
	FRAME_2_38,
	FRAME_2_37,
	FRAME_2_40,
	GLOW_END,
	};

	const uint32_t STRIP_14X1_EXAMPLE_SIZES[] PROGMEM = { 
	14,
	14,
	14,
	14,
	14,
	14,
	14,
	14,
	14,
	14,
	};

}

using namespace NS_STRIP_14X1_EXAMPLE;

		
class Pattern_STRIP_14X1_EXAMPLE : public GimpLedPattern 
{

  public:
    Pattern_STRIP_14X1_EXAMPLE(Adafruit_NeoPixel& strip): GimpLedPattern(strip){}

    ~Pattern_STRIP_14X1_EXAMPLE(){}

    void playPattern() 
    {
      int totalFrames = sizeof(STRIP_14X1_EXAMPLE) / sizeof(uint32_t*);
      for (int framePos = 0; framePos < totalFrames; framePos ++)
      {
        int frameTotalLeds = pgm_read_dword(&(STRIP_14X1_EXAMPLE_SIZES[framePos]));
		int ledOffset = 0;
        for (int ledPos = 0; ledPos < frameTotalLeds; ledPos++)
        {
          if(mInterrupt)
          {
            // If we are interrupted stop the pattern. "Clean" LED pattern.
            mStrip.clear();
            mStrip.show();
            mInterrupt = false;
            return;
          }
          uint32_t ledColor = pgm_read_dword(&(STRIP_14X1_EXAMPLE[framePos][ledPos]));
          int blue = ledColor & 0x00FF;
          int green = (ledColor >> 8) & 0x00FF;
          int red = (ledColor >>  16) & 0x00FF;
          mStrip.setPixelColor(ledPos + ledOffset, red, green, blue);

        }
        mStrip.show();
        delay(STRIP_14X1_EXAMPLE_DELAY);
      }
    }

    
    void stopPattern() 
    {
      mInterrupt = true;
    }
};
		
#endif //STRIP_14X1_EXAMPLE_H

