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
    __strip = None
    
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
                 color_schema   = NeoPixelColors,
                 brightness     = 0.2):
        
        # check if mapping of pin is required
        pixelpin = self.__map_Pin__(pixelpin)
        
        # check if mapping of pixelorder is required
        pixelorder = self.__map_Order__(pixelorder)
                
        #initializing color schema
        #this will dependent whether its a RGB or RGBW strip define the predefined color values
        self.__schema = color_schema(pixelorder)
        
        # init strip
        self.__strip = neopixel.NeoPixel(pixelpin, 
                                         int(pixelnum), 
                                         brightness=brightness, 
                                         auto_write=False,
                                         pixel_order=pixelorder)

    ########################################
    #            UTILITY METHODS           #
    ######################################## 
    """
        checks if pixelpin parameter was provided as instance or string (in case of command line configuration)
        maps to PCM capable GPIOs - https://forums.adafruit.com/viewtopic.php?f=47&p=776283
        
        :param    pixelpin: pin defined either by neopixel attributes (board.D18, ...) or string
        :type     pixelpin: str or neopixel attribute
        :returns: pin as defined by neopixel attribute
    """
    def __map_Pin__(self, pixelpin):
        
        if isinstance(pixelpin, str):
            if(pixelpin == 'D18'):
                pixelpin = board.D18
            elif(pixelpin == 'D10'):
                pixelpin = board.D10
            elif(pixelpin == 'D12'):
                pixelpin = board.D12
            elif(pixelpin == 'D21'):
                pixelpin = board.D21
        
        return pixelpin
    
    """
        checks if pixelorder parameter was provided as instance or string (in case of command line configuration)
        
        :param    pixelorder: order defined either by neopixel attributes (neopixel.GRB, ...) or string
        :type     pixelorder: str or neopixel attribute
        :returns: order as defined by neopixel attribute
    """
    def __map_Order__(self, pixelorder):
        # check if pixelorder parameter was provided as instance or string (in case of command line configuration)
        if isinstance(pixelorder, str):
            if(pixelorder == 'GRB'):
                pixelorder = neopixel.GRB
            elif(pixelorder == 'RGB'):
                pixelorder = neopixel.RGB
            elif(pixelorder == 'GRBW'):
                pixelorder = neopixel.GRBW
            elif(pixelorder == 'RGBW'):
                pixelorder = neopixel.RGBW
        
        return pixelorder

    ########################################
    #            MEMBER METHODS            #
    ########################################
    """
    TODO
    """
    def setBrightness(self, brightness):
        self.__strip.brightness = brightness
        self.__strip.show()
        #print('brightness level: ' + str(brightness))

    """
        return the numer of led pixels defined for the current instance
        
        :returns: number of pixels
    """
    def getNumPixels(self):
        return self.__strip.n
    
    """
        turns all led pixels off
    """
    def reset(self):
        self.__strip.fill(self.__schema.W_BLACK)
    
    """
        set the color at the corresponding index
    """        
    def setPixel(self, index, color):
        self.__strip[index] = color
        
    """
        update the strip with the defined color values
    """        
    def show(self):
        self.__strip.show()
        