# Catatumbo
Catatumbo is an Adaptive Smart Home Lightning project that lets your home indicate information of relevance for you. It aims to build up light components (led strips) that are distributed across the appartement. Each device being addressed via network or KNX in the future. While each device can foresee a different scene, in special cases they can also act together - e.g. for indicating an alarm situation in the whole appartment. Special focus is on adaptive lightning scenes which indicate real world information via color codes - e.g. stock prices, weather forecasts, social media states. Say you want to your led strip to show how your favorite share price correlates to how the the leading index is performing or just by having your hall stand illuminated in bright blue may indicate that you better take the umbrella along.
The project is named after the famous weather spectacle 'Faros del Catatumbo', showing up as silent thunderstorms over the marshlands of Catatumbo river in Venezuela.

Let yourself be dragged into the fascination of Catatumbo - Happy weather watching!

# Benefits
Using the Catatumbo library brings you the following benefits:
## Simplicity
The Catatumbo lib let's you program your led strip in the easiest way. Getting the French tricolore filling up your strip is a matter of a few lines:

	np = NeoPixelBase(pixelpin     = board.D18, 
                      pixelnum     = 300, 
                      pixelorder   = neopixel.GRBW, 
                      color_schema = NeoPixelColors,
                      brightness   = 0.2)
    
    # preset sampleboard - Viva la France!
    sampleboard = (NeoPixelColors.W_BLUE,
                   NeoPixelColors.W_WHITE,
                   NeoPixelColors.W_RED)    

    np.setPixelBySampeboard(sampleboard)
That's all! Find the sample module allowing you to configure led strip parametrization from the command line (`--version`) [here](https://github.com/MBizm/Catatumbo/blob/master/src/test/adafruit/neopixel_base_simpletest.py). 
## Abstraction
With Catatumbo lib you do not have to care about led strip specifics. Just wire up the strip and run the module. Whether it is predefined color values, matching color schemas, or using configuration files - the abstraction layer let's you do it in a structured and easy way.
## Multi-strip support
Do you want to connect multiple led strips to your Raspberry? Catatumbo lib let's you create multiple instances which can be easily configured and change the color pattern or brightness independently. At the same time, Catatumbo may abstract the usage of multiple strips directly connected to the Raspberry by representing it as one. As a result, you just set up one sampleboard and Catatumbo will spread it across all available instances.

*   Connecting multiple strips transparently, see example [here](https://github.com/MBizm/Catatumbo/blob/master/src/test/adafruit/forecast/neopixel_multibase_test.py)
*   Having two separate instances being controlled by your Raspberry, see example [here](https://github.com/MBizm/Catatumbo/blob/master/src/test/adafruit/forecast/neopixel_base_threadtest.py)

_REMARK: Multi-strip support currently depends on adapted Adafruit Blinka lib. This version of the driver supports several GPIO pins (12, 13, 18, 19, 21). For avoiding interference between the instances, pin 18 and 21 is recommended. Find the adapted version of Adafruit Blinka [here](https://github.com/MBizm/Adafruit_Blinka)._ 



# Projects
## Forecast
Visualizes the weather forecast based on OpenWeatherMap data.
### Forecast-FruitStrip
Want to have a permanent overview of the weather condition in the next days? Don't like to be surprised by sudden rain or snow fall?
The forecast module represents the weather forecast as color code on your led strip. Select between a range of today up until in 5 days, shown as 3 hours blocks. It divides into warm, medium and cold temperatures. For each of the temperature ranges, it will deviate the color to indicate the presence of clouds, rain and snow.
How to get started? Simply configure the configuration file test/adafruit/forecast/config/FORECASTCONFIG.properties with the following attributes:

*   An OpenWeatherMap account key - simply register at [https://openweathermap.org/] for a free account 
*   An IPInfo account key - simply register at [https://ipinfo.io/] for a free account
*	Your led strip(s) configuration

**That's all!** You may define a location different than your current location by defining its longitude/latitude or city name/country. Otherwise Catatumbo will automatically take your current location for weather forecast.
_For an overview how the weather will be rendered with your defined configuration, you may have a look into [Tk Forecast script](https://github.com/MBizm/Catatumbo/blob/master/src/test/visualizeTk/forecast/CityBarChart.py)._


## Stock
Visualizes a defined share and compares its performance against its leading index. The timeline will represent the performance in the form of a color graph, letting you know when your share performed well or bad and how it performed in comparison to the leading index.
**This project currently awaits porting to Adafruit. It will be available soon.** 
## Stock-VisualizeTk
A simple script that shows the full color spectrum how share price and leading index correlate. The closer both indices are, the more it will tend to neutral white. The more the values differentiate, the more it will tend to one of the HSV color circle representation. Find the sample script [here](https://github.com/MBizm/Catatumbo/blob/master/src/test/visualizeTk/stock/FullSpectrum.py).
![Stock price comparison matrix showing the performance of a share correlated to its leading index](https://raw.githubusercontent.com/MBizm/Catatumbo/master/docs/stock/Full%20Spectrum.png)


# Credits
- [OpenWeatherMap](https://openweathermap.org/) - weather data is provided under the [Open Data Commons Open Database License(ODbL)](http://opendatacommons.org/licenses/odbl/)
- [IPInfo](https://github.com/ipinfo/python)
- [Astral](https://github.com/sffjunkie/astral)
- [Adafruit Lib for WS281x SK681x LEDs](https://github.com/adafruit)
