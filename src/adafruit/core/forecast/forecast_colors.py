#!/usr/bin/env python
# encoding: utf-8
'''
This is a sample of colors for forecast apps
Colors are defined on base class based on the perceived colors resulting from an WS2811 LED strip.

Current version of the class only addresses RGBW capable chips

@author:     MBizm

@copyright:  2019 organization_name. All rights reserved.

@license:    Apache License 2.0

@deffield    created: November 2019
@deffield    updated: Updated
'''
from ..neopixel_colors import NeoPixelColors

class ForecastNeoPixelColors(NeoPixelColors):

    """
    STATIC CLASS ATTRIBUTES
    """
    W_HITMP             = None  #high temperature, no rain, no clouds
    W_HITMP_SLRAINY     = None  #high temperature, slightly rainy
    W_HITMP_RAINY       = None  #high temperature, rainy
    W_HITMP_SLCLOUDY    = None  #high temperature, slightly cloudy
    W_HITMP_CLOUDY      = None  #high temperature, cloudy
    
    W_MIDTMP            = None  #mid temperature, no rain, no clouds
    W_MIDTMP_SLCLOUDY   = None  #mid temperature, slightly cloudy
    W_MIDTMP_CLOUDY     = None  #mid temperature, cloudy
    W_MIDTMP_SLRAINY    = None  #mid temperature, slightly rainy
    W_MIDTMP_RAINY      = None  #mid temperature, rainy
    
    W_LOWTMP            = None  #low temperature, no rain, no clouds
    W_LOWTMP_SLRAINY    = None  #low temperature, slightly rainy
    W_LOWTMP_RAINY      = None  #low temperature, rainy
    W_LOWTMP_SLCLOUDY   = None  #low temperature, slightly cloudy
    W_LOWTMP_CLOUDY     = None  #low temperature, cloudy
    
    W_SNOW              = None
    W_STORM             = None

    """
        initializer for RGBW LED strip
    """     
    def __initDerivedColors__(self):
        
        super().__initDerivedColors__()

        type(self).W_HITMP             = ForecastNeoPixelColors.W_RED             #high temperature, no rain, no clouds
        type(self).W_HITMP_SLRAINY     = ForecastNeoPixelColors.W_WARM_MAGENTA    #high temperature, slightly rainy
        type(self).W_HITMP_RAINY       = ForecastNeoPixelColors.W_LIGHT_MAGENTA   #high temperature, rainy
        type(self).W_HITMP_SLCLOUDY    = ForecastNeoPixelColors.W_WARM_ORANGE     #high temperature, slightly cloudy
        type(self).W_HITMP_CLOUDY      = ForecastNeoPixelColors.W_LIGHT_ORANGE    #high temperature, cloudy
        
        type(self).W_MIDTMP            = ForecastNeoPixelColors.W_WARM_YELLOW     #mid temperature, no rain, no clouds
        type(self).W_MIDTMP_SLCLOUDY   = ForecastNeoPixelColors.W_YELLOW          #mid temperature, slightly cloudy
        type(self).W_MIDTMP_CLOUDY     = ForecastNeoPixelColors.W_LIGHT_YELLOW    #mid temperature, cloudy
        type(self).W_MIDTMP_SLRAINY    = ForecastNeoPixelColors.W_LIGHT_SALMON    #mid temperature, slightly rainy
        type(self).W_MIDTMP_RAINY      = ForecastNeoPixelColors.W_LAVENDERBLUSH   #mid temperature, rainy
        
        type(self).W_LOWTMP            = ForecastNeoPixelColors.W_LIGHT_BLUE      #low temperature, no rain, no clouds
        type(self).W_LOWTMP_SLRAINY    = ForecastNeoPixelColors.W_CORNFLOWERBLUE  #low temperature, slightly rainy
        type(self).W_LOWTMP_RAINY      = ForecastNeoPixelColors.W_LIGHT_PURPLE    #low temperature, rainy
        type(self).W_LOWTMP_SLCLOUDY   = ForecastNeoPixelColors.W_CYAN            #low temperature, slightly cloudy
        type(self).W_LOWTMP_CLOUDY     = ForecastNeoPixelColors.W_AQUAMARINE      #low temperature, cloudy
        
        type(self).W_SNOW              = ForecastNeoPixelColors.W_LIGHT_WHITE
        type(self).W_STORM             = ForecastNeoPixelColors.W_LIGHT_MINTH