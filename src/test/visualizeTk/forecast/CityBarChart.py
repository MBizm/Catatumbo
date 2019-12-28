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
from tkinter import Tk, Canvas, font, mainloop
from configparser import NoSectionError, NoOptionError
from pyowm import OWM
from datetime import datetime, timedelta
from pyowm.exceptions.api_call_error import APIInvalidSSLCertificateError

#standard size of period rectangles for visualization
RECT_W = 20
RECT_H = 20

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
    config = configparser.RawConfigParser()
    config.read('../../../test/adafruit/forecast/config/FORECASTCONFIG.properties')
        
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
    uses TK to setup a Canvas for painting the scales in the order:
        - temperature
        - cloud coverage
        - rain and snow
        - combined values resulting from combined RGB of the previous three
        
    :param    tc: forecast object from OWM
    :type     tc: *Forecast* instance
    :param    location: location description for output
    :type     location: str
    :param    startdate: start date of forecast period
    :type     startdate: ``datetime.datetime`` object instance
"""
def visualizeWeatherForecast(fc, location, startdate):
    #initialize canvas
    root = Tk()
    root.geometry("850x250")
    root.title(location)
    canvas = Canvas(root, width=900, height=500)
    canvas.pack()
    
    #draw location information and scale for boxes with time information
    paintLocationAndTime(canvas,location)

    #iterate forecasts & store original as well as mapped data on a scale of 255
    #OWM API: https://openweathermap.org/forecast5
    index = 0
    period = int(startdate.hour / 3) #forecast is divided by 3h periods

    for weather in fc:
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

        #paint weather boxes for the current index
        paintScalePeriod(canvas, t, tm, c, cm, r, rm, index, startdate, (period + index))
        index = index + 1

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

"""
    paints textual information about location and scales:
        - city [country]
        - scale metric
        - time information
    
    :param    canvas: an TK area for painting
    :type     canvas: *Canvas* instance
    :param    location: location description for output
    :type     location: str
"""
def paintLocationAndTime(canvas, location):
    #paint location header
    f = font.Font(size=20, family="Times", slant="italic", weight="bold")
    x1 = f.measure(location)
    y1 = f.metrics('linespace')
    canvas.create_text(20 + x1 / 2,     #x - x location dependent on text length
                       5 + y1 / 2,      #y
                       text = location,
                       fill = 'black',
                       font = f)
    f = font.Font(size=10, family="Times", slant="italic", weight="bold")
    t = "[" + datetime.now().strftime("%A, %d. %B %Y %I:%M%p") + "]"
    canvas.create_text(20 + x1 + 20 + f.measure(t) / 2,     #x - x location dependent on text length
                   5 + (y1 - f.metrics('linespace') / 2) - 1,    #y
                   text = t,
                   fill = 'black',
                   font = f)
    
    #scale metric
    f = font.Font(size=10, family="Times", slant="roman", weight="normal")
    for sc in range (1, 5):
        metric = {1 : "RED - Temperature [Celsius]", 
                  2 : "GREEN - Cloud Coverage [Percent]", 
                  3 : "BLUE - Rain/Snow [l/sqm]", 
                  4 : "Combined"}[sc]
        canvas.create_text(20 + f.measure(metric) / 2,          #x
                           0.5 * RECT_H + RECT_H * (sc * 2),    #y
                           text=metric,
                           fill = 'black',
                           font = f)    
        
"""
    paints a box for a given period for all scales:
        - temperature
        - cloud coverage
        - rain and snow
        - combined values resulting from combined RGB of the previous three
    
    :param    canvas: an TK area for painting
    :type     canvas: *Canvas* instance
    :param    t: temperature value for period
    :type     t: int in celsius
    :param    tm: mapped color of temperature value for period
    :type     tm: int
    :param    c: cloud percentage value for period
    :type     c: int in percentage
    :param    cm: mapped color of cloud coverage value for period
    :type     cm: int
    :param    r: rain value for period
    :type     r: int in l/hour and sqrmeter 
    :param    rm: mapped color of rain value for period
    :type     rm: int
    :param    index: counter for index in complete scale
    :type     index: int   
    :param    startdate: start date of the whole forecast period, period defines which 3h period is the current
    :type     startdate: 
    :param    period: counter for period of the day, each period represents a 3h slot, periods will be summed up from forecast start
    :type     period: int
