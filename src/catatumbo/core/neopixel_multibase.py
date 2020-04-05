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
import neopixel
import ipinfo

from catatumbo.core.util.utility import getExternalIPAddress
from ipinfo.exceptions import RequestQuotaExceededError
from catatumbo.core.neopixel_colors import NeoPixelColors
from catatumbo.core.neopixel_base import NeoPixelBase
from catatumbo.core.util.configurations import Configurations
from astral import Location
from datetime import datetime, timedelta
import os
from catatumbo.core.util.update_thread import fadeBrightness
from adafruit_blinka.microcontroller.bcm283x import pin


class NeoPixelMultiBase(NeoPixelBase):
    
    """
    STATIC CLASS ATTRIBUTES
    """
    
    """
    OBJECT ATTRIBUTES
    """
    # the set of led strip represented by NeoPixelBase classes
    __stripList     = None
    
    # brightness adaption location resolved by external IP resolution
    localCity       = None
    localCountry    = None
    localLat        = None
    localLon        = None
    localTimeZone   = None
    
    
    # time between updating the brightness of the strip, 1800 sec (30min)
    # may be also used for other purpose by derived classes, e.g. forecast frequency
    UpdateFrequency   = 1800

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
        
        :param    color_schema: the color schema class which defined the color values, e.g. NeoPixelColors or derived classes
        :type     color_schema: class
    """  
    def __init__(self, color_schema):
        
        # no initialization of super constructor to avoid led strip initialization
        
        # the set of led strip represented by NeoPixelBase classes
        self.__stripList = []
        
        config = Configurations()
        

        # loop all individual led strip configurations
        counter = 1
        while counter > -1:
            section = "Strip" + str(counter)
            
            # check whether strip enumerator has been defined
            if not config.hasSection(section):
                counter = -1
                # ensure we directly step out of loop
                continue
            
            pp = config.getConfigProperty(section, "PixelPin")
            pn = config.getConfigProperty(section, "PixelNum")
            po = config.getConfigProperty(section, "PixelOrder")

            strip = NeoPixelMultiBase.__Config__(pixelpin       = pp,
                                                 pixelnum       = pn,
                                                 pixelorder     = po,
                                                 color_schema   = color_schema)
            self.addStrip(strip)
            
            counter = counter + 1
        
        # set brightness level for all strips
        brightness = config.getBrightness()
        self.setBrightness(0.3 if brightness is None else brightness)
        
        # get current location for brightness adaption
        ipInfoKey = config.getIPInfoKey()
        if ipInfoKey is not None:            
            try:
                # determine location by external IP
                ipInfo = ipinfo.getHandler(ipInfoKey)
                ipDetails = ipInfo.getDetails(getExternalIPAddress())
                
                self.localCity      = ipDetails.city
                self.localCountry   = ipDetails.country
                self.localLat       = float(ipDetails.latitude)
                self.localLon       = float(ipDetails.longitude)
                self.localTimeZone  = ipDetails.timezone
            except (RequestQuotaExceededError, AttributeError):
                pass
    
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

    ########################################
    #        OVERRIDEN MEMBER METHODS      #
    ########################################
    """
        set the same brightness on all strip instances 
        
        :param    num: brightness of LED strips
        :type     num: float
    """
    def setBrightness(self, brightness):
        for i in range(self.countStrips()):
            strip = self.__getStrip(i)
            
            # cast
            strip.__class__ = NeoPixelBase
            
            strip.setBrightness(brightness)
        
    """
        returns the current brightness based on the actual value of the first strip
        
        :returns:    brightness
        :type        float
    """
    def getBrightness(self):
        return self.__getStrip(0).getBrightness()    

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
    #     BRIGHTNESS ADAPTION METHODS      #
    ######################################## 
    """
        adapts the strip brightness based on sunset/sunrise time for current location
    """
    def adaptBrightnessToLocalDaytime(self):
        
        config = Configurations()
        
        if config.getAutoBrightnessMax() is not None and \
            config.getAutoBrightnessMin() is not None and \
            self.localCity is not None and \
            self.localCountry is not None and \
            self.localLat is not None and \
            self.localLon is not None:
            # create Astral Location object for sunset/sunrise calculation
            # https://astral.readthedocs.io/en/stable/index.html
            astralLoc = Location((self.localCity,
                                  self.localCountry,
                                  self.localLat,
                                  self.localLon,
                                  # local timezone, see https://stackoverflow.com/questions/2720319/python-figure-out-local-timezone
                                  '/'.join(os.path.realpath('/etc/localtime').split('/')[-2:]),
                                  # well, anyone has a lucky number?
                                  # based on https://www.quora.com/What-is-the-average-elevation-of-Earth-above-the-ocean-including-land-area-below-sea-level-What-is-the-atmospheric-pressure-at-that-elevation
                                  #  "The average elevation of the land is 800m, covering 29% of the surface."
                                  # and https://ngdc.noaa.gov/mgg/global/etopo1_surface_histogram.html
                                  #  "average land height: 797m"
                                  500))
            
            # ensure we are using the same timezone for all to compare
            sunrise = astralLoc.sunrise()
            sunset  = astralLoc.sunset()
            now     = datetime.now(sunrise.tzinfo)
            
            print("now: {0}, sunrise: {1}, sunset: {2}".format(now, sunrise, sunset))

            # check if night time
            if now < sunrise or now > sunset:
                # sleep mode in dark hours
                self.setBrightness(config.getAutoBrightnessMin())
            # assure the fading process for brightness increase is started after sunrise within the boundaries of the update cycle
            elif now < sunrise + timedelta(seconds = self.UpdateFrequency):
                # see method description for initial parametrization
                fadeBrightness(self, config.getAutoBrightnessMin(), config.getAutoBrightnessMax(), 600, True)
            # assure the fading process for brightness decrease is started before sunset within the boundaries of the update cycle
            elif now > sunset - timedelta(seconds = self.UpdateFrequency):
                fadeBrightness(self, config.getAutoBrightnessMax(), config.getAutoBrightnessMin(), 600, True)
            else:
                # daytime mode
                self.setBrightness(config.getAutoBrightnessMax())   
    
    
    
    
    ########################################
    #            INNER CLASS               #
    ########################################
    class __Config__(object):
        
        def __init__(self, 
                     pixelpin       = pin.D18, 
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