#!/usr/bin/env python


import os
from gimpfu import *
import time

def generate_led_pattern(ledType, newimg, 
               frameDelay, rowOrderType, dir):
    
	# TODO Consider allowing user to specify pattern name instead of using the file name.
	filename, file_extension = os.path.splitext(newimg.name)
	
	constPattern = nameToConst(filename)
		
	# List of frames in the pattern. 
	patternFrames = []
	
	ledFrames = []
	# Get layers in the newimg
	imageLayers = flatternGroups(newimg)
	layerIndex = 0
	for layer in imageLayers:
		
		# Skip the layers that are hidden / not visible
		if not pdb.gimp_drawable_get_visible(layer):
			continue
		
		# convert the layer name to a const name 
		constLayer = nameToConst(layer.name)
		
		# Track the pattern name
		patternFrames.append(constLayer)
		
		lastLed = (layer.height * layer.width) - 1 
		ledIndex = 0
		
		pixelColors = []
		# Get the pixels in the layer
		for y in range(0, layer.height):
			for x in range(0, layer.width):
				num_channels, pixel = pdb.gimp_drawable_get_pixel(layer, x, y)
				
				ledAlpha = 255
				# If it has 4 channels then we have alpha in the end. 
				if num_channels == 4:
					ledAlpha = pixel[3]
				
				pixelColor = {
					KEY_COLOR_RED: pixel[0], 
					KEY_COLOR_GREEN: pixel[1], 
					KEY_COLOR_BLUE: pixel[2], 
					KEY_COLOR_ALPHA: ledAlpha
					}
					
				# Track LED
				pixelColors.append(pixelColor)
		
		# Perform any processing needed on the pixel row.
		pixelColors = processPixelRow(pixelColors, rowOrderType, rowOrderType)
		
		# TODO Depending on the row ordering flip this list. 	
		# Track pattern.
		ledFrame = {
			KEY_FRAME_ID: constLayer,
			KEY_FRAME_PIXEL_COLORS: pixelColors
		}
		ledFrames.append(ledFrame)
	
	
	#Layers are listed from the top most down, for the frames we want to start at the bottom.
	ledFrames.reverse() 
	# Build LEd Pattern
	outLedPattern = {
		KEY_PATTERN_ID: constPattern,
		KEY_PATTERN_DELAY: frameDelay,
		KEY_PATTERN_FRAMES: ledFrames,
		KEY_PATTERN_TOTAL_LEDS: (newimg.width*newimg.height)
	}
	
	pdb.gimp_progress_pulse()
	pdb.gimp_progress_set_text("Generating code...")
	if ledType == CHOICE_ADAFRUIT_NEOPIXEL_ARDUINO:
		# Generate Code for Arduino and Adafruit Neo Pixel.
		ledCodeGenerator = AdafruitNeoPixelStripCodeGenerator(outLedPattern, filename, dir)
		ledCodeGenerator.generate()
		pass
	pdb.gimp_progress_update(1.0)
	pdb.gimp_progress_set_text("Generation Done!")
	pdb.gimp_progress_end()
	
	return

	
def nameToConst(name):
	outName = name.upper().replace(" ", "_").replace("#","")
	return outName

# Groups are layers composed of layser, so this will flatten 
# all the groups into a single list of layers.
# Note: Not to be confused with the actual GIMP command called flatten
# which produces a single image with all visible layers.	
def flatternGroups(parent):
	
	outLayers = []
	
	layers = parent.layers
	
	for layer in layers:
		if  pdb.gimp_item_is_group(layer) and pdb.gimp_drawable_get_visible(layer):
			# flatten the groups 
			outLayers.extend( flatternGroups(layer))
			pass
		else:
			outLayers.append(layer)
	
	return outLayers

