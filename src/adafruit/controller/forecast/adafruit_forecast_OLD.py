'''
The visualization script will present the weather forecast for the next days in 3 hour period for a defined location.
It requires a valid OpenWeatherMap key - free of charge for a limited amount of requests. See OWM website for more information: https://openweathermap.org/price.
Static configuration can be done by CONFIG.properties file. Otherwise values will be requested via command line.

Resulting Tk Canvas will output 3 scales with temperature (red), cloud coverage (green) and rain forecast (blue) as well as an additional combined scale.

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

@author: MBizm
'''
import configparser
import sys
from configparser import NoSectionError, NoOptionError
from pyowm import OWM
from pyowm.exceptions.api_call_error import APIInvalidSSLCertificateError
import time 
import board
import neopixel
from ...core.forecast.forecast_colors import ForecastNeoPixelColors

# Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18
# NeoPixels must be connected to D10, D12, D18 or D21 to work.
PIXEL_PIN = board.D18

# The number of NeoPixels
NUM_PIXELS = 60

# defines the time in seconds that it will take to from an illuminated to faded state
# calculation will be based on 190 individual steps for dimming from which 100 are twice the speed - step divider 280
CYCLE_TIME = 15

# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.GRBW


"""
    TODO
    
"""
def init():
    global PIXEL_PIN
    global NUM_PIXELS
    global CYCLE_TIME
    global ORDER
    global API_KEY
    
    global owm
    global cityID
    global pixels
    
    #get your personal key
    API_KEY = getProperty('ConnectionData', 'APIKey');
    if(API_KEY is None):
        API_KEY = input('Enter your API Key: ')
    
    #get location for request
    #TODO get location via IP: https://ipinfo.io/developers
    cityID = getProperty('ApplicationData', 'CityID')
    city = getProperty('ApplicationData', 'CityName')
    country = getProperty('ApplicationData', 'Country')
    if(cityID is None):
        if(country is None):
            country = input('Enter your country: ')
        if(city is None):
            city = input('Enter your city: ')
            
    #initiate OpenWeatherMap object
    owm = OWM(API_KEY);
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
    
    pixels = neopixel.NeoPixel(PIXEL_PIN, NUM_PIXELS, brightness=0.2, auto_write=False,
                               pixel_order=ORDER)
    
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
def getProperty(p_section, p_attribute):
    #TODO make this a static class attribute
    config = configparser.RawConfigParser()
    config.read('adafruit/core/forecast/CONFIG.properties')
        
    try:
        ret = config.get(p_section, p_attribute)
    except (NoOptionError, NoSectionError):
        return None;
    return ret;    

"""
    converts the RGB color code into numerical representation in the range of 0-100
    
    :param    rgb: RGB values
    :type     rgb: dict of RGB values
    :returns: converted RGB value
"""
def _from_rgb(rgb):
    #translates an rgb tuple of int to a tkinter friendly color code
    return "#%02x%02x%02x" % rgb

"""
    maps the temperature value into a continuous RGB value starting from 60 up to 255 in the temperature range of -10 celsius up to 35 celsius
    see \docs\forecast\ColorScale.png for more information
    
    :param    t: temperature
    :type     t: float
    :returns: mapped temperature
"""
def mapTemperatureToRGB(t):
    t = t + 10
    if t < 0:
        t = 0
    elif t > 45:
        t = 45
    
    return int(60 + (195 * (1 / 45 * t)))

"""
    maps the cloud coverage value into a discrete RGB value by the for categories (no clouds, slightly, cloudy, covered) based on DWD terminology
    see \docs\forecast\ColorScale.png for more information
    
    :param    c: percentage of cloud coverage
    :type     c: float
    :returns: mapped cloud coverage
"""   
def mapCloudsToRGB(c):
    if c < (100*1/8):       #no clouds
        return 255
    elif c < (100*3/8):     #slightly cloudy
        return 201
    elif c < (100*6/8):     #cloudy
        return 148
    else:                   #covered
        return 95

"""
    maps the rain value into a discrete RGB value by the for categories (no rain, slightly, moderate, heavy) based on DWD terminology
    see \docs\forecast\ColorScale.png for more information
    
    :param    r: amount of rain on l/sqm
    :type     r: float
    :returns: mapped rain
"""  
def mapRainToRGB(r):
    if r < 0.3:             #no rain
        return 95
    elif r < 2.5:           #slightly
        return 148
    elif r < 10:            #moderate
        return 201
    else:                   #heavy
        return 255

