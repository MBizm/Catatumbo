'''
Test program for NeoPixelMultiBase - with several physical strips representing the color values
This will initiate the led strips based on the defined color values and categories taken from Forecast color set.
The color set will be spread across the entire set of pixels available by the number of physical led strips.
A color set represents all potential values within the forecast category, e.g for high temperature:
temp high 
 + no clouds
 + scuttered clouds
 + cloudy
 + slightly rainy
 + heavy rain

Potential color categories are:
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
from adafruit.core.neopixel_multibase import NeoPixelMultiBase
from adafruit.core.forecast.forecast_colors import ForecastNeoPixelColors
import configparser
from configparser import NoOptionError, NoSectionError
from adafruit.core.cmd_functions import cmd_options

class NeoPixelMultiStripsColorsTest(NeoPixelMultiBase):
    
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
                 color_mode     = 1,
                 brightness     = None):
        
        # initialize super class
        super().__init__()
        
        # read config for led strips
        config = configparser.RawConfigParser()
        config.read('test/adafruit/forecast/MULTIBASECONFIG.properties')
        
        # loop all individual led strip configurations
        counter = 1
        while counter > -1:
            try:
                section = "Strip" + str(counter)

                strip = NeoPixelMultiBase.__Config__(pixelpin       = config.get(section, "PixelPin" + str(counter)),
                                                     pixelnum       = config.get(section, "PixelNum" + str(counter)),
                                                     pixelorder     = config.get(section, "PixelOrder" + str(counter)),
                                                     color_schema   = ForecastNeoPixelColors)
                super().addStrip(strip)
                
            except (NoOptionError, NoSectionError):
                counter = -1
                # ensure we directly step out of loop
                continue
            
            counter = counter + 1
        
        # set brightness level for all strips
        if brightness is None:
            try:
                self.setBrightness(config.get("GeneralConfiguration", "Brightness"))
            except (NoOptionError, NoSectionError):
                self.setBrightness(0.3)
        else:
            self.setBrightness(brightness)
            
        # set color values
        self.initColorTest(color_mode)


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
    # configuration for multi base example is available via config file
    # only color mode can be selected via cmd line (how about brightness)
    opts = cmd_options(NeoPixelMultiStripsColorsTest.__version__, 
                       NeoPixelMultiStripsColorsTest.__updated__)
    
    NeoPixelMultiStripsColorsTest(color_mode=opts.mode,
                                  brightness=opts.bright)