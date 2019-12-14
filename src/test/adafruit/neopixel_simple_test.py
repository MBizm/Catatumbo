#!/usr/bin/env python
# encoding: utf-8
'''
TODO


@author:     MBizm

@copyright:  2019 organization_name. All rights reserved.

@license:    Apache License 2.0

@deffield    created: December 2019
@deffield    updated: Updated
'''
from adafruit.core.neopixel_base import NeoPixelBase
import board
import neopixel
import sys
from adafruit.core.neopixel_colors import NeoPixelColors

class NeoPixelOneColorsTest(NeoPixelBase):

    """
        predefined schemas based on ForecastNeoPixelColors colorset
    """
    SCHEMA_ALLTEMPHIGH  = '1'
    SCHEMA_ALLTEMPMED   = '2'
    SCHEMA_ALLTEMPLOW   = '3'
    SCHEMA_ALLCLOUDY    = '4'
    SCHEMA_ALLRAINY     = '5'

    def __init__(self, 
                 pixelpin       = board.D18, 
                 pixelnum       = 0, 
                 pixelorder     = neopixel.RGBW,
                 schema_type    = 1):
        
        super().__init__(pixelpin, pixelnum, pixelorder, NeoPixelColors)
        
        self.initColorTest(schema_type)

    def initColorTest(self, color_mode = 1):

        if color_mode == type(self).SCHEMA_ALLTEMPHIGH:                          #all varieties of high temperature
            sampleboard = (NeoPixelColors.W_BLUE,)        #    + heavy rain
        elif color_mode == type(self).SCHEMA_ALLTEMPMED:                        #all varieties of mid temperature
            sampleboard = (NeoPixelColors.W_LIGHT_GREEN,)       #    + heavy rain
        elif color_mode == type(self).SCHEMA_ALLTEMPLOW:                        #all varieties of low temperature
            sampleboard = (NeoPixelColors.W_MAGENTA,)              #storm
        elif color_mode == type(self).SCHEMA_ALLCLOUDY:                        #compare cloudiness of all
            sampleboard = (NeoPixelColors.W_LIGHT_ORANGE,)      #    + cloudy
        elif color_mode == type(self).SCHEMA_ALLRAINY:                        #compare raininess of all
            sampleboard = (NeoPixelColors.W_RED,)       #    + heavy rain
        else:
            #stay with the default initialization
            return
    
        sectionsize = int(self.getNumPixels() / len(sampleboard))
        
        self.setBrightness(100)
    
        # preset pixel colors
        for i in range(self.getNumPixels()-1):
            # fill up remaining pixels
            if(int(i / sectionsize) >= len(sampleboard)):
                self.pixels[i] = sampleboard[len(sampleboard) - 1] 
            # preset pixel colors according to color space set  
            else:
                self.pixels[i] = sampleboard[int(i / sectionsize)]
                print('[' + str(i) + '] ' + str(sampleboard[int(i / sectionsize)]))
        self.pixels.show()

if __name__ == '__main__':
    strip = NeoPixelOneColorsTest(pixelnum = int(sys.argv[2]), pixelorder = neopixel.GRB, schema_type = sys.argv[1])  