#!/usr/bin/env python
# encoding: utf-8
'''
This class defines some basic colors based on the perceived colors resulting from an WS2811 LED strip.
The neopixel driver does not allow an accurate mapping of RGB/HSV color values. Even small blue values will result in very bright result.

Available colors depend on the type of the neopixel LED strip and can be seen from the respective init-methods. 

@author:     MBizm

@copyright:  2019 organization_name. All rights reserved.

@license:    Apache License 2.0

@deffield    created: November 2019
@deffield    updated: Updated
'''
import neopixel

class NeoPixelColors(object):

    """
    STATIC CLASS ATTRIBUTES
    """
    W_RED              = None
    
    W_WARM_ORANGE      = None
    W_LIGHT_ORANGE     = None
    
    W_WARM_YELLOW      = None     #yellow with a redish nuance
    W_YELLOW           = None
    W_LIGHT_YELLOW     = None     #brighter yellow with a greenish accent
    
    W_WARM_MAGENTA     = None     #magenta with a redish nuance
    W_MAGENTA          = None
    W_LIGHT_MAGENTA    = None     #brighter magenta with more blueish accent
    
    W_LIGHT_SALMON     = None
    
    W_LAVENDERBLUSH    = None     #very bright version of rose
    
    W_LIGHT_GREEN      = None     #green with a tendency to limegreen
    W_LIGHT_MINTH      = None     #light green with bright white
    W_LIGHT_SEAGREEN   = None
    
    W_CYAN             = None     #light turkis
    
    W_AQUAMARINE       = None     #light turkis with greenish accent
    
    W_LIGHT_BLUE       = None     #brighter blue with a nuance white
    W_BLUE             = None
    W_CORNFLOWERBLUE   = None     #purple with blueish accent
    
    W_LIGHT_PURPLE     = None     #brighter purple with a redish nuance 
    
    W_LIGHT_WHITE      = None     #brighter white
    W_WHITE            = None
    
    W_BLACK            = None
    
    
    """
        contructor
        
        :param    pixelorder: defines the LED strip type. use NeoPixel class attributes RGB, GRB, RGBW, GRBW
        :type     pixelorder: int
    """  
    def __init__(self, pixelorder):
        if pixelorder == neopixel.GRB or pixelorder == neopixel.RGB:
            self.__initRGB__()
        elif pixelorder == neopixel.GRBW or pixelorder == neopixel.RGBW:
            self.__initRGBW__()

        self.__initDerivedColors__()

    """
        initializer for RGBW LED strip
    """     
    def __initRGBW__(self):
   
        type(self).W_RED              = (255,0,0,0)
        
        type(self).W_WARM_ORANGE      = (255,20,0,0)
        type(self).W_LIGHT_ORANGE     = (255,60,0,0)
        
        type(self).W_WARM_YELLOW      = (255,100,0,0)     #yellow with a redish nuance
        type(self).W_YELLOW           = (255,150,1,0)
        type(self).W_LIGHT_YELLOW     = (255,210,3,0)     #brighter yellow with a greenish accent
        
        type(self).W_WARM_MAGENTA     = (255,0,3,0)       #magenta with a redish nuance
        type(self).W_MAGENTA          = (255,0,6,0)
        type(self).W_LIGHT_MAGENTA    = (255,0,17,0)      #brighter magenta with more blueish accent
        
        type(self).W_LIGHT_SALMON     = (255,60,7,0)
        
        type(self).W_LAVENDERBLUSH    = (255,80,15,0)     #very bright version of rose
        
        type(self).W_LIGHT_GREEN      = (0,63,0,0)        #green with a tendency to limegreen
        type(self).W_LIGHT_MINTH      = (0,255,0,255)     #light green with bright white
        type(self).W_LIGHT_SEAGREEN   = (0,63,15,0)
        
        type(self).W_CYAN             = (50,150,127,0)    #light turkis
        
        type(self).W_AQUAMARINE       = (50,180,60,0)     #light turkis with greenish accent
        
        type(self).W_LIGHT_BLUE       = (0,70,255,10)     #brighter blue with a nuance white
        type(self).W_BLUE             = (0,0,255,0)
        type(self).W_CORNFLOWERBLUE   = (70,0,255,0)      #purple with blueish accent
        
        type(self).W_LIGHT_PURPLE     = (140,0,255,0)     #brighter purple with a redish nuance 
        
        type(self).W_LIGHT_WHITE      = (255,255,255,255) #brighter white
        type(self).W_WHITE            = (255,255,255,0)
        
        type(self).W_BLACK            = (0,0,0,0)
        
    
    """
        initializer for RGB LED strip
    """ 
    def __initRGB__(self):
        
        type(self).W_RED              = (255,0,0)
        
        type(self).W_WARM_ORANGE      = (255,20,0)
        type(self).W_LIGHT_ORANGE     = (255,60,0)
        
        type(self).W_WARM_YELLOW      = (255,100,0)       #yellow with a redish nuance
        type(self).W_YELLOW           = (255,150,1)
        type(self).W_LIGHT_YELLOW     = (255,210,3)       #brighter yellow with a greenish accent
        
        type(self).W_WARM_MAGENTA     = (255,0,3)         #magenta with a redish nuance
        type(self).W_MAGENTA          = (255,0,6)
        type(self).W_LIGHT_MAGENTA    = (255,0,17)        #brighter magenta with more blueish accent
        
        type(self).W_LIGHT_SALMON     = (255,60,7)
        
        type(self).W_LAVENDERBLUSH    = (255,80,15)       #very bright version of rose
        
        type(self).W_LIGHT_GREEN      = (0,63,0)          #green with a tendency to limegreen
        type(self).W_LIGHT_MINTH      = (0,255,10)        #light green with bright white
        type(self).W_LIGHT_SEAGREEN   = (0,63,15)
        
        type(self).W_CYAN             = (50,150,127)      #light turkis
        
        type(self).W_AQUAMARINE       = (50,180,60)       #light turkis with greenish accent
        
        type(self).W_LIGHT_BLUE       = (0,70,255)        #brighter blue with a nuance white
        type(self).W_BLUE             = (0,0,255)
        type(self).W_CORNFLOWERBLUE   = (70,0,255)        #purple with blueish accent
        
        type(self).W_LIGHT_PURPLE     = (140,0,255)       #brighter purple with a redish nuance 
        
        type(self).W_LIGHT_WHITE      = (233,233,255)     #brighter white
        type(self).W_WHITE            = (255,255,255)
          
        
        type(self).W_BLACK            = (0,0,0)
        
    """
        empty implementation for derived classes to define own color definitions on base colors
    """ 
    def __initDerivedColors__(self):
        pass