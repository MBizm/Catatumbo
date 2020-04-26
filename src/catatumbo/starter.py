'''
This singleton module is the central starter for the led strip to have it display a variety of modes. 
It will start the interceptor class which exposes an external port for interacting with the strip
at runtime and interacts with starter module to change modus at runtime.

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

@deffield    created: April 2020
@deffield    updated: Updated
'''
from catatumbo.core.util.cmd_functions import cmd_options
from catatumbo.controller.forecast.adafruit_forecast import NeoPixelForecast
from catatumbo.controller.forecast.forecast_colors import ForecastNeoPixelColors
from catatumbo.core.util.update_thread import queueUpdate
import catatumbo.core.interceptor.server.configuration_service

import threading
from catatumbo.core.util.configurations import Configurations
from catatumbo.core.neopixel_colors import NeoPixelColors
import neopixel

class CatatumboStart():
    
    __version__ = 0.1
    __updated__ = '2020-01-03'
    
    """
    STATIC CLASS ATTRIBUTES
    """
    MODE_BASICCOLOR         = 0
    MODE_WEATHERFORECAST    = 10
    MODE_SHAREPRICE         = 20
    MODE_ALARM              = 99
    
    """
    OBJECT ATTRIBUTES
    """    
    __instance = None
    __options = None
    
    __activeMode = 0
    # controller object instances for different modes
    __basiccolorInstance = None
    __forecastInstance = None
    __sharepriceInstance = None
    __alarmInstance = None
    

    """
        static class constructor for singleton
    """
    def __new__(cls, *args, **kwargs):
        if CatatumboStart.__instance is None:
            CatatumboStart.__instance = object.__new__(cls)
        return CatatumboStart.__instance

    """
        constructor for singleton
        TODO define default constructor parameters, parametrization for modes
        
        :param    opts: command line options of starter module
        :type     opts: class
    """    
    def __init__(self, opts = None):
        if opts is not None:
            self.__options = opts
        
    
    ########################################
    #         WEATHER INSTANCIATION        #
    ########################################
    """
        TODO
    """
    def __startBasicColorMode(self):
        pass
    
    """
        TODO
    """    
    def __startWeatherForecastMode(self):
        # create __forecastInstance instance
        if self.__forecastInstance is None:
            self.__forecastInstance = NeoPixelForecast(color_schema  = ForecastNeoPixelColors)
        
        
        # start regular update of weather data and brightness adaption if configured
        queueUpdate(self.__forecastInstance, self.__options.mode)
            
    """
        TODO
    """
    def __startSharePriceMode(self):
        pass
    
    """
        TODO
    """
    def __startAlarmMode(self):
        pass
    
    ########################################
    #           MODE CONFIGURATION         #
    ########################################
    """
        set and activate a defined mode by running through the setup procedure
        
        :param    mode: mode to be activated; see MODE_BASICCOLOR, MODE_WEATHERFORECAST, MODE_SHAREPRICE, MODE_ALARM
        :type     mode: int
    """
    def setActiveMode(self, mode = 0):
        # ensure we properly clean up currently active mode
        self.__deactiveModeInstance()
        
        if mode == type(self).MODE_WEATHERFORECAST:
            self.__startWeatherForecastMode()
            self.__activeMode = type(self).MODE_WEATHERFORECAST
        elif mode == type(self).MODE_SHAREPRICE:
            self.__startSharePriceMode()
            self.__activeMode = type(self).MODE_SHAREPRICE
        elif mode == type(self).MODE_ALARM:
            self.__startAlarmMode()
            self.__activeMode = type(self).MODE_ALARM
        # if basic color is selected or an invalid value, switch back to basic colors
        else:
            self.__startBasicColorMode()
            self.__activeMode = type(self).MODE_BASICCOLOR
    
    """
        returns the activated mode
        
        :returns    see MODE_BASICCOLOR, MODE_WEATHERFORECAST, MODE_SHAREPRICE, MODE_ALARM
        :type       int
    """
    def getActiveMode(self):
        return self.__activeMode
    
    """
        returns the current object instance based on the selected mode
    """       
    def getActivedInstance(self):
        if self.__activeMode == type(self).MODE_WEATHERFORECAST:
            return self.__forecastInstance
        elif self.__activeMode == type(self).MODE_SHAREPRICE:
            return self.__sharepriceInstanceforecastInstance
        elif self.__activeMode == type(self).MODE_ALARM:
            return self.__alarmInstance
        # if basic color is selected or an invalid value, switch back to basic colors
        else:
            return self.__basiccolorInstance
        
    def __deactiveModeInstance(self):
        # TODO implement "flush" of current active mode
        pass
    
            
########################################
#                MAIN                  #
########################################
if __name__ == '__main__':
    # configuration for multi base example is available via config file
    # only color mode can be selected via cmd line (how about brightness)
    # TODO adapt command line options for later multi mode selection
    # TODO brightness from cmd_options
    opts = cmd_options(catatumbo.starter.CatatumboStart.__version__, 
                       catatumbo.starter.CatatumboStart.__updated__,
                       par = "extended")
    
    # start external configuration interceptor
    # use default configuration: listening externally and on port 8080
    threading.Thread(target =  catatumbo.core.interceptor.server.configuration_service.startServer).start()

    #event though we have a singleton, python differentiate between __main__.CatatumboStart and catatumbo.starter.CatatumboStart
    ci = catatumbo.starter.CatatumboStart(opts)
    # TODO change standard mode
    ci.setActiveMode(catatumbo.starter.CatatumboStart.MODE_WEATHERFORECAST)