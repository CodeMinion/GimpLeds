# Gimp LED Generator Plug-in
Plug-in to create code to drive LEDs from an image file in Gimp. 


## How does it work?
The plug-in takes one image to represent a single LED pattern (or animation) and each layer to be a step (or keyframe) in the LED pattern. To do this it uses the following Gimp elements:

  - **Image:** Uses the layer order as the final frame order in the animation in a top down form where the top most layer will be the first frame, the layer below it will be the second frame, etc.  
 
  - **Layer:** From the layer, the plugin will extract the LED index as well as the LED color. It will perform this extraction in a row-major order.
 
    - **Opacity:** Depending on the code generator the layer's opacity may be multiplied by the actual pixel color when creating the final color for the LED. This is because LED might not support the concept of alpha. 
    
    - **Pixel Alpha:** If a given pixel has an alpha channel its value will also be proved to the generators. In some generators this alpha will be multiplied with the pixel RGB values to create the final LED color from that pixel. 
    
  - **Layer Group:** Layer groups are supported by this plug-in and each layer inside the group will be converted to a keyframe in the final LED pattern.   
  
  - **Layer Visibility**: The layer's visibility is used to decide which layers will be used in the generation of the pattern. 
    - **Note:** This is not to be confused with opacity. A layer can be marked visible in the editor and yet have an opacity of 0 (invisible) and this will generate a frame for that layer with all LEDs off. Layer visibility in Gimp is marked by the eye icon next to a layer or layer group.
    

 - **Layer Order:** The plugin will use a top-down order when generating the LED pattern/animation keyframes. This means that the top-most layer will generate the first frame in the pattern, the second top-most layer the second frame, the third top-most layer the third frame and so on. The same order applies when using layer groups. 



## Installing the Plug-in
 - **Preferences:** In Gimp go to the preferences dialog, **Edit**->**Preferences**. 
 
 - **Plugins Folder:** While in that dialog expand find the plugin folders under ''Folders'' **Folders**->**Plug-ins**.
 
 - **Copy Plug-in:** Navigate to the plug-ins folder under your user directory and paste the **.py** file included in this repo there.
 
 - **Restart Gimp:** For plug-in changes to be picked up by Gimp you must restart Gimp, so if you have Gimp running when you paste this plugin in that directory then just restart. The next time Gimp starts this plugin will appear under **File**->**Create**-> **Generate LED Pattern...**

## Plug-in Fields
**Note:** This Gimp LED Generator plugin requires that at least one image is active. If accessing the plug-in without an active image, the plug-in option will just appear grayed out until an image is loaded or created. 

- **LED Type:** This option represents the LED Type for which the code will be generated. 
    - **Currently Supported**:
        - Adafruit NeoPixel for Arduino  

- **Input Image:** This is the Gimp image that will be used as a source when generating the code to drive the LEDs. If other images are open in Gimp simply select from the drop-down the image to use as an input. 

- **Frame Delay:** This represents how many milliseconds each frame will be shown for or how long the delay will be before we show the next frame. 

- **Row Ordering:** This represents how each row of pixels will be translated. If your row of LEDs are laid out in row-major order then standard (default) is all you need. Used to support some basic wiring types for an LED strip.
    - **Options:**
      - **Standard:** Row-major ordering. 
      
      - **Flip Odd:** This will reverse the order of the pixels in every odd row. This means that the first pixel will map to the last LED in that section of the trip, the second pixel will map to the seconds to last LED in that section of the trip, and so on. 
      
      - **Flip Even:** This will reverse the order of the pixels in every even row. This means that the first pixel will map to the last LED in that section of the trip, the second pixel will map to the seconds to last LED in that section of the trip, and so on.

- **Layout: (TODO)** Specifies how the LEDs are laid out in the hardware.
  - **Options:**
    - **Strip:** The LEDs are in a strip of LEDs. 
    
    - **Single Matrix: (TODO)** The output will control an LED matrix. The actual manipulation of the information is dependent on the code generator but for now it is assumed that the matrix is in row-major order.
    
    - **Tile Matrix: (TODO)** The output will control tiled matrices. In this mode each layer is taken as a representation of a single tile (matrix) in the tileset with the ordering of the layers being used as the connection order of the tileset. Each matrix tile is assumed to be in row-major order. 

- **Directory:** The destination directory where the code will be generated to. Ideally this should be the folder where your sketch (or project) lives to make integration simple. 
 
## Generated Code
**Note:** The actual code generated is dependent on the code generator selected but this could should drive the LEDs on the target platform and expose a simple interface of **playPattern()**, **stopPattern()**.
- Adafruit NeoPixel generates the following:
  - **Pattern_<GimpImageFilename>.h:** Pattern class with all the information needed to execute the pattern on an Adafruit NeoPixel strip on Arduino. 
  - **GimpLedPatern.h:** Abstract class to provide some consistency among all patterns generated. 
  - **README_Pattern_<GimpeImageFilename>.txt:** Information text file with instructions on how to integrate the generated pattern into the final sketch. Follow these instructions and copy-paste the instructed lines where specified to be up and running in no time. 

License
----

**Gimp LED Generator Plug-in** is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version. **Gimp LED Generator Plug-in** is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the [GNU Lesser General Public License](https://www.gnu.org/licenses/lgpl-3.0.en.html) for more details. You should have received a copy of the GNU Lesser General Public License along with **Gimp LED Generator Plug-in**. If not, see [this](https://www.gnu.org/licenses/lgpl-3.0.en.html)




