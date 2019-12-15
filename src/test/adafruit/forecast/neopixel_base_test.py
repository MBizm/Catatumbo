#!/usr/bin/env python
# encoding: utf-8
'''
Test program for simple NeoPixelBase
This will initiate the led strip based on the defined color schema taken from Forecast color set.
A color set represents all potential values within the forecast category, e.g for high temperature:
temp high 
 + no clouds
 + scuttered clouds
 + cloudy
 + slightly rainy
 + heavy rain

Potential color ranges are:
    SCHEMA_ALLTEMPHIGH  = '1'
    SCHEMA_ALLTEMPMED   = '2'
    SCHEMA_ALLTEMPLOW   = '3'
    SCHEMA_ALLCLOUDY    = '4'
    SCHEMA_ALLRAINY     = '5'


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
from adafruit.core.cmd_functions import cmd_options

class NeoPixelForecastColorsTest(NeoPixelBase):

    __version__ = 0.1
    __updated__ = '2019-12-14'

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
                 color_mode     = 1,
                 brightness     = 0.2):
        
        super().__init__(pixelpin, 
                         pixelnum, 
                         pixelorder, 
                         ForecastNeoPixelColors,
                         brightness)
        
        self.initColorTest(color_mode)
        
        #self.setBrightness(brightness)

    def initColorTest(self, color_mode = 1):

        if color_mode == type(self).SCHEMA_ALLTEMPHIGH:                          #all varieties of high temperature
            sampleboard = (ForecastNeoPixelColors.W_HITMP,              #temp high 
                           ForecastNeoPixelColors.W_HITMP_SLCLOUDY,     #    + scuttered clouds
                           ForecastNeoPixelColors.W_HITMP_CLOUDY,       #    + cloudy
                           ForecastNeoPixelColors.W_HITMP_SLRAINY,      #    + slightly rainy
                           ForecastNeoPixelColors.W_HITMP_RAINY)        #    + heavy rain
        elif color_mode == type(self).SCHEMA_ALLTEMPMED:                        #all varieties of mid temperature
            sampleboard = (ForecastNeoPixelColors.W_MIDTMP,             #temp mid 
                           ForecastNeoPixelColors.W_MIDTMP_SLCLOUDY,    #    + scuttered clouds
                           ForecastNeoPixelColors.W_MIDTMP_CLOUDY,      #    + cloudy
                           ForecastNeoPixelColors.W_MIDTMP_SLRAINY,     #    + slightly rainy
                           ForecastNeoPixelColors.W_MIDTMP_RAINY)       #    + heavy rain
        elif color_mode == type(self).SCHEMA_ALLTEMPLOW:                        #all varieties of low temperature
            sampleboard = (ForecastNeoPixelColors.W_LOWTMP,             #temp low 
                           ForecastNeoPixelColors.W_LOWTMP_SLCLOUDY,    #    + scuttered clouds
                           ForecastNeoPixelColors.W_LOWTMP_CLOUDY,      #    + cloudy
                           ForecastNeoPixelColors.W_LOWTMP_SLRAINY,     #    + slightly rainy
                           ForecastNeoPixelColors.W_LOWTMP_RAINY,       #    + heavy rain
                           ForecastNeoPixelColors.W_SNOW,               #snow
                           ForecastNeoPixelColors.W_STORM)              #storm
        elif color_mode == type(self).SCHEMA_ALLCLOUDY:                        #compare cloudiness of all
            sampleboard = (ForecastNeoPixelColors.W_HITMP,              #temp high 
                           ForecastNeoPixelColors.W_HITMP_SLCLOUDY,     #    + scuttered clouds
                           ForecastNeoPixelColors.W_HITMP_CLOUDY,       #    + cloudy
                           ForecastNeoPixelColors.W_MIDTMP,             #temp mid 
                           ForecastNeoPixelColors.W_MIDTMP_SLCLOUDY,    #    + scuttered clouds
                           ForecastNeoPixelColors.W_MIDTMP_CLOUDY,      #    + cloudy
                           ForecastNeoPixelColors.W_LOWTMP,             #low high 
                           ForecastNeoPixelColors.W_LOWTMP_SLCLOUDY,    #    + scuttered clouds
                           ForecastNeoPixelColors.W_LOWTMP_CLOUDY)      #    + cloudy
        elif color_mode == type(self).SCHEMA_ALLRAINY:                        #compare raininess of all
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
    
        # preset pixel colors
        for i in range(self.getNumPixels()-1):
            # fill up remaining pixels
            if(int(i / sectionsize) >= len(sampleboard)):
                self.setPixel(i, sampleboard[len(sampleboard) - 1]) 
            # preset pixel colors according to color space set  
            else:
                self.setPixel(i, sampleboard[int(i / sectionsize)])
                print('[' + str(i) + '] ' + str(sampleboard[int(i / sectionsize)]))
        self.show()
 

########################################
#                MAIN                  #
########################################
if __name__ == '__main__':
    # interpret cmd line arguments
    opts = cmd_options(NeoPixelForecastColorsTest.__version__, 
                       NeoPixelForecastColorsTest.__updated__,
                       par = "extended")
    
    NeoPixelForecastColorsTest(pixelpin     = opts.port, 
                               pixelnum     = int(opts.len), 
                               pixelorder   = opts.schema, 
                               color_mode   = opts.mode,
                               brightness   = float(opts.bright))


    