def setBrightness(brightness, delay):
    pixels.brightness = brightness
    pixels.show()
    #print('brightness level: ' + str(brightness))
    time.sleep(delay)


if __name__ == '__main__':
        
    sampleboard = (())
    sectionsize = 0
    
    init()
    
    pixels = neopixel.NeoPixel(PIXEL_PIN, NUM_PIXELS, brightness=0.2, auto_write=False,
                               pixel_order=ORDER)

    #print('addressable pixels: ' + str(NUM_PIXELS) + ' section size: ' + str(sectionsize))
    
    #request forecast
    #https://pyowm.readthedocs.io/en/latest/usage-examples-v2/weather-api-usage-examples.html#getting-weather-forecasts
    try:
        forecast = owm.three_hours_forecast_at_id(int(cityID))
    except (APIInvalidSSLCertificateError):
        #TODO need to check how lib would react if max request for free OWM account reached
        print('Establishing a network connection failed!')
        sys.exit();
    
    #TODO comments
    startdate=forecast.when_starts('date')
    index = 0
    period = int(startdate.hour / 3) #forecast is divided by 3h periods
    
    nextday_range = False
    
    for weather in forecast.get_forecast():
        ts = (period + index) % 8 #check start time of period
        
        #6am - set start signal
        if(ts == 2):
            nextday_range = True     
        
        index = index + 1

        #check if period is within next day's range
        if nextday_range == False:
            continue
        
        #record 6am to 9pm weather forecast
        #temperature
        t = next(iter(weather.get_temperature(unit='celsius').values()))
        tm = mapTemperatureToRGB(t)#int(255/45* ((45 if t > 45 else (-10 if t < -10 else t)) + 10))
        #cloud coverage
        c = weather.get_clouds()
        cm = mapCloudsToRGB(c)#int(255-255/100*c)
        #rain 
        r = 0 if len(weather.get_rain()) == 0 else list(weather.get_rain().values())[0]
        rm = mapRainToRGB(r)
        #special color for any kind of snow fall - snow white is coming
        if (len(weather.get_snow()) > 0):
            tm = 100
            cm = 200
            rm = 255
            
        sampleboard = sampleboard + ((tm, cm, rm),)
    
        #9pm - stop recording
        if ts == 7 and nextday_range == True:
            break

    sectionsize = int(NUM_PIXELS / len(sampleboard))
    
    setBrightness(80, 0)

    # preset pixel colors
    for i in range(NUM_PIXELS-1):
        # fill up remaining pixels
        if(int(i / sectionsize) >= len(sampleboard)):
            pixels[i+1] = sampleboard[len(sampleboard) - 1] 
        # preset pixel colors according to color space set  
        else:
            pixels[i+1] = sampleboard[int(i / sectionsize)]
            print('[' + str(i) + '] ' + str(sampleboard[int(i / sectionsize)]))
    pixels.show()
    
    while False:
        # direction = 0 - fading from illuminated state, direction = 1 - illuminating
        for direction in range (0, 2, 1):
            # iterating brightness level in the range of 1.0 and 0.1, step size 0.01
            for i in range(100, 0, -1):
                
                # iterating brightness level in the range of 0.0 and 0.099, step size 0.001
                if i == 100 and direction == 1:
                    for j in range(99, 0, -1):
                        setBrightness(abs(100 * direction - j) / 1000,
                                      CYCLE_TIME / (2 * (90 + 50)))
                
                # iterating brightness level in the range of 1.0 and 0.1, step size 0.01
                # skip the range between 0.1 and 0
                if (direction == 0 and i >= 10) or (direction == 1 and i <= 90):
                    setBrightness(abs(100 * direction - i) / 100,
                                  CYCLE_TIME / (90 + 50))
                
                # iterating brightness level in the range of 0.099 and 0.0, step size 0.001
                if i == 10 and direction == 0:
                    for j in range(99, 0, -1):
                        setBrightness(abs(100 * direction - j) / 1000,
                                      CYCLE_TIME / (2 * (90 + 50)))