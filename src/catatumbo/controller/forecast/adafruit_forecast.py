'''
The Forecast module will represent the weather forecast in a range between today and +5 days (see mode attribute on command line for parametrization)
as color values on the attached led strips. Status will be constantly updated every 30mins. See the color values for the weather conditions in
Catatumbo/src/catatumbo/core/forecast/forecast_colors.py.

It requires a valid OpenWeatherMap key - free of charge for a limited amount of requests. See OWM website for more information: https://openweathermap.org/price.
Static configuration can be done by FORECASTCONFIG.properties file. Otherwise values will be requested via command line.

Let yourself be dragged into the fascination of Catatumbo - Happy weather watching!
 

Copyright MBizm [https://github.com/MBizm]

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

@author:     MBizm

@copyright:  2019 organization_name. All rights reserved.

@license:    Apache License 2.0

@deffield    created: December 2019
@deffield    updated: Updated
'''

from pyowm import OWM
from catatumbo.core.neopixel_multibase import NeoPixelMultiBase
from catatumbo.core.util.cmd_functions import cmd_options
from pyowm.exceptions.api_call_error import APIInvalidSSLCertificateError
from catatumbo.core.util.utility import numberToBase, is_dst
from catatumbo.controller.forecast.forecast_colors import ForecastNeoPixelColors
from catatumbo.core.util.configurations import Configurations
from catatumbo.core.util.update_thread import queueUpdate

