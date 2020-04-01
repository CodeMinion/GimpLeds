#!/usr/bin/env python


import os
from gimpfu import *

def generate_led_pattern(ledType, newimg, 
               frameDelay, imagefile, dir):
    
	
	filename, file_extension = os.path.splitext(newimg.name)
	
	constPattern = nameToConst(filename)
		
	# List of frames in the pattern. 
	patternFrames = []
	
	ledFrames = []
	# Get layers in the newimg
	imageLayers = newimg.layers
	for layer in imageLayers:
		# TODO convert the layer name to a const name 
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
					KEY_COLOR_BLUE: pixel[1], 
					KEY_COLOR_GREEN: pixel[2], 
					KEY_COLOR_ALPHA: ledAlpha
					}
					
				# Track LED
				pixelColors.append(pixelColor)
					
		# Track pattern.
		ledFrame = {
			KEY_FRAME_ID: constLayer,
			KEY_FRAME_PIXEL_COLORS: pixelColors
		}
		ledFrames.append(ledFrame)
		
	# Build LEd Pattern
	outLedPattern = {
		KEY_PATTERN_ID: constPattern,
		KEY_PATTERN_DELAY: frameDelay,
		KEY_PATTERN_FRAMES: ledFrames
	}
	
	
	ledCodeGenerator = AdafruitNeoPixelStripCodeGenerator(outLedPattern, filename, dir)
	ledCodeGenerator.generate()
		
	return

	
def nameToConst(name):
	outName = name.upper().replace(" ", "_")
	return outName

'''
 JSON Intermediate generation section
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
# Color keys, stored in a range between 0-255
KEY_COLOR_RED = "R"
KEY_COLOR_GREEN = "G"
KEY_COLOR_BLUE = "B"
KEY_COLOR_ALPHA = "A"
'''
----------------- END of JSON Intermediate generation section -----
'''	

'''
TODO Move to Adafruit Code Generator
'''

class AdafruitNeoPixelStripCodeGenerator: 
	
	# File to which to write the generated code to. 
	mOutFile = None
	mLedPattern = None
	
	LIMIT_LINE_LENTH = 10
	LIMIT_LINE_BREAK = 9
	
	def __init__(self, ledPattern, outFileName, outDir):
		outFilename = os.path.join(outDir, '{0}_Pattern.h'.format(outFileName))
		self.mOutFile = open(outFilename, "w")
		self.mLedPattern = ledPattern
		pass
		
	def generate(self):
		# Write Header 
		patternId = self.mLedPattern[KEY_PATTERN_ID]
		self.writeHeaders(patternId, self.mOutFile)
		
		# TODO For each LED Frame Generate constant
		ledFrames = self.mLedPattern[KEY_PATTERN_FRAMES]
		
		for frame in ledFrames:
			# TODO Write Frame const start
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
				
				# TODO Move this into code generator which will consume the LED Pattern JSON
				if pixelIndex < lastPixel:
					self.mOutFile.write('0x{0}{1}{2}, '.format(R,G,B))
				else: 
					self.mOutFile.write('0x{0}{1}{2}\n'.format(R,G,B))
				pass
				
				# Add a new line after 10 patterns to keep the width of the code slim
				if pixelIndex % self.LIMIT_LINE_LENTH == self.LIMIT_LINE_BREAK:
					self.mOutFile.write("\n")
				
				pixelIndex = pixelIndex + 1
			# TODO Write Frame const end 
			self.mOutFile.write("};\n")
			
			pass
			
		# TODO Generate LED Pattern constant.
		self.writePatternConst(patternId, self.mOutFile)
		for frame in ledFrames:
			self.mOutFile.write("{0},\n".format(frame[KEY_FRAME_ID]))
		pass
		self.mOutFile.write("};\n")
	
		
		# Write Footer
		self.writeFooters(patternId, self.mOutFile)
		
		pass

	# Dims a color by a given ratio. Because we are creating LED 
	# patterns and those don't have opacity, we'll just update the 
	# color by the opacity ratio	
	def dimColorByRatio(self, color, ratio):
		outColor = int(color * ratio)
		return outColor

	# Helper to write the start of a frame to the Arduino file.
	def writeFrameConst(self, frameName, outFile):
		outFile.write("\nconst long {0}[] PROGMEM = {{ \n".format(frameName))

	# Helper to write the start of a pattern to the Arduino file.
	# A Pattern is composed of Frames.
	def writePatternConst(self, patternName, outFile):
		outFile.write("\nconst long *const {0}[] PROGMEM = {{ \n".format(patternName))

	# Helper to write any headers needed	
	def writeHeaders(self, patternName, outFile):
		outFile.write("#ifndef {0}_H\n".format(patternName))
		outFile.write("#define {0}_H\n".format(patternName))
		
		#outFile.write("\n#ifndef PGMSPACE_H\n")
		#outFile.write("#define PGMSPACE_H\n")
		outFile.write("#include <avr/pgmspace.h>\n")
		#outFile.write("#endif //PGMSPACE_H\n")


	#Helper to write any footers needed.
	def writeFooters(self, patternName, outFile):
		outFile.write("\n#endif //{0}_H\n".format(patternName))


	
register(
    "python_fu_code_minion_led_pattern_generator",
    "Generates LED pattern from Image",
    "Uses the pixels in the current image to generate an LED pattern for Arduino. Layers will be used as frames in the pattern.",
    "Frank E. Hernandez",
    "Frank E. Hernandez",
    "2020",
    "Generate LED Pattern...",
    "*",      # Alternately use RGB, RGB*, GRAY*, INDEXED etc. (Options "" for Create a new image, "*" for Any Image" )
    [
        (PF_OPTION, "ledType", "LED Type", 0, ("Adafruit NeoPixel", "Coming Soon...")),
        (PF_IMAGE, "image", "Input image", None),
        (PF_SPINNER, "frameDelay", "Frame Delay (ms)", 200, (1, 80000, 1)),
		(PF_FILE, "imagefile", "Image file", ""),
        (PF_DIRNAME, "dir", "Directory", "/tmp")

		# Python-Fu Type, paramter-name, ui-text, default
    ],
    [],
    generate_led_pattern, menu="<Image>/File/Create" )

main()