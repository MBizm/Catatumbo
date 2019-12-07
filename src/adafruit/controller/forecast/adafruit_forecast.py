'''
TODO The visualization script will present the weather forecast for the next days in 3 hour period for a defined location.
It requires a valid OpenWeatherMap key - free of charge for a limited amount of requests. See OWM website for more information: https://openweathermap.org/price.
Static configuration can be done by CONFIG.properties file. Otherwise values will be requested via command line.

TODO Resulting Tk Canvas will output 3 scales with temperature (red), cloud coverage (green) and rain forecast (blue) as well as an additional combined scale.

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
from adafruit.core.neopixel_base import NeoPixelBase
import board
import neopixel
from adafruit.core.forecast.forecast_colors import ForecastNeoPixelColors
from configparser import NoOptionError, NoSectionError
import configparser
from pyowm import OWM
import sys

class NeoPixelForecast(NeoPixelBase):

    """
    STATIC CLASS ATTRIBUTES
    """
    # config parser instance
    CONFIG = None
    
    
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
                 pixelorder     = neopixel.RGBW):
        
        super().__init__(pixelpin, 
                         pixelnum, 
                         pixelorder, 
                         ForecastNeoPixelColors)
        
        #init OWM registration
        self.__init_OWM()
    
    """
        TODO
    """
    def __init_OWM(self): 
           
        #get your personal key
        apiKey = self.__getConfigProperty('ConnectionData', 'APIKey');
        if(apiKey is None):
            apiKey = input('Enter your API Key: ')
        
        #get location for request
        #TODO get location via IP: https://ipinfo.io/developers
        cityID = self.__getConfigProperty('ApplicationData', 'CityID')
        city = self.__getConfigProperty('ApplicationData', 'CityName')
        country = self.__getConfigProperty('ApplicationData', 'Country')
        if(cityID is None):
            if(country is None):
                country = input('Enter your country: ')
            if(city is None):
                city = input('Enter your city: ')
                
        #initiate OpenWeatherMap object
        owm = OWM(apiKey);
        #get city id for defined location
        if(cityID is None):
            reg = owm.city_id_registry()
            try:
                locs = reg.ids_for(city, country, matching='exact')
                #always select first from list
                loc = locs.pop(0)
                cityID = int(loc[0])
            except (ValueError, IndexError):
                print('Defined city could not be found!')
                sys.exit();
                
    """
        reads defined values from property file - CONFIG.properties at same location
        property file consists of two sections:
            - [ConnectionData]:APIKeyDomain, APIKeyName(optional), APIKey
            - [ApplicationData]:CityID, CityName, Country
        
        :param    p_section: property file section
        :type     p_section: str
        :param    p_attribute: property file key of defined section
        :type     p_attribute: str
        :returns: value 
    """
    def __getConfigProperty(self, p_section, p_attribute):
        if type(self).CONFIG == None:
            type(self).CONFIG = configparser.RawConfigParser()
            type(self).CONFIG.read('adafruit/core/forecast/CONFIG.properties')
            
        try:
            ret = type(self).CONFIG.get(p_section, p_attribute)
        except (NoOptionError, NoSectionError):
            return None;
        return ret; 
    
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
                        storm = False, 
                        snow = False, 
                        temp, 
                        cloud, 
                        rain):
        
        c = None
        
        # highest prio - any storm indication
        if storm:
            c = ForecastNeoPixelColors.W_STORM
        # second prio - snow fall indication
        elif snow:
            c = ForecastNeoPixelColors.W_SNOW
        # segregation by color range
        # TODO differentiation based on summer/winter period??
        # low temp
        elif temp <= 10:
            # highest prio - rain fall indication
            # rainy
            if rain > 2.5:
                c = ForecastNeoPixelColors.W_LOWTMP_RAINY
            # slightly rainy
            elif rain > 0.3:
                c = ForecastNeoPixelColors.W_LOWTMP_SLRAINY
            # no rain
            else:
                # second prio - cloud coverage
                # cloudy
                if cloud > (100 * 3/8):
                    c = ForecastNeoPixelColors.W_LOWTMP_CLOUDY
                # slightly cloudy
                elif cloud > (100 * 1/8):
                    c = ForecastNeoPixelColors.W_LOWTMP_SLCLOUDY
                # no clouds
                else:
                    c = ForecastNeoPixelColors.W_LOWTMP
        # mid temp
        elif temp <= 25:
            # highest prio - rain fall indication
            # rainy
            if rain > 2.5:
                c = ForecastNeoPixelColors.W_MIDTMP_RAINY
            # slightly rainy
            elif rain > 0.3:
                c = ForecastNeoPixelColors.W_MIDTMP_SLRAINY
            # no rain
            else:
                # second prio - cloud coverage
                # cloudy
                if cloud > (100 * 3/8):
                    c = ForecastNeoPixelColors.W_MIDTMP_CLOUDY
                # slightly cloudy
                elif cloud > (100 * 1/8):
                    c = ForecastNeoPixelColors.W_MIDTMP_SLCLOUDY
                # no clouds
                else:
                    c = ForecastNeoPixelColors.W_MIDTMP
        # high temp
        elif temp > 25:
            # highest prio - rain fall indication
            # rainy
            if rain > 2.5:
                c = ForecastNeoPixelColors.W_HITMP_RAINY
            # slightly rainy
            elif rain > 0.3:
                c = ForecastNeoPixelColors.W_HITMP_SLRAINY
            # no rain
            else:
                # second prio - cloud coverage
                # cloudy
                if cloud > (100 * 3/8):
                    c = ForecastNeoPixelColors.W_HITMP_CLOUDY
                # slightly cloudy
                elif cloud > (100 * 1/8):
                    c = ForecastNeoPixelColors.W_HITMP_SLCLOUDY
                # no clouds
                else:
                    c = ForecastNeoPixelColors.W_HITMP
        
        return c