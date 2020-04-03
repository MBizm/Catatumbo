'''
The configurations class is a singleton for retrieving and setting all configuration values.
It is used by the all controller/* as well as all core/* classes. Additionally, interceptor class uses it
to directly perform changes before instructing running adafruit process to reload.

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

@copyright:  2020 organization_name. All rights reserved.

@license:    Apache License 2.0

@deffield    created: March 2020
@deffield    updated: Updated
'''
import configparser

from configparser import NoOptionError, NoSectionError
from os import path

class Configurations(object):
    
    """
    STATIC CLASS ATTRIBUTES
    """
    DEFAULT_CONFIG      = 'test/adafruit/forecast/config/FORECASTCONFIG.properties'
    RUNTIME_CONFIG      = 'test/adafruit/forecast/config/RUNTIMECONFIG.properties'
    
    """
    OBJECT ATTRIBUTES
    """    
    __instance = None
    __config_parser = None
    
    """
        static class constructor for singleton
    """
    def __new__(cls, *args, **kwargs):
        if Configurations.__instance is None:
            Configurations.__instance = object.__new__(cls)
        return Configurations.__instance
    
    
    """
        constructor for singleton
        Catatumbo defines two config properties files: 
        - default configuration file which provides the template and comments for the configuration; for usage of services additional configuration is required (e.g. OWM API key)
        - runtime configuration file is created the first time the user changes a configuration and is based on the values defined in the default configuration file
        If runtime configuration file exists, this will be the leading one irrespective of the values defined in default configuration file
        TODO define proper default configuration file
        
        :param    config_file: the location of the properties file, relative to runtime execution path
        :type     config_file: str
    """    
    def __init__(self, config_file = None):
        # read config for led strips
        self.__config_parser = configparser.ConfigParser() 
        
        # check if custom configuration file defined
        if config_file is None:
            # check if runtime configuration file was already created
            if path.exists(type(self).RUNTIME_CONFIG):
                config_file = type(self).RUNTIME_CONFIG
            # fallback to default configuration
            else:
                config_file = type(self).DEFAULT_CONFIG
        
        self.__config_parser.read(config_file)    
        # configparser does not offer any flush method, so no destruction required?
        
    
    ########################################
    #      GETTER/SETTER Methods           #
    ########################################
    
    #
    #    service provider configuration
    #
    def getIPInfoKey(self):
        return self.getConfigProperty('Forecast-IPInfoData', 'APIKey')
    
    def getOWMKey(self):
        return self.getConfigProperty('Forecast-OWMData', 'APIKey')
    
    
    #
    #    technical LED strip configuration
    #
            
    def getBrightness(self):
        b = self.getConfigProperty("GeneralConfiguration", "Brightness")
        if b is not None:
            b = float(b)
        return b
    
    def setBrightness(self, brightness):
        if isinstance(brightness, float):
            self.setConfigProperty("GeneralConfiguration", "Brightness", str(brightness))
        self.writeConfiguration()
    
    # TODO unite brightness value with AutoBrightnessMAX value - if only brightness is defined, the strip will be always the same brightness, if min value is defined in addition that value represents the lower boundary for automatic brightness fading
    def getAutoBrightnessMax(self):
        bmax = self.getConfigProperty("GeneralConfiguration", "AutoBrightnessMAX")
        if bmax is not None:
            bmax = float(bmax)
        return bmax

    def setAutoBrightnessMax(self, brightness):
        if isinstance(brightness, float):
            self.setConfigProperty("GeneralConfiguration", "AutoBrightnessMAX", str(brightness))
        self.writeConfiguration()
    
    def getAutoBrightnessMin(self):
        bmin = self.getConfigProperty("GeneralConfiguration", "AutoBrightnessMIN")
        if bmin is not None:
            bmin = float(bmin)
        return bmin
    
    def setAutoBrightnessMin(self, brightness):
        if isinstance(brightness, float):
            self.setConfigProperty("GeneralConfiguration", "AutoBrightnessMIN", str(brightness))
        self.writeConfiguration()
    
    #
    #    location information
    #
    def getCityID(self):
        cid = self.getConfigProperty('Forecast-ApplicationData', 'CityID')
        if cid is not None:
            cid = int(cid)
        return cid
    
    def getCityName(self):
        return self.getConfigProperty('Forecast-ApplicationData', 'CityName')
    
    def getCityCountry(self):
        return self.getConfigProperty('Forecast-ApplicationData', 'Country')

    def getLongitude(self):
        lon = self.getConfigProperty('Forecast-ApplicationData', 'Longitude')
        if lon is not None:
            lon = float(lon)
        return lon
    
    def getLatitude(self):
        lat = self.getConfigProperty('Forecast-ApplicationData', 'Latitude')
        if lat is not None:
            lat = float(lat)
        return lat
    
    #
    #    additional configuration information
    #
    
    def isWinterMode(self):
        wc = bool(self.getConfigProperty('Forecast-ApplicationData', 'WinterMode'))
        if wc is None:            
            wc = False
        return wc
    
    ########################################
    #         UTILITY Methods              #
    ########################################
    
    """
        returns a property from specified config file (dynamic values)
        shall be only used in exceptional cases - use dedicated getter/setter classes instead
        
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
    
    """
        sets property for specified config file (dynamic values)
        shall be only used in exceptional cases - use dedicated getter/setter classes instead
        
        :param    section: section in config file
        :type     section: str
        :param    attribute: required attribute
        :type     attribute: str
        :param    value: property value
        :type     value: str
    """
    def setConfigProperty(self, section, attribute, value):
        try:
            self.__config_parser.set(section, attribute, value)
        except (NoOptionError, NoSectionError):
            print('Error in setting configuration')

    def hasSection(self, section):
        return self.__config_parser.has_section(section)
    
    """
        persists the current configuration
        if a runtime configuration file exists, it will override the values
        if configuration was loaded from default configuration file, a runtime configuration file will be created
    """    
    def writeConfiguration(self):
        with open(type(self).RUNTIME_CONFIG, 'w') as configfile:
            self.__config_parser.write(configfile, True)