# Processing to support form common LED layouts.
# Standard - Default, row-major. No changes needed.
# Flip Odd - Reverses the pixels in the odd rows.
# Flip Even - Reverses the pixels in the even rows.
def processPixelRow(pixelList, rowOrder, rowPosition):
	outPixelList = []
	if rowOrder == ROW_PROCESSING_STANDARD:
		# Do nothing
		outPixelList = pixelList
	elif rowOrder == ROW_PROCESSING_EVEN and rowPosition % 2 == 0:
		pixelList.reverse()
		outPixelList = pixelList
	elif rowOrder == ROW_PROCESSING_ODD and rowPosition % 2 == 1:
		pixelList.reverse()
		outPixelList = pixelList
		
	return outPixelList	
'''
Row Processing Options
'''
# No change, continue default row-major order.
ROW_PROCESSING_STANDARD = 0
# Reverse pixel Order for odd rows.
ROW_PROCESSING_ODD = 1 
# Reverse pixel order for even rows.
ROW_PROCESSING_EVEN = 2 	
'''
Code Generation Choices
'''
CHOICE_ADAFRUIT_NEOPIXEL_ARDUINO = 0
CHOICE_RESERVED = 1
	
'''
 Intermediate generation section
'''
# ID of the Entire Pattern.
KEY_PATTERN_ID = "patternId"
# List of frames in the pattern. 
KEY_PATTERN_FRAMES = "patternFrames"
# Delay in milliseconds of the LED pattern. 
# This will be the duration a given frame is displayed for.
KEY_PATTERN_DELAY = "delay"
# ID of the frame. Used mostly internally. 
KEY_FRAME_ID = "frameId"
# Color of each individual LED/Pixel during this frame. 
# Note: Each pixel in the image maps to an LED.
# Pixels are laid out as a linear sequence
# of width*height pixels, extracted from the image in row-major,
# top-to-bottom, left-to-right order (the same as the reading direction
# of multi-line English text)
KEY_FRAME_PIXEL_COLORS = "pixels"
# Total number of LEDs. Total = Width*Height
KEY_PATTERN_TOTAL_LEDS = "totalLeds"
# Color keys, stored in a range between 0-255
KEY_COLOR_RED = "R"
KEY_COLOR_GREEN = "G"
KEY_COLOR_BLUE = "B"
KEY_COLOR_ALPHA = "A"
'''
----------------- END of JSON Intermediate generation section -----
'''	

