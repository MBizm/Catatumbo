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
from adafruit.core.forecast.forecast_colors import ForecastNeoPixelColors
import sys

class NeoPixelForecastColorsTest(NeoPixelBase):

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
        
        super().__init__(pixelpin, pixelnum, pixelorder, ForecastNeoPixelColors)
        
        self.initColorTest(schema_type)

    def initColorTest(self, schema_type = 1):

        if schema_type == type(self).SCHEMA_ALLTEMPHIGH:                          #all varieties of high temperature
            sampleboard = (ForecastNeoPixelColors.W_HITMP,              #temp high 
                           ForecastNeoPixelColors.W_HITMP_SLCLOUDY,     #    + scuttered clouds
                           ForecastNeoPixelColors.W_HITMP_CLOUDY,       #    + cloudy
                           ForecastNeoPixelColors.W_HITMP_SLRAINY,      #    + slightly rainy
                           ForecastNeoPixelColors.W_HITMP_RAINY)        #    + heavy rain
        elif schema_type == type(self).SCHEMA_ALLTEMPMED:                        #all varieties of mid temperature
            sampleboard = (ForecastNeoPixelColors.W_MIDTMP,             #temp mid 
                           ForecastNeoPixelColors.W_MIDTMP_SLCLOUDY,    #    + scuttered clouds
                           ForecastNeoPixelColors.W_MIDTMP_CLOUDY,      #    + cloudy
                           ForecastNeoPixelColors.W_MIDTMP_SLRAINY,     #    + slightly rainy
                           ForecastNeoPixelColors.W_MIDTMP_RAINY)       #    + heavy rain
        elif schema_type == type(self).SCHEMA_ALLTEMPLOW:                        #all varieties of low temperature
            sampleboard = (ForecastNeoPixelColors.W_LOWTMP,             #temp low 
                           ForecastNeoPixelColors.W_LOWTMP_SLCLOUDY,    #    + scuttered clouds
                           ForecastNeoPixelColors.W_LOWTMP_CLOUDY,      #    + cloudy
                           ForecastNeoPixelColors.W_LOWTMP_SLRAINY,     #    + slightly rainy
                           ForecastNeoPixelColors.W_LOWTMP_RAINY,       #    + heavy rain
                           ForecastNeoPixelColors.W_SNOW,               #snow
                           ForecastNeoPixelColors.W_STORM)              #storm
        elif schema_type == type(self).SCHEMA_ALLCLOUDY:                        #compare cloudiness of all
            sampleboard = (ForecastNeoPixelColors.W_HITMP,              #temp high 
                           ForecastNeoPixelColors.W_HITMP_SLCLOUDY,     #    + scuttered clouds
                           ForecastNeoPixelColors.W_HITMP_CLOUDY,       #    + cloudy
                           ForecastNeoPixelColors.W_MIDTMP,             #temp mid 
                           ForecastNeoPixelColors.W_MIDTMP_SLCLOUDY,    #    + scuttered clouds
                           ForecastNeoPixelColors.W_MIDTMP_CLOUDY,      #    + cloudy
                           ForecastNeoPixelColors.W_LOWTMP,             #low high 
                           ForecastNeoPixelColors.W_LOWTMP_SLCLOUDY,    #    + scuttered clouds
                           ForecastNeoPixelColors.W_LOWTMP_CLOUDY)      #    + cloudy
        elif schema_type == type(self).SCHEMA_ALLRAINY:                        #compare raininess of all
            sampleboard = (ForecastNeoPixelColors.W_HITMP,              #temp high 
                           ForecastNeoPixelColors.W_HITMP_SLRAINY,      #    + slightly rainy
                           ForecastNeoPixelColors.W_HITMP_RAINY,        #    + heavy rain
                           ForecastNeoPixelColors.W_MIDTMP,             #temp mid 
                           ForecastNeoPixelColors.W_MIDTMP_SLRAINY,     #    + slightly rainy
                           ForecastNeoPixelColors.W_MIDTMP_RAINY,       #    + heavy rain
                           ForecastNeoPixelColors.W_LOWTMP,             #low high 
                           ForecastNeoPixelColors.W_LOWTMP_SLRAINY,     #    + slightly rainy
                           ForecastNeoPixelColors.W_LOWTMP_RAINY)       #    + heavy rain
        else:
            #stay with the default initialization
            return
    
        sectionsize = int(self.getNumPixels() / len(sampleboard))
        
        self.setBrightness(80)
    
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
    strip = NeoPixelForecastColorsTest(pixelnum = 61, pixelorder = neopixel.GRBW, schema_type = sys.argv[1])  