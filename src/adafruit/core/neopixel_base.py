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

import board
import neopixel
from adafruit.core.neopixel_colors import NeoPixelColors

class NeoPixelBase(object):
    
    """
    STATIC CLASS ATTRIBUTES
    """

    
    """
    OBJECT ATTRIBUTES
    """
    
    """
        contructor
        
        :param    pixelorder: defines the LED strip type. use NeoPixel class attributes RGB, GRB, RGBW, GRBW
        :type     pixelorder: int
        TODO
    """  
    def __init__(self, 
                 pixelpin       = board.D18, 
                 pixelnum       = 0, 
                 pixelorder     = neopixel.RGBW,
                 color_schema   = NeoPixelColors):
        
        #initializing color schema
        #this will dependent whether its a RGB or RGBW strip define the predefined color values
        color_schema(pixelorder)
        
        self.pixels = neopixel.NeoPixel(pixelpin, pixelnum, brightness=0.2, auto_write=False,
                                   pixel_order=pixelorder)
    
    """
    TODO
    """
    def setBrightness(self, brightness):
        self.pixels.brightness = brightness
        self.pixels.show()
        #print('brightness level: ' + str(brightness))

    """
        return the numer of led pixels defined for the current instance
        
        :returns: number of pixels
    """
    def getNumPixels(self):
        return self.pixels.n