"""
def paintScalePeriod(canvas, t, tm, c, cm, r, rm, index, startdate, period):
    f = font.Font(size=10, family="Times", slant="roman", weight="normal")
    
    #paint color boxes with value inside
    for sc in range (1, 5):
        canvas.create_rectangle(20 + RECT_W * index,                                    #x1
                                RECT_H + RECT_H * (sc * 2),                             #y1
                                20 + RECT_W * (index + 1),                              #x2
                                2 * RECT_H + RECT_H * (sc * 2),                         #y2
                                fill=_from_rgb((tm if sc == 1 or sc == 4 else 0,        #temperature scale
                                                cm if sc == 2 or sc == 4 else 0,        #cloud coverage scale
                                                rm if sc == 3 or sc == 4 else 0)))      #rain scale
        canvas.create_text(20 + RECT_W * index + RECT_W / 2,                            #x
                           1.5 * RECT_H + RECT_H * (sc * 2),                            #y
                           text=int(t if sc == 1 else
                                        c if sc == 2 else
                                        r if sc == 3 else
                                        index),
                           fill = 'white',
                           font = f)
        
    #add time and date scale at the bottom
    dtText = None
    ts = period % 8 #check start time of period
    if(ts == 2):
        dtText='|6am'
    elif(ts == 7):
        dtText='|9pm'
    elif(ts == 3):
        #calculate the current day based on period
        dt = startdate + timedelta(days=int(period / 8))
        dtText = "   " + dt.strftime("%a, %d.%b")
            
    if(not dtText is None):
        canvas.create_text(20 + RECT_W * index + f.measure(dtText) / 2, #x
                           1.5 * RECT_H + RECT_H * 9,                   #y
                           text=dtText,
                           fill = 'black',
                           font = f)
    #adding a line for marking daytime
    if(ts >= 2 and ts < 7):
        canvas.create_line(20 + RECT_W * index,                         #x1
                           1.5 * RECT_H + RECT_H * 9.5,                  #y1
                           20 + RECT_W * index + RECT_W,                #x2
                           1.5 * RECT_H + RECT_H * 9.5,                  #y2
                           fill='black')
"""
"
"    ####### MAIN #######
"
"""
if __name__ == '__main__':
    #get your personal key
    API_KEY = getProperty('Forecast-ConnectionData', 'APIKey');
    if(API_KEY is None):
        API_KEY = input('Enter your API Key: ')
    
    #get location for request
    #TODO get location via IP: https://ipinfo.io/developers
    cityID = getProperty('Forecast-ApplicationData', 'CityID')
    city = getProperty('Forecast-ApplicationData', 'CityName')
    country = getProperty('Forecast-ApplicationData', 'Country')
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
            cityName = loc[1]
            country = loc[2]
        except (ValueError, IndexError):
            print('Defined city could not be found!')
            sys.exit();
            
    #request forecast
    #https://pyowm.readthedocs.io/en/latest/usage-examples-v2/weather-api-usage-examples.html#getting-weather-forecasts
    try:
        forecast = owm.three_hours_forecast_at_id(int(cityID))
    except (APIInvalidSSLCertificateError):
        #TODO need to check how lib would react if max request for free OWM account reached
        print('Establishing a network connection failed!')
        sys.exit();

    visualizeWeatherForecast(forecast.get_forecast(), 
                             location=city+", " + country, 
                             startdate=forecast.when_starts('date'))
    
    mainloop()