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
from adafruit.core.util.cmd_functions import cmd_options
from adafruit.controller.forecast.adafruit_forecast import NeoPixelForecast
from adafruit.controller.forecast.forecast_colors import ForecastNeoPixelColors
from adafruit.core.util.update_thread import queueUpdate

class AdafruitStart():
    
    __version__ = 0.1
    __updated__ = '2020-01-03'
    
    """
    OBJECT ATTRIBUTES
    """    
    __instance = None
    __options = None
    forecast = None

    """
        static class constructor for singleton
    """
    def __new__(cls, *args, **kwargs):
        if AdafruitStart.__instance is None:
            AdafruitStart.__instance = object.__new__(cls)
        return AdafruitStart.__instance

    """
        constructor for singleton
        TODO define default constructor parameters, parametrization for modes
        
        :param    opts: command line options of starter module
        :type     opts: class
    """    
    def __init__(self, opts):
        __options = opts
    
    
    """
        TODO
    """    
    def startWeatherForecast(self):
        # create forecast instance
        if self.forecast is None:
            self.forecast = NeoPixelForecast(color_schema  = ForecastNeoPixelColors)
        
        # start repetitive update
        queueUpdate(self.forecast, opts.mode)
        
        if opts.bright is not None:
            self.forecast.setBrightness(opts.bright)

########################################
#                MAIN                  #
########################################
if __name__ == '__main__':
    # configuration for multi base example is available via config file
    # only color mode can be selected via cmd line (how about brightness)
    # TODO adapt command line options for later multi mode selection
    opts = cmd_options(AdafruitStart.__version__, 
                       AdafruitStart.__updated__,
                       par = "extended")
    
    starter = AdafruitStart(opts)
    
    # TODO change standard mode
    starter.startWeatherForecast()