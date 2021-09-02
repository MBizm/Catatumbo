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

from datetime import timedelta, datetime

from catatumbo.controller.forecast.forecast_colors import ForecastNeoPixelColors
from catatumbo.core.neopixel_multibase import NeoPixelMultiBase
from catatumbo.core.util.cmd_functions import cmd_options
from catatumbo.core.util.configurations import Configurations
from catatumbo.core.util.update_thread import queueUpdate
from catatumbo.core.util.utility import numberToBase, is_dst
from pyowm import OWM
from pyowm.exceptions.api_call_error import APIInvalidSSLCertificateError


class NeoPixelForecast(NeoPixelMultiBase):
    
    __version__ = 0.1
    __updated__ = '2019-12-29'

    """
    STATIC CLASS PROPERTIES
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
    
    # WEATHER CONDITION CODE
    # each weather condition based on rain, cloud coverage and temperature is mapped into discrete number of condition states
    #  that are indicated by different colors on the LED strip 
    # storm: digit 6, big endian
    CONDITION_STORM = 0x40
    # snow: digit 5, big endian
    CONDITION_SNOW = 0x20
    # temperature: digit 4-3, big endian
    CONDITION_LTMP = 0x08
    CONDITION_MTMP = 0x10
    CONDITION_HTMP = 0x18
    # rain/cloud: digit 2-0, big endian
    CONDITION_CLEAR = 0x01
    CONDITION_SLCLO = 0x02
    CONDITION_CLO   = 0x03
    CONDITION_SLRAI = 0x04
    CONDITION_RAI   = 0x05 
    
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
    
    # sampleboard storing currently displayed weather conditions
    # a dictionary consisting of {<id> : {"timestamp", "color", "CATAcode", "OWMcode", "temp", "cloud", "rain", "debug"}, ...}
    __sampleboard = None

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
        
        OWM weather API reference:
        https://github.com/csparpa/pyowm/blob/a5d8733412168516f869c84600812e0046c209f9/sphinx/usage-examples-v2/weather-api-usage-examples.md
        
        :param    color_mode: forecast period to be display, 
                    see MODE_TODAY, MODE_TOMORROW_DAYTIME, MODE_ALL, ...
        :type     color_mode: str
    """
    def fillStrips(self, color_mode = '2'):
        
        print("#### " + str(datetime.now()) + " Updating weather information")
        
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

        # create sampleboard dictionary for current weather condition
        sampleboard = {}
        # calculate offset for current days, forecast is provided in 3 hour blocks
        # TODO this requires adaption to timezone of defined location, current implementation considers local timezone!
        offset = int(forecast.when_starts('date').hour / 3)
        # mask for period selection, always representing full days including today, stored in big endian representation
        mask = self._getMask(color_mode, offset)
        # position marker representing current index in binary representation for comparison with mask
        pos = 1
        
        # prepare position marker to current time of the day
        pos = pos << offset

        # check whether winterMode was configured in properties
        if self.winterConf:
            # winterMode shall be activated based on winter-/summertime
            self.winterMode = not(is_dst(timezone=self.localTimeZone))
        
        
        # track current date & time of forecast
        cdate = forecast.when_starts('date')
        index = 0

        # iterate through weather forecast blocks
        for weather in forecast.get_forecast():

            # check whether current position marker matches with flagged timeslots
            if (mask & pos) > 0:
                sampleboard = self._fillSampleBoard(cdate, index, sampleboard, weather)

                # count the number of entries for index of dictionary - dictionary is not in chronological order
                index = index + 1
            
            # switch to next forecast block
            pos = pos << 1
            cdate = cdate + timedelta(hours=3)
        
        # prepare mask for day turn analysis by shifting by the offset
        mask = (mask >> offset) & 0xFFFFFFFFFF

        print(sampleboard)

        # display weather forecast on LED strip
        self.setPixelBySampleboard(sampleboard, mask)
        
        # store currently displayed weather condition for external status requests
        self.__sampleboard = sampleboard

    def _fillSampleBoard(self, cdate, index, sampleboard, weather):
        # get 3-byte or 4-byte color representation based on weather condition
        sampleboard.update({index: self.mapWeatherConditions(weather.get_temperature(unit='celsius')['temp'],
                                                             weather.get_clouds(),
                                                             0 if len(weather.get_rain()) == 0 else
                                                             list(weather.get_rain().values())[0],
                                                             cdate,
                                                             weather.get_weather_code(),
                                                             len(weather.get_snow()) > 0,
                                                             weather.get_wind()['speed'],
                                                             weather.get_humidity(),
                                                             weather.get_pressure()['press']
                                                             )})
        return sampleboard

    """
        returns the mask depending on the configuration 
    """
    def _getMask(self, color_mode, offset):
        mask = 0
        # will not make use of offset as the mask is static

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

        return mask

    """
        fills the strips according to a list of color values
        in case there are blocks in the sampleboard that shall be separated, a mask can be provided. 
        each entry in the sampleboard must be represented by a binary 1. 
        the block size is defined by the number of binary 1s that are in a chain without a binary 0 in between. 
        a new block can start with a binary 0 in between.
        the logic for the blocks resulted from the forecast functionality, in which only certain periods of the day were taken over into sampleboard.
        
        TODO the implementation of divider needs refactoring, simplifying coding and also considering cases where full day is considered in bit mask but still there should be a day divider being shown
        TODO implement blinking indication for storm and extreme weather situations
        
        :param    sampleboard: TODO UPDATE DESCRIPTION BASED ON CHANGED STRUCTURE list of color values defining the section, the section size depends on the number of pixels available in total
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
                # get color value from sampleboard - 1. step: get the right index, 2. step get color value
                self.setPixel(pixelindex, sampleboard[len(sampleboard) - 1]['color']) 
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
                    # get color value from sampleboard - 1. step: get the right index, 2. step get color value
                    self.setPixel(pixelindex, sampleboard[int(pixelindex / sectionsize)]['color'])
                    #print('[' + str(pixelindex) + '] ' + str(sampleboard[int(pixelindex / sectionsize)]))
                    
        
        # update color values if not done automatically
        self.show()
    
    """
        maps weather conditions (temperature, rain and cloud) to color values
        For each temperature scale (low, medium, high) values for rain (prioritized over cloud) and cloudiness will be indicated
        
        see \docs\forecast\ColorScale.png for more information

        :param    temp: temperature in Celsius
        :type     temp: float
        :param    cloud: percentage of cloud coverage
        :type     cloud: float
        :param    rain: amount of rain on mm/sqm
        :type     rain: float
        :param    timestamp: timestampf for the current weather forecast
        :type     timestamp: datetime object
        :param    OWMcode: OWM weather code - storm is not exposed via API and allows finer segregation of weather state
        :type     OWMcode: integer
        :param    snow: snow fall
        :type     snow: boolean
        :param    wind: wind speed m/s
        :type     wind: float
        :param    humidity: humidity in percentage
        :type     humidity: integer
        :param    pressure: athmosperic pressure in hPa
        :type     pressure: float
        :returns: a dictionary consisting of {"timestamp", "color", "CATAcode", "OWMcode", "temp", "cloud", "rain", "debug"}
    """
    def mapWeatherConditions(self,  
                                temp, 
                                cloud, 
                                rain,
                                timestamp,
                                OWMcode, 
                                snow,
                                wind,
                                humidity,
                                pressure):
               
        # color value
        c = None
        # code describing weather condition as hex value
        code = None
        debug = None
        
        # highest prio - any storm or extreme weather indication
        # storm is not directly exposed via OWM API
        # see OWM API: https://github.com/csparpa/pyowm/blob/a5d8733412168516f869c84600812e0046c209f9/pyowm/weatherapi25/weather.py
        # see OWM code description - official page missing description for >= 900
        # official description: https://openweathermap.org/weather-conditions
        # additional helpful documentation: https://godoc.org/github.com/briandowns/openweathermap
        #     202: thunderstorm with heavy rain, 212: heavy thunderstorm
        #     503: very heavy rain, 504: extreme rain
        #     711: smoke, 762: volcanic ash, 781: tornado
        #     900: tornado, 901: tropical storm, 902: hurricane, 906: hail
        #     958: gale, 959: severe gale, 960: storm, 961: violent storm, 962: hurricane
        if OWMcode == 202 or \
            OWMcode == 212 or \
            OWMcode == 503 or \
            OWMcode == 504 or \
            OWMcode == 711 or \
            OWMcode == 762 or \
            OWMcode == 781 or \
            OWMcode == 900 or \
            OWMcode == 901 or \
            OWMcode == 902 or \
            OWMcode == 906 or \
            OWMcode == 958 or \
            OWMcode == 959 or \
            OWMcode == 960 or \
            OWMcode == 961 or \
            OWMcode == 962:
            c = ForecastNeoPixelColors.W_STORM
            code = type(self).CONDITION_STORM
            debug = "storm"
        # second prio - snow fall or dangerous freezing rain indication
        # see https://godoc.org/github.com/briandowns/openweathermap
        #     511: freezing rain
        elif snow or \
            OWMcode == 511:
            c = ForecastNeoPixelColors.W_SNOW
            code = type(self).CONDITION_SNOW
            debug = "snow"
        # segregation by color range
        # low temp
        elif ( (not(self.winterMode) and temp <= 10) or (self.winterMode and temp <= 0) ) :
            # highest prio - rain fall indication
            # rainy
            if rain > 2.5:
                c = ForecastNeoPixelColors.W_LOWTMP_RAINY
                code = type(self).CONDITION_LTMP | type(self).CONDITION_RAI
                debug = "low temp [{0} C], rainy [{1}mm/qm]".format(temp, rain)
            # slightly rainy
            elif rain > 0.3:
                c = ForecastNeoPixelColors.W_LOWTMP_SLRAINY
                code = type(self).CONDITION_LTMP | type(self).CONDITION_SLRAI
                debug = "low temp [{0} C], slightly rainy [{1}mm/qm]".format(temp, rain)
            # no rain
            else:
                # second prio - cloud coverage
                # cloudy
                if cloud > (100 * 3/8):
                    c = ForecastNeoPixelColors.W_LOWTMP_CLOUDY
                    code = type(self).CONDITION_LTMP | type(self).CONDITION_CLO
                    debug = "low temp [{0} C], cloudy [{1}%]".format(temp, cloud)
                # slightly cloudy
                elif cloud > (100 * 1/8):
                    c = ForecastNeoPixelColors.W_LOWTMP_SLCLOUDY
                    code = type(self).CONDITION_LTMP | type(self).CONDITION_SLCLO
                    debug = "low temp [{0} C], slightly cloudy [{1}%]".format(temp, cloud)
                # no clouds
                else:
                    c = ForecastNeoPixelColors.W_LOWTMP
                    code = type(self).CONDITION_LTMP | type(self).CONDITION_CLEAR
                    debug = "low temp [{0} C]".format(temp)
        # mid temp
        elif (not(self.winterMode) and temp <= 25) or (self.winterMode and temp <= 10):
            # highest prio - rain fall indication
            # rainy
            if rain > 2.5:
                c = ForecastNeoPixelColors.W_MIDTMP_RAINY
                code = type(self).CONDITION_MTMP | type(self).CONDITION_RAI
                debug = "mid temp [{0} C], rainy [{1}mm/qm]".format(temp, rain)
            # slightly rainy
            elif rain > 0.3:
                c = ForecastNeoPixelColors.W_MIDTMP_SLRAINY
                code = type(self).CONDITION_MTMP | type(self).CONDITION_SLRAI
                debug = "mid temp [{0} C], slightly rainy [{1}mm/qm]".format(temp, rain)
            # no rain
            else:
                # second prio - cloud coverage
                # cloudy
                if cloud > (100 * 3/8):
                    c = ForecastNeoPixelColors.W_MIDTMP_CLOUDY
                    code = type(self).CONDITION_MTMP | type(self).CONDITION_CLO
                    debug = "mid temp [{0} C], cloudy [{1}%]".format(temp, cloud)
                # slightly cloudy
                elif cloud > (100 * 1/8):
                    c = ForecastNeoPixelColors.W_MIDTMP_SLCLOUDY
                    code = type(self).CONDITION_MTMP | type(self).CONDITION_SLCLO
                    debug = "mid temp [{0} C], slightly cloudy [{1}%]".format(temp, cloud)
                # no clouds
                else:
                    c = ForecastNeoPixelColors.W_MIDTMP
                    code = type(self).CONDITION_MTMP | type(self).CONDITION_CLEAR
                    debug = "mid temp [{0} C]".format(temp)
        # high temp
        elif (not(self.winterMode) and temp > 25) or (self.winterMode and temp > 10):
            # highest prio - rain fall indication
            # rainy
            if rain > 2.5:
                c = ForecastNeoPixelColors.W_HITMP_RAINY
                code = type(self).CONDITION_HTMP | type(self).CONDITION_RAI
                debug = "high temp [{0} C], rainy [{1}mm/qm]".format(temp, rain)
            # slightly rainy
            elif rain > 0.3:
                c = ForecastNeoPixelColors.W_HITMP_SLRAINY
                code = type(self).CONDITION_HTMP | type(self).CONDITION_SLRAI
                debug = "high temp [{0} C], rainy [{1}mm/qm]".format(temp, rain)
            # no rain
            else:
                # second prio - cloud coverage
                # cloudy
                if cloud > (100 * 3/8):
                    c = ForecastNeoPixelColors.W_HITMP_CLOUDY
                    code = type(self).CONDITION_HTMP | type(self).CONDITION_CLO
                    debug = "high temp [{0} C], cloudy [{1}%]".format(temp, cloud)
                # slightly cloudy
                elif cloud > (100 * 1/8):
                    c = ForecastNeoPixelColors.W_HITMP_SLCLOUDY
                    code = type(self).CONDITION_HTMP | type(self).CONDITION_SLCLO
                    debug = "high temp [{0} C], slightly cloudy [{1}%]".format(temp, cloud)
                # no clouds
                else:
                    c = ForecastNeoPixelColors.W_HITMP
                    code = type(self).CONDITION_HTMP | type(self).CONDITION_CLEAR
                    debug = "high temp [{0} C]".format(temp)
                    
        print("weather condition: " + debug)
        
        return {"timestamp" : timestamp.ctime(),
                "color"     : c,
                "CATAcode"  : code,
                "OWMcode"   : OWMcode,
                "temp"      : temp,
                "cloud"     : cloud,
                "rain"      : rain,
                "wind"      : wind,
                "humidity"  : humidity,
                "pressure"  : pressure,
                "debug"     : debug}

    ########################################
    #        GETTER/SETTER METHODS         #
    ######################################## 
    """
        returns currently displayed weather condition
        :returns:    dictionary consisting of {<id> : {"timestamp", "color", "CATAcode", "OWMcode", "temp", "cloud", "rain", "debug"}, ...}
    """
    def getCurrentWeatherCondition(self):
        return self.__sampleboard
    

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