class NeoPixelForecast(NeoPixelMultiBase):
    
    __version__ = 0.1
    __updated__ = '2019-12-29'

    """
    STATIC CLASS ATTRIBUTES
    """
    MODE_TODAY_DAYTIME      = '1'
    MODE_TODAY_ALL          = '2'
    MODE_TOMORROW_DAYTIME   = '3'
    MODE_TOMORROW_ALL       = '4'
    MODE_3DAYS_DAYTIME      = '5'
    MODE_3DAYS_ALL          = '6'
    # TODO better to have 5d forecast aggregated per day?
    MODE_5DAYS_DAYTIME      = '7'
    MODE_5DAYS_ALL          = '8'
    
    """
    OBJECT ATTRIBUTES
    """
    owm = None
    # geo coordinates for desired location
    cityID = 0
    cityName = None
    cityCountry = None
    cityLon = 0.0
    cityLat = 0.0
    # winter mode will adapt the adapt the temperature scale, e.g. >10C is considered high temperature in winter
    # winterConf will enable winterMode determination based on properties file definition
    winterConf = False
    # winterMode is the mode dependent on the time of the year
    winterMode = False

    """
        TODO adapt config to Forecast requirement
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
        
        super().__init__(color_schema)
        
        config = Configurations()
        
        #get non OWM specific properties          
        self.winterConf = config.isWinterMode()
        
        #init OWM registration
        self.__init_OWM(config)

    ########################################
    #            UTILITY METHODS           #
    ######################################## 
    
    """
        reads forecast config values from the defined property file
        this will instantiate the OpenWeatherMap instance and read country, city, ... data
        
        property file consists of two sections:
            - [OWMData]:APIKeyDomain, APIKeyName(optional), APIKey
            - [ApplicationData]:CityID, CityName, Country
    """
    def __init_OWM(self, config):            
        #get your personal key
        apiKey = config.getOWMKey();
        if apiKey is None:
            raise RuntimeError('You need to define an Open Weather Map API key to run the forecast module!')
        
        #get location for request
        #TODO get location via IP: https://ipinfo.io/developers
        self.cityLon        = config.getLongitude()
        self.cityLat        = config.getLatitude()
        self.cityID         = config.getCityID()
        self.cityName       = config.getCityName()
        self.cityCountry    = config.getCityCountry()
               
        #initiate OpenWeatherMap object
        self.owm = OWM(apiKey);
        reg = self.owm.city_id_registry()
                
        #check whether we can get get lon/lat and id based on cityName and cityCountry
        if self.cityName is not None and self.cityCountry is not None:
            if self.cityLat is None or self.cityLon is None:
                try:
                    locs = reg.locations_for(self.cityName, self.cityCountry, matching='exact')
                    #always select first from list
                    loc = locs.pop(0)
                    self.cityID = int(loc[0])
                    self.cityLon = float(loc[2])
                    self.cityLon = float(loc[3])
                except (ValueError, IndexError):
                    pass
        else:
            # fallback to location determined by external IP of Raspberry
            self.cityName       = self.localCity
            self.cityCountry    = self.localCountry
            self.cityLat        = self.localLat
            self.cityLon        = self.localLon 
        
        # final try to get city id for defined location
        if self.cityID is None:
            try:
                locs = reg.ids_for(self.cityName, self.cityCountry, matching='exact')
                #always select first from list
                loc = locs.pop(0)
                self.cityID = int(loc[0])
            except (ValueError, IndexError):
                pass
        
        if self.cityID is None and self.cityLat == self.cityLon == None:          
            raise RuntimeError('Defined city could not be found: {0}'.format(self.cityName))
    
    
    ########################################
    #         COLOR SCALE METHODS          #
    ######################################## 
    """
        fills weather forecast data based on defined mode
        
        :param    color_mode: forecast period to be display, 
                    see MODE_TODAY, MODE_TOMORROW_DAYTIME, MODE_ALL, ...
        :type     color_mode: str
    """
    def fillStrips(self, color_mode = '2'):
        #request forecast
        #https://pyowm.readthedocs.io/en/latest/usage-examples-v2/weather-api-usage-examples.html#getting-weather-forecasts
        try:
            if self.cityLat is not None and self.cityLon is not None:
                forecast = self.owm.three_hours_forecast_at_coords(float(self.cityLat),
                                                                   float(self.cityLon))
            else:
                forecast = self.owm.three_hours_forecast_at_id(self.cityID)
        except (APIInvalidSSLCertificateError):
            # network temporarily not available
            print('Network error during OWM call')
            # stop processing here
            return

        # create sampleboard for relevant color slots
        sampleboard = ()
        # calculate offset for current days, forecast is provided in 3 hour blocks
        # TODO this requires adaption to timezone of defined location, current implementation considers local timezone!
        offset = int(forecast.when_starts('date').hour / 3)
        # mask for period selection, always representing full days including today, stored in big endian representation
        mask = 0 
        # position marker representing current index in binary representation for comparison with mask
        pos = 1

        if color_mode == type(self).MODE_TODAY_DAYTIME:
            # masks 6am to 9pm slot the next day
            mask = 0x7C
        elif color_mode == type(self).MODE_TODAY_ALL:
            # masks all forecast blocks from 0am to 11:59pm the next day
            mask = 0xFF
        elif color_mode == type(self).MODE_TOMORROW_DAYTIME:
            # masks 6am to 9pm slot the next day
            mask = 0x7C00
        elif color_mode == type(self).MODE_TOMORROW_ALL:
            # masks all forecast blocks from 0am to 11:59pm the next day
            mask = 0xFF00
        elif color_mode == type(self).MODE_3DAYS_DAYTIME:
            # masks 6am to 9pm slot all next 3 days including today
            mask = 0x7C7C7C
        elif color_mode == type(self).MODE_3DAYS_ALL:
            # masks all forecast blocks from 0am to 11:59pm the next 3 day including today
            mask = 0xFFFFFF
        elif color_mode == type(self).MODE_5DAYS_DAYTIME:
            # masks 6am to 9pm slot all next 5 days including today
            mask = 0x7C7C7C7C7C
        elif color_mode == type(self).MODE_5DAYS_ALL:
            # just everything...
            mask = 0xFFFFFFFFFF
        
        # prepare position marker to current time of the day
        pos = pos << offset
        
        # check whether winterMode was configured in properties
        if self.winterConf:
            # winterMode shall be activated based on winter-/summertime
            self.winterMode = not(is_dst(timezone=self.localTimeZone))
        
        
        # iterate through weather forecast blocks
        # forecast is provided for 5 days in 8 blocks per day
        # TODO check offset and max counter values
        for weather in forecast.get_forecast():

            # check whether current position marker matches with flagged timeslots
            if (mask & pos) > 0:
                # get 3-byte or 4-byte color representation based on weather condition
                # TODO check for storm attribute
                sampleboard = sampleboard + (self.mapWeatherToRGB(weather.get_temperature(unit='celsius')['temp'],
                                                                   weather.get_clouds(),
                                                                   0 if len(weather.get_rain()) == 0 else list(weather.get_rain().values())[0],
                                                                   False,
                                                                   len(weather.get_snow()) > 0), )
                #print("Added entry at: {0} - {1}".format(str(numberToBase((mask & pos), 2)), sampleboard))
            
            # switch to next forecast block
            pos = pos << 1
        
        # prepare mask for day turn analysis by shifting by the offset
        mask = (mask >> offset) & 0xFFFFFFFFFF
        
        # print weather forecast
        self.setPixelBySampleboard(sampleboard, mask)
        
    """
        fills the strips according to a list of color values
        in case there are blocks in the sampleboard that shall be separated, a mask can be provided. 
        each entry in the sampleboard must be represented by a binary 1. 
        the block size is defined by the number of binary 1s that are in a chain without a binary 0 in between. 
        a new block can start with a binary 0 in between.
        the logic for the blocks resulted from the forecast functionality, in which only certain periods of the day were taken over into sampleboard.
        
        TODO the implementation of divider needs refactoring, simplifying coding and also considering cases where full day is considered in bit mask but still there should be a day divider being shown
        
        :param    sampleboard: list of color values defining the section, the section size depends on the number of pixels available in total
        :type     sampleboard: list
        :param    mask: a binary list, indicating each sampleboard entry by a binary 1 and each block being separated by a binary 0 in between.
        :type     mask: long int
    """       
    def setPixelBySampleboard(self, sampleboard, mask = -1):
        
        # do nothing if sampleboard is empty
        if len(sampleboard) == 0:
            return
        
        # check if a color block mask was provided
        # set with all individual block lengths, the total number of dividers and divider length in relation to strip length
        block_set = ()
        divider_size = 0
        # a color block may indicate block in the sampleboard belonging together
        # these may be separated by a divider (black leds)
        if mask > 0:
            # convert mask into a set of bit values
            mask_set = numberToBase(mask, 2)
            
            # boolean indicator of blocks
            new_block = False
            old_block = False
            # counts the length of the individual blocks
            block_counter = 0
            
            # check each bit in mask for block belonging together and count all blocks of '1's assembled together
            # a '0' in between indicates that a divider is required
            for i in reversed(range(len(mask_set))):
                if mask_set[i] == 1:
                    new_block = True
                elif mask_set[i] == 0:
                    new_block = False
                    
                # check if we found a new block
                if new_block == True and old_block == False:
                    # store the previous block size
                    # we are only interested in the previous block if there is another block to follow
                    if block_counter > 0:
                        block_set = block_set + (block_counter, )
                    # start counting the next block
                    block_counter = 1  
                # check if we are within a block
                elif new_block == old_block == True:
                    block_counter = block_counter + 1
                    
                # keep status of this cycle for analysis in next cycle
                old_block = new_block
            
            # check if the strip offers enough space for showing dividers
            # 1% of the strip length shall be reserved for dividers
            divider_size = int(self.getNumPixels() * 0.01)
            # at least 1 pixel per divider is required
            if len(block_set) == 0 or divider_size == 0:
                # reset block set if strip is too short
                block_set = ()
                divider_size = 0
                
            #print("mask: " + str(mask_set) + " block_set: " + str(block_set) + " divider size: " + str(divider_size))

        # divide the sections across all strips by the number of color entries in the sampleboard
        sectionsize = int(self.getNumPixels() / len(sampleboard))

        # preset pixel colors
        for pixelindex in range(self.getNumPixels()-1):
            # fill up remaining pixels
            if(int(pixelindex / sectionsize) >= len(sampleboard)):
                self.setPixel(pixelindex, sampleboard[len(sampleboard) - 1]) 
            # preset pixel colors according to color space set  
            else:
                # sums up the length of the individual blocks
                block_counter = 0
                # counts the number of the dividers for the given pixelindex
                divider_required = False
                
                # iterate the set of individual block sets
                for i in range(len(block_set)):
                    # count how the number of sampleboard indexes covered so far
                    block_counter = block_counter + block_set[i]
                    
                    # check if current sampleboard index is matching given block end
                    if int(pixelindex / sectionsize) == block_counter - 1:
                        # set marker
                        divider_required = True
                        break
                
                # let us steal the last pixels of the current block
                # TODO have a more accurate calculation by shrinking block size overall instead of stealing from the current block only
                if divider_required == True and (int(pixelindex / sectionsize) + 1) * sectionsize - divider_size <= pixelindex:
                    self.setPixel(pixelindex, ForecastNeoPixelColors.W_BLACK)
                    #print('[' + str(pixelindex) + '] <DIVIDER>')
                else:
                    self.setPixel(pixelindex, sampleboard[int(pixelindex / sectionsize)])
                    #print('[' + str(pixelindex) + '] ' + str(sampleboard[int(pixelindex / sectionsize)]))
                    
        
        # update color values if not done automatically
        self.show()
    
    """
        adapting the scales for the different vectors based on DWD terminology
        
        see \docs\forecast\ColorScale.png for more information

        :param    storm: storm indication
        :type     storm: boolean
        :param    snow: snow fall
        :type     snow: boolean
        :param    temp: temperature
        :type     temp: float
        :param    cloud: percentage of cloud coverage
        :type     cloud: float
        :param    rain: amount of rain on l/sqm
        :type     rain: float
        :returns: mapped color for weather condition
    """
    def mapWeatherToRGB(self,  
                        temp, 
                        cloud, 
                        rain,
                        storm = False, 
                        snow = False):
        
        c = None
        debug = None
        
        # highest prio - any storm indication
        if storm:
            c = ForecastNeoPixelColors.W_STORM
            debug = "storm"
        # second prio - snow fall indication
        elif snow:
            c = ForecastNeoPixelColors.W_SNOW
            debug = "snow"
        # segregation by color range
        # TODO differentiation based on summer/winter period??
        # low temp
        elif ( (not(self.winterMode) and temp <= 10) or (self.winterMode and temp <= 0) ) :
            # highest prio - rain fall indication
            # rainy
            if rain > 2.5:
                c = ForecastNeoPixelColors.W_LOWTMP_RAINY
                debug = "low temp, rainy"
            # slightly rainy
            elif rain > 0.3:
                c = ForecastNeoPixelColors.W_LOWTMP_SLRAINY
                debug = "low temp, slightly rainy"
            # no rain
            else:
                # second prio - cloud coverage
                # cloudy
                if cloud > (100 * 3/8):
                    c = ForecastNeoPixelColors.W_LOWTMP_CLOUDY
                    debug = "low temp, cloudy"
                # slightly cloudy
                elif cloud > (100 * 1/8):
                    c = ForecastNeoPixelColors.W_LOWTMP_SLCLOUDY
                    debug = "low temp, slightly cloudy"
                # no clouds
                else:
                    c = ForecastNeoPixelColors.W_LOWTMP
                    debug = "low temp"
        # mid temp
        elif (not(self.winterMode) and temp <= 25) or (self.winterMode and temp <= 10):
            # highest prio - rain fall indication
            # rainy
            if rain > 2.5:
                c = ForecastNeoPixelColors.W_MIDTMP_RAINY
                debug = "mid temp, rainy"
            # slightly rainy
            elif rain > 0.3:
                c = ForecastNeoPixelColors.W_MIDTMP_SLRAINY
                debug = "mid temp, slightly rainy"
            # no rain
            else:
                # second prio - cloud coverage
                # cloudy
                if cloud > (100 * 3/8):
                    c = ForecastNeoPixelColors.W_MIDTMP_CLOUDY
                    debug = "mid temp, cloudy"
                # slightly cloudy
                elif cloud > (100 * 1/8):
                    c = ForecastNeoPixelColors.W_MIDTMP_SLCLOUDY
                    debug = "mid temp, slightly cloudy"
                # no clouds
                else:
                    c = ForecastNeoPixelColors.W_MIDTMP
                    debug = "mid temp"
        # high temp
        elif (not(self.winterMode) and temp > 25) or (self.winterMode and temp > 10):
            # highest prio - rain fall indication
            # rainy
            if rain > 2.5:
                c = ForecastNeoPixelColors.W_HITMP_RAINY
                debug = "high temp, rainy"
            # slightly rainy
            elif rain > 0.3:
                c = ForecastNeoPixelColors.W_HITMP_SLRAINY
                debug = "high temp, slightly rainy"
            # no rain
            else:
                # second prio - cloud coverage
                # cloudy
                if cloud > (100 * 3/8):
                    c = ForecastNeoPixelColors.W_HITMP_CLOUDY
                    debug = "high temp, cloudy"
                # slightly cloudy
                elif cloud > (100 * 1/8):
                    c = ForecastNeoPixelColors.W_HITMP_SLCLOUDY
                    debug = "high temp, slightly cloudy"
                # no clouds
                else:
                    c = ForecastNeoPixelColors.W_HITMP
                    debug = "high temp"
                    
        print("weather condition: " + debug)
        
        return c
    

########################################
#                MAIN                  #
########################################

if __name__ == '__main__':
    # configuration for multi base example is available via config file
    # only color mode can be selected via cmd line (how about brightness)
    # TODO adapt mode parameter proposals in help
    opts = cmd_options(NeoPixelForecast.__version__, 
                       NeoPixelForecast.__updated__,
                       par = "extended")
    
    np = NeoPixelForecast(color_schema  = ForecastNeoPixelColors)
    
    # start repetitive update
    queueUpdate(np, opts.mode)
    
    if opts.bright is not None:
        np.setBrightness(opts.bright)