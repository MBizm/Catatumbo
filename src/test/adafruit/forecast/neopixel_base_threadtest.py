#!/usr/bin/env python
# encoding: utf-8
'''
Test program for simple NeoPixelBase for testing capability to address multiple strips at once.
The instantiated strips will permanently change their brightness via two separate thread, to proof capability of adapted Adafruit_Blinka controller.
See https://github.com/MBizm/Adafruit_Blinka/blob/master/src/adafruit_blinka/microcontroller/bcm283x/neopixel.py

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
from adafruit.core.forecast.forecast_colors import ForecastNeoPixelColors
from adafruit.core.util.cmd_functions import cmd_options
import board
import neopixel
import time
from threading import Thread

# defines the time in seconds that it will take to from an illuminated to faded state
# calculation will be based on 190 individual steps for dimming from which 100 are twice the speed - step divider 280
CYCLE_TIME = 15

class NeoPixelForecastColorsThreadTest(NeoPixelBase):

    __version__ = 0.1
    __updated__ = '2019-12-26'

    """
        predefined schemas based on ForecastNeoPixelColors colorset
    """
    SCHEMA_ALLTEMPHIGH  = '1'
    SCHEMA_ALLTEMPMED   = '2'
    SCHEMA_ALLTEMPLOW   = '3'
    SCHEMA_ALLCLOUDY    = '4'
    SCHEMA_ALLRAINY     = '5'

    def fillStrip(self, color_mode = 1):

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
    
        self.setPixelBySampleboard(sampleboard)
 
########################################
#         UTILITY METHODS              #
########################################
def setBrightness(strip, brightness, delay):
    strip.setBrightness(brightness)
    strip.show()
    #print('brightness level: ' + str(brightness))
    time.sleep(delay)

def circleBrightness(strip):
    while True:
        # direction = 0 - fading from illuminated state, direction = 1 - illuminating
        for direction in range (0, 2, 1):
            # iterating brightness level in the range of 1.0 and 0.1, step size 0.01
            for i in range(100, 0, -1):
                
                # iterating brightness level in the range of 0.0 and 0.099, step size 0.001
                if i == 100 and direction == 1:
                    for j in range(99, 0, -1):
                        setBrightness(strip, abs(100 * direction - j) / 1000,
                                      CYCLE_TIME / (2 * (90 + 50)))
                
                # iterating brightness level in the range of 1.0 and 0.1, step size 0.01
                # skip the range between 0.1 and 0
                if (direction == 0 and i >= 10) or (direction == 1 and i <= 90):
                    setBrightness(strip, abs(100 * direction - i) / 100,
                                  CYCLE_TIME / (90 + 50))
                
                # iterating brightness level in the range of 0.099 and 0.0, step size 0.001
                if i == 10 and direction == 0:
                    for j in range(99, 0, -1):
                        setBrightness(strip, abs(100 * direction - j) / 1000,
                                      CYCLE_TIME / (2 * (90 + 50)))

########################################
#                MAIN                  #
########################################
if __name__ == '__main__':
    # interpret cmd line arguments
    opts = cmd_options(NeoPixelForecastColorsThreadTest.__version__, 
                       NeoPixelForecastColorsThreadTest.__updated__)
    
    np1 = NeoPixelForecastColorsThreadTest(pixelpin    = board.D13, 
                                    pixelnum     = 145, 
                                    pixelorder   = neopixel.GRB, 
                                    color_schema = ForecastNeoPixelColors,
                                    brightness   = float(opts.bright))

    np1.fillStrip(opts.mode)
    
    t1 = Thread(target = circleBrightness, 
                args = (np1, ))
    
    mode = int(opts.mode) + 1
    if (mode > 5):
        mode = 1
    
    np2 = NeoPixelForecastColorsThreadTest(pixelpin    = board.D18, 
                                    pixelnum     = 61, 
                                    pixelorder   = neopixel.GRBW, 
                                    color_schema = ForecastNeoPixelColors,
                                    brightness   = float(opts.bright))
    
    np2.fillStrip(str(mode))
    
    t2 = Thread(target = circleBrightness, 
                args = (np2, ))
    
    t1.start()
    t2.start()
