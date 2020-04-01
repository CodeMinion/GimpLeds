#!/usr/bin/env python


import os
import struct
from gimpfu import *

def generate_led_pattern(ledType, newimg, 
               frameDelay, imagefile, dir):
    
	
	filename, file_extension = os.path.splitext(newimg.name)
	
	# Create the destination file
	outFilename = os.path.join(dir, '{0}_Pattern.h'.format(filename))
	ledPatternFile = open(outFilename, "w")
	
	constPattern = nameToConst(filename)
	writeHeaders(constPattern, ledPatternFile)
	
	# List of frames in the pattern. 
	patternFrames = []
	
	# Get layers in the newimg
	imageLayers = newimg.layers
	for layer in imageLayers:
		# TODO convert the layer name to a const name 
		constLayer = nameToConst(layer.name)
		
		# Write the start of the pattern
		writeFrameConst(constLayer, ledPatternFile)
		
		# Track the pattern name
		patternFrames.append(constLayer)
		
		lastLed = (layer.height * layer.width) - 1 
		ledIndex = 0
		
		# Get the pixels in the layer
		for y in range(0, layer.height):
			for x in range(0, layer.width):
				num_channels, pixel = pdb.gimp_drawable_get_pixel(layer, x, y)
				
				#ledPatternFile.write('Channels {0}'.format(num_channels))
				# TODO If it has 4 channels then we have alpha in the end, we'll use it to dim the LED color. 
				colorRatio = 1
				if num_channels == 4:
					colorRatio = pixel[3]/255.0
					#ledPatternFile.write('{0}'.format(colorRatio))
					
				R = "%02x" %dimColorByRatio(pixel[0], colorRatio)
				G = "%02x" %dimColorByRatio(pixel[1], colorRatio)
				B = "%02x" %dimColorByRatio(pixel[2], colorRatio)
				#ledPatternFile.write('LED: {0} - R-{1}, G-{2}, B-{3}'.format(ledIndex, R, G, B ))
				
				if ledIndex < lastLed:
					ledPatternFile.write('0x{0}{1}{2}, '.format(R,G,B))
				else: 
					ledPatternFile.write('0x{0}{1}{2}\n}};\n'.format(R,G,B))
				
				
				if ledIndex % 10 == 9:
					ledPatternFile.write("\n")
					
				ledIndex = ledIndex + 1
		
	# Write the pattern to the file. 
	writePatternConst(constPattern, ledPatternFile)
		
	for frame in patternFrames:
		ledPatternFile.write("{0},\n".format(frame))
		pass
	ledPatternFile.write("};\n")
	
	# TODO Create Pattern playback methods.

	writeFooters(constPattern, ledPatternFile)
		
	return

def nameToConst(name):
	outName = name.upper().replace(" ", "_")
	return outName

# Dims a color by a given ratio. Because we are creating LED 
# patterns and those don't have opacity, we'll just update the 
# color by the opacity ratio	
def dimColorByRatio(color, ratio):
	outColor = int(color * ratio)
	return outColor

# Helper to write the start of a frame to the Arduino file.
def writeFrameConst(frameName, outFile):
	outFile.write("\nconst long {0}[] PROGMEM = {{ \n".format(frameName))

# Helper to write the start of a pattern to the Arduino file.
# A Pattern is composed of Frames.
def writePatternConst(patternName, outFile):
	outFile.write("\nconst long *const {0}[] PROGMEM = {{ \n".format(patternName))

# Helper to write any headers needed	
def writeHeaders(patternName, outFile):
	outFile.write("#ifndef {0}_H\n".format(patternName))
	outFile.write("#define {0}_H\n".format(patternName))
	outFile.write("#include <avr/pgmspace.h>\n")

#Helper to write any footers needed.
def writeFooters(patternName, outFile):
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