'''
Adafruit Code Generator
'''
class AdafruitNeoPixelStripCodeGenerator: 
	
	# File to which to write the generated code to. 
	mOutFile = None
	mLedPattern = None
	mOutDir = None
	
	LIMIT_LINE_LENTH = 10
	LIMIT_LINE_BREAK = 9
	
	def __init__(self, ledPattern, outFileName, outDir):
		#outFilename = os.path.join(outDir, '{0}_Pattern.h'.format(outFileName))
		outFilename = os.path.join(outDir, '{0}.h'.format(self.getGeneratedLedPatternClassName(ledPattern[KEY_PATTERN_ID])))
		self.mOutDir = outDir
		self.mOutFile = open(outFilename, "w")
		self.mLedPattern = ledPattern
		
		
		pass
		
	def generate(self):
		# Write Header 
		patternId = self.mLedPattern[KEY_PATTERN_ID]
		self.writeHeaders(patternId, self.mOutFile)
		
		# Include delay
		patternDelay = self.mLedPattern[KEY_PATTERN_DELAY]
		self.mOutFile.write("\n#define {0} {1}\n".format(self.getDelayDefineId(patternId), int(patternDelay)))
		
		# Include total LEDs
		patternLEDsTotal = self.mLedPattern[KEY_PATTERN_TOTAL_LEDS]
		self.mOutFile.write("\n#define {0} {1}\n\n".format(self.getTotalLedsDefineId(patternId), int(patternLEDsTotal)))
		
		# For each LED Frame Generate constant
		ledFrames = self.mLedPattern[KEY_PATTERN_FRAMES]
		
		# Wrap const declarations in namespace to prevent duplicate conflicts
		self.writeNamespaceStart(patternId, self.mOutFile)
		
		for frame in ledFrames:
			# Write Frame const start
			frameId = frame[KEY_FRAME_ID]
			self.writeFrameConst(frameId, self.mOutFile)
			
			pixelColors = frame[KEY_FRAME_PIXEL_COLORS]
			pixelIndex = 0
			lastPixel = len(pixelColors) - 1
			for color in pixelColors:
				# LEDs don't have alpha so we just reduce the color by the alpha ratio.
				colorRatio = color[KEY_COLOR_ALPHA]/255.0
				
				R = "%02x" %self.dimColorByRatio(color[KEY_COLOR_RED], colorRatio)
				G = "%02x" %self.dimColorByRatio(color[KEY_COLOR_GREEN], colorRatio)
				B = "%02x" %self.dimColorByRatio(color[KEY_COLOR_BLUE], colorRatio)
				
				# Move this into code generator which will consume the LED Pattern JSON
				if pixelIndex < lastPixel:
					self.mOutFile.write('0x{0}{1}{2}, '.format(R,G,B))
				else: 
					self.mOutFile.write('0x{0}{1}{2}\n'.format(R,G,B))
				pass
				
				# Add a new line after 10 patterns to keep the width of the code slim
				if pixelIndex % self.LIMIT_LINE_LENTH == self.LIMIT_LINE_BREAK:
					self.mOutFile.write("\n	")
				
				pixelIndex = pixelIndex + 1
			# Write Frame const end 
			self.mOutFile.write("	};\n")
			
			pass
			
		# Generate LED Pattern constant.
		self.writePatternConst(patternId, self.mOutFile)
		for frame in ledFrames:
			self.mOutFile.write("	{0},\n".format(frame[KEY_FRAME_ID]))
		pass
		self.mOutFile.write("	};\n")
		
		# End namespace declarations
		self.writeNamespaceEnd(patternId, self.mOutFile)
		
		# Write the function that will be exposed 
		# to the main Arduino sketch to run the led pattern.
		#self.writePlayFunction(patternId, self.mOutFile)
		self.writePatternClass(patternId, self.mOutFile)
		
		# Write Footer
		self.writeFooters(patternId, self.mOutFile)
		
		self.mOutFile.write("\n")
		
		self.mOutFile.close()
		
		# Write Base Pattern class 
		self.writeBaseLedPatternClass()
		
		# TODO Generate ReadMe file with simple instructions on how to include in existing script.
		self.generateReadMe(patternId)
		pass

	# Dims a color by a given ratio. Because we are creating LED 
	# patterns and those don't have opacity, we'll just update the 
	# color by the opacity ratio	
	def dimColorByRatio(self, color, ratio):
		outColor = int(color * ratio)
		return outColor
	
	# Generates the ID that will be used in the Total LEDs define statement
	def getTotalLedsDefineId(self, patternId):
		return "{0}_TOTAL_LEDS".format(patternId)
		
	# Generates the ID that will be used in the Delay define statement
	def getDelayDefineId(self, patternId):
		return "{0}_DELAY".format(patternId)
		
	def toCamelCase(self, text):
		text = text.title()
		return text[0].lower() + text[1:]
		
	# Helper to write the start of a frame to the Arduino file.
	def writeFrameConst(self, frameName, outFile):
		outFile.write("\n	const uint32_t {0}[] PROGMEM = {{ \n	".format(frameName))

	# Helper to write the start of a pattern to the Arduino file.
	# A Pattern is composed of Frames.
	def writePatternConst(self, patternName, outFile):
		outFile.write("\n	const uint32_t *const {0}[] PROGMEM = {{ \n".format(patternName))

	# Helper to write any headers needed	
	def writeHeaders(self, patternName, outFile):
		outFile.write("#ifndef {0}_H\n".format(patternName))
		outFile.write("#define {0}_H\n".format(patternName))
		
		#outFile.write("\n#ifndef PGMSPACE_H\n")
		#outFile.write("#define PGMSPACE_H\n")
		outFile.write("#include <avr/pgmspace.h>\n")
		outFile.write("#include <Adafruit_NeoPixel.h>\n")
		#Include Base Pattern class
		outFile.write('#include "{0}.h"\n'.format(self.getBasePatternClassName()))
		#outFile.write("#endif //PGMSPACE_H\n")

		
	# Namespaces used to prevent conflicts in cases where two patterns 
	# are generated from layers with the same name.
	def writeNamespaceStart(self, patternId, outFile):
		outFile.write("namespace {0} {{\n".format(self.getNamespaceName(patternId)))
		pass
		
	def writeNamespaceEnd(self, patternId, outFile):
		outFile.write("""
}}

using namespace {0};

		""".format(self.getNamespaceName(patternId)))
		pass
		
	def getNamespaceName(self, patternId):
		return "NS_{0}".format(patternId)
		pass

	#Helper to write any footers needed.
	def writeFooters(self, patternName, outFile):
		outFile.write("\n#endif //{0}_H\n".format(patternName))

	def writePlayFunction(self, patternId, outFile):
		outFile.write("""
/**
 * Call this with the NeoPixel strip on which the pattern 
 * will be displayed.
 */ 
void play_{3}(Adafruit_NeoPixel strip) 
{{
  int totalFrames = sizeof({0})/sizeof(long*);
  for (int framePos = 0; framePos < totalFrames; framePos ++) 
  {{
    for (int ledPos =0; ledPos < {1}; ledPos++)
    {{
      unsigned long ledColor = pgm_read_word(&({0}[framePos][ledPos]));
      int blue = ledColor & 0x00FF;
      int green = (ledColor >> 8);
      int red = (ledColor >>  16);
      strip.setPixelColor(ledPos, red, green, blue);
      
    }}
    strip.show();
    delay({2});
  }}
}}
""".format(patternId, self.getTotalLedsDefineId(patternId), self.getDelayDefineId(patternId), self.toCamelCase(patternId)))
	
	# Writes the base class used by all LED pattern in a seprate class. 
	# This would ideally be released as an independent Lib later on. 
	# But for now generating it so the output is self-contained. 
	def writeBaseLedPatternClass(self):
		outFilename = os.path.join(self.mOutDir, '{0}.h'.format(self.getBasePatternClassName()))
		baseClassFile = open(outFilename, "w")
		baseClassFile.write(
		"""#ifndef GIMP_LED_PATTERN_H
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
		""")
		baseClassFile.close()
		
	# Returns the class name for the base LED Pattern class	
	def getBasePatternClassName(self):
		return "GimpLedPattern"
	
	# Returns the name of the class generated for this pattern. 
	def getGeneratedLedPatternClassName(self, patternId):
		return "Pattern_{0}".format(patternId)
		
	# Writes the class for this LED Pattern
	def writePatternClass(self, patternId, outFile):
		outFile.write("""
class {4} : public GimpLedPattern 
{{

  public:
    {4}(Adafruit_NeoPixel& strip): {3}(strip){{}}

    ~Pattern_{0}(){{}}

    void playPattern() 
    {{
      int totalFrames = sizeof({0}) / sizeof(uint32_t*);
      for (int framePos = 0; framePos < totalFrames; framePos ++)
      {{
        for (int ledPos = 0; ledPos < {1}; ledPos++)
        {{
          if(mInterrupt)
          {{
            // If we are interrupted stop the pattern. "Clean" LED pattern.
            mStrip.clear();
            mStrip.show();
            mInterrupt = false;
            return;
          }}
          uint32_t ledColor = pgm_read_dword(&({0}[framePos][ledPos]));
          int blue = ledColor & 0x00FF;
          int green = (ledColor >> 8) & 0x00FF;
          int red = (ledColor >>  16) & 0x00FF;
          mStrip.setPixelColor(ledPos, red, green, blue);

        }}
        mStrip.show();
        delay({2});
      }}
    }}

    
    void stopPattern() 
    {{
      mInterrupt = true;
    }}
}};
		""".format(patternId, 
		self.getTotalLedsDefineId(patternId), 
		self.getDelayDefineId(patternId), 
		self.getBasePatternClassName(), 
		self.getGeneratedLedPatternClassName(patternId))
		)
	
	# Generates a ReadMe file for ease of integration into an existing sketch. 
	def generateReadMe(self, patternId):
		outFilename = os.path.join(self.mOutDir, 'ReadMe_{0}.txt'.format(self.getGeneratedLedPatternClassName(patternId)))
		readMeFile = open(outFilename, "w")
		readMeFile.write("""

// Note: These steps assume you used the sketh directory as the destination directory when creating the pattern. 
// If you selected a different directory then simply copy the generated files over and into the sketch directory. 

// 1 - Include at the top of Arduino sketch under your other #include statements.
#include "{0}.h"

// 2 - Paste on top of setup() and under Adafruit NeoPixel declaration.
// Note: This assumes you named your pixel strip 'strip' as in the Adafruit sample
// from: https://learn.adafruit.com/adafruit-neopixel-uberguide?view=all#arduino-library-installation
// If you named it differently used that name here instead of 'strip'
{1} * {2} = new {0}(strip);

// 3 - Paste inside loop() to run the pattern.
{2}->playPattern();  
  
// 4 - Optional: Use this to stop the pattern while it is in the middle of running.
//{2}->stopPattern();

		""".format(self.getGeneratedLedPatternClassName(patternId),
		self.getBasePatternClassName(),
		self.getGeneratedLedPatternClassName(patternId).lower()))
		readMeFile.close()
		pass
		
