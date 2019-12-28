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
from adafruit.core.neopixel_colors import NeoPixelColors
import configparser
from configparser import NoOptionError, NoSectionError

class NeoPixelMultiBase(NeoPixelBase):
    
    """
    STATIC CLASS ATTRIBUTES
    """
    
    """
    OBJECT ATTRIBUTES
    """
    # the set of led strip represented by NeoPixelBase classes
    __stripList = None
    __config_parser = None

    """
        constructor for multi strip base class
        multiple strips connected to different GPIO pins will be treated as a chain of strips attached to each other.
        if first strip is filled up, second one will be filled with the remaining buffer content and so on.
        configuration for the strips is taken from a property file that needs to be defined.
        format of the property file is expected to be:
        
                [GeneralConfiguration]
                Brightness=0.3
                
                [Strip1]
                PixelPin1=D18
                PixelNum1=60
                PixelOrder1=GRBW
                
                [Strip2]
                PixelPin2=D21
                PixelNum2=301
                PixelOrder2=GRB
                
                [Strip3]
                PixelPin3=D13
                PixelNum3=145
                PixelOrder3=GRB
        
        :param    config_file: the location of the properties file, relative to runtime execution path
        :type     config_file: str
        :param    color_schema: the color schema class which defined the color values, e.g. NeoPixelColors or derived classes
        :type     color_schema: class
    """  
    def __init__(self, config_file, color_schema):
        
        # no initialization of super constructor to avoid led strip initialization
        
        # the set of led strip represented by NeoPixelBase classes
        self.__stripList = []
        
        # read config for led strips
        self.__config_parser = configparser.RawConfigParser()
        self.__config_parser.read(config_file)
        # configparser does not offer any flush method, so no destruction required?

        # loop all individual led strip configurations
        counter = 1
        while counter > -1:
            try:
                section = "Strip" + str(counter)

                strip = NeoPixelMultiBase.__Config__(pixelpin       = self.__config_parser.get(section, "PixelPin" + str(counter)),
                                                     pixelnum       = self.__config_parser.get(section, "PixelNum" + str(counter)),
                                                     pixelorder     = self.__config_parser.get(section, "PixelOrder" + str(counter)),
                                                     color_schema   = color_schema)
                self.addStrip(strip)
                
            except (NoOptionError, NoSectionError):
                counter = -1
                # ensure we directly step out of loop
                continue
            
            counter = counter + 1
        
        # set brightness level for all strips
        try:
            self.setBrightness(self.__config_parser.get("GeneralConfiguration", "Brightness"))
        except (NoOptionError, NoSectionError):
            self.setBrightness(0.3)
            
    
    ########################################
    #            UTILITY METHODS           #
    ########################################   
    """
        adds a new led strip to the configuration
        a reset of the color values and brightness is required by the calling application to include the new strip
        
        :param    config: config of the new led strip
        :type     config: __Config__
    """   
    def addStrip(self, config = None):
        if config is not None:
            self.__stripList.append(NeoPixelBase(config.getPixelPin(), 
                                                 config.getPixelNum(), 
                                                 config.getPixelOrder(), 
                                                 config.getColorSchema()))

    """
        returns the NeoPixelBase representation of one particular led strip for a given index
        
        :param    num: index of led strip
        :type     num: int
        :returns: NeoPixelBase instance
    """   
    def __getStrip(self, num):
        return self.__stripList[num]

    """
        returns the number of led strips
        
        :returns: number of led strips
    """ 
    def countStrips(self):
        return len(self.__stripList)
    
    """
        returns a property from specified config file
        
        :param    section: section in config file
        :type     section: str
        :param    attribute: required attribute
        :type     attribute: str
        :returns: property value
    """
    def getConfigProperty(self, section, attribute):
        try:
            ret = self.__config_parser.get(section, attribute)
        except (NoOptionError, NoSectionError):
            return None;
        return ret;      

    ########################################
    #        OVERRIDEN MEMBER METHODS      #
    ########################################
    def setBrightness(self, brightness):
        for i in range(self.countStrips()):
            strip = self.__getStrip(i)
            
            # cast
            strip.__class__ = NeoPixelBase
            
            strip.setBrightness(float(brightness))
            

    """
        return the number of led pixels defined for the current instance
        
        :returns: number of pixels
    """
    def getNumPixels(self):
        count = 0
        
        for i in range(self.countStrips()):
            strip = self.__getStrip(i)
            
            # cast
            strip.__class__ = NeoPixelBase
            
            count += strip.getNumPixels()
        
        return count
    
    """
        turns all led pixels off
    """
    def reset(self):
        for i in range(self.countStrips()):
            strip = self.__getStrip(i)
            
            # cast
            strip.__class__ = NeoPixelBase
            
            strip.fill(strip.__schema.W_BLACK)
    
    """
        set the color at the corresponding index
        #### TODO abstraction required - not all may use the same color schema ####
    """        
    def setPixel(self, index, color):
        count = 0
        
        for i in range(self.countStrips()):
            strip = self.__getStrip(i)
            
            # cast
            strip.__class__ = NeoPixelBase
            
            # set color value to matching pixel
            if((count + strip.getNumPixels()) > index):
                strip.setPixel(index = (index - count),
                               color = color)
                # corresponding pixel found
                return
            
            count += strip.getNumPixels()       
        
    """
        update the strip with the defined color values
    """        
    def show(self):
        for i in range(self.countStrips()):
            strip = self.__getStrip(i)
            
            # cast
            strip.__class__ = NeoPixelBase
            
            strip.show()
    
    
    
    
    
    
    
    
    ########################################
    #            INNER CLASS               #
    ########################################
    class __Config__(object):
        
        def __init__(self, 
                     pixelpin       = board.D18, 
                     pixelnum       = 0, 
                     pixelorder     = neopixel.RGBW,
                     color_schema   = NeoPixelColors):
            
            self.__pixelpin     = NeoPixelBase.__map_Pin__(self, pixelpin = pixelpin)
            self.__pixelnum     = pixelnum
            self.__pixelorder   = NeoPixelBase.__map_Order__(self, pixelorder = pixelorder)
            self.__colorschema  = color_schema
            
        ########################################
        #            GETTER METHODS            #
        ########################################
    
        def getPixelPin(self):
            return self.__pixelpin
        
        def getPixelNum(self):
            return self.__pixelnum
        
        def getPixelOrder(self):
            return self.__pixelorder
        
        def getColorSchema(self):
            return self.__colorschema