'''
End: Adafruit Code Generator
'''

		
register(
    "python_fu_code_minion_led_pattern_generator",
    "Generates LED pattern from Image",
    """Uses the pixels in the current image to generate an LED pattern for Arduino. Layers will be used as frames in the pattern and only visible layers are used. Layer Groups are also supported and will be included in the final patten if visible. 
	
UI Fields Help
LED Type: Type of LEDs for which to generated the code for. 
- Currently supporting: 
-- Adafruit NeoPixel for Arduino
	
Image: The GIMP image to use as an imput for the generation of the LED pattern. 
	
Frame Delay: Delay in millisaconds of each frame. This is how long each layer of pixels will be shown for while the pattern is running. 
	
Row Order Type: This is the order in which the pixels translated to LED positions. Used to support common wiring forms for LED Matrices. 
- Currently supporting: 
-- Standard: This is row major.
-- Flip Odd: This will flip the order of the pixels in the odd rows. First pixel will mapped to last LED and last pixel will map to the first LED.
-- Flip Even: This will flip the order of the pixels in the even rows. First pixel will mapped to last LED and last pixel will map to the first LED.
	
Directory: Directory where the code will be placed once generation is complete. It is recommended to make this your Arduino sketch folder for convenience but not required. 
	
	""",
    "Frank E. Hernandez",
    "Frank E. Hernandez",
    "2020",
    "Generate LED Pattern...",
    "*",      # Alternately use RGB, RGB*, GRAY*, INDEXED etc. (Options "" for Create a new image, "*" for Any Image" )
    [
        (PF_OPTION, "ledType", "LED Type", 0, ("Adafruit NeoPixel", "Coming Soon...")),
        (PF_IMAGE, "image", "Input image", None),
        (PF_SPINNER, "frameDelay", "Frame Delay (ms)", 200, (1, 80000, 1)),
		(PF_OPTION, "rowOrderType", "Row Ordering", 0, ("Standard", "Flip Odd", "Flip Even")),
        
		(PF_DIRNAME, "dir", "Directory", os.getcwd())

		# Python-Fu Type, paramter-name, ui-text, default
    ],
    [],
    generate_led_pattern, menu="<Image>/File/Create" )

main()