# Catatumbo
Catatumbo is an Adaptive Smart Home Lightning project that lets your home indicate information of relevance for you. It shows real world information like stock-market price mode or weather forecast mode via color representation. While each device can foresee a different mode, in special cases they can also act together - e.g. for indicating an alarm situation in the whole appartment.

The project is named after the famous weather spectacle 'Faros del Catatumbo', showing up as silent thunderstorms over the marshlands of Catatumbo river in Venezuela.
Let yourself be dragged into the fascination of Catatumbo - Happy weather watching!

# Available Modes
## Weather Forecast
Visualizes the weather forecast based on OpenWeatherMap data.

![Color representation of different weather conditions for Catatumbo LED strip](https://github.com/MBizm/Catatumbo/blob/master/docs/forecast/color_chart-stairs.jpg)

Want to have a permanent overview of the weather condition in the next days? Don't like to be surprised by sudden rain or snow fall?
The forecast module represents the weather forecast as color code on your led strip. Select between a range of today up until in 5 days, shown as 3 hours blocks. It divides into warm, medium and cold temperatures. For each of the temperature ranges, it will deviate the color to indicate the presence of clouds, rain and snow.
How to get started? Simply configure the configuration file test/adafruit/forecast/config/FORECASTCONFIG.properties with the following attributes:

*   An OpenWeatherMap account key - simply register at [https://openweathermap.org/] for a free account 
*   An IPInfo account key - simply register at [https://ipinfo.io/] for a free account
*	Your led strip(s) configuration

**That's all!** You may define a location different than your current location by defining its longitude/latitude or city name/country. Otherwise Catatumbo will automatically take your current location for weather forecast.

## Stock Price
Visualizes a defined share and compares its performance against its leading index. The timeline will represent the performance in the form of a color graph, letting you know when your share performed well or bad and how it performed in comparison to the leading index.
**This project currently awaits porting to Adafruit. It will be available soon.** 

# Getting Started - Quick Guide
For setting up your own Catatumbo light strip, follow the below steps:
* copy the files and copy it to your Raspberry (e.g. user home dir)
* attach led strip based on the guidance in below Contruction Guide
* assure you have Python3 installed on your Raspberry
* go to the Catatumbo home folder
* run 'sudo pip3 install -r requirements.txt'
* start Catatumbo server by typing 'sudo python3 -m catatumbo.starter -m 7' - this will activate 5d day-time weather forecast

# Construction Guide
For running Catatumbo light strip your require:
* A Raspberry PI 3 or above
* An LED strip, Adafruit LED strips or similar 5050-sized LED strips
* Depending on the length and required power you may need additional power supply for the LED strip

## Fritzing circuit diagram
Setting up the component for your Catatumbo LED strip is easy. Depending on the length of your LED strip, power supply from Raspberry may be sufficient (usually Raspberry can supply 1m with 30 LEDs).
![Raspberry circuit diagram for LED strip with power supply](https://github.com/MBizm/Catatumbo/blob/master/docs/core/circuit-diagram-RaspiAdafruitLED.jpg)

# Developer Quick Guide
Catatumbo comes with a set of controller, utility classes, a JSON server instance and configuration files. Controller define the mode of the led strip by translating corresponding real-world information in color representations on the LED strip. Utility classes abstract the lower level LED strip implementation. The JSON server is the gateway for [Catatumbo WebApp](https://github.com/MBizm/CatatumboWebApp) to interact with the Catatumbo server. The configuration files contain LED configuration (like numer of LEDs and Raspberry pin), service account information (like IPInfo and OWM account information) and dynamic configuration (like LED brightness and daytime/nighttime mode).

## Packages
These are the most important packages of Catatumbo lib:
* *./catatumbo* - main package for all catatumbo server files
* *./catatumbo/controller* - contains the controller classes that represent the different modes, e.g. weather forecast
* *./core* - contains LED abstraction classes as well as additional utility and JSON server files required for running Catatumbo server
* *./core/interceptor* - contains simple JSON server that exposes services on port 8080
* *./test* - currently combines a number of test files as well as Catatumbo server configuration
* *./test/catatumbo/forecast/config* - currently contains the configuration file for initial start up required for running Catatumbo server (FORECASTCONFIG.properties). At runtime an additional file will be created that represents the changed configuration (RUNTIMECONFIG.properties) that if present will be prioritized. Location of configuration files may change in later versions of Catatumbo.

## Classes
These are the most important classes of Catatumbo lib:
* *./catatumbo/starter.py* - central startup class that starts the predefined mode. It will initialize the controller for setting up the LED strip and start the JSON server to allow interaction via the [Catatumbo WebApp](https://github.com/MBizm/CatatumboWebApp).
* *./catatumbo/core/neopixel_multibase.py* - the main abstraction class for derived controllers. All controller should derive from this class. It already comes with support for multiple LED strip initialization (installation of custom [Adafruit Blinka Lib](https://github.com/MBizm/Adafruit_Blinka) currently is required), automatic determination of the location based on the IP, automatic daytime/nighttime adaption for fading the brightness at nighttime
* *./catatumbo/controller/forecast/adafruit_forecast.py* - the controller for starting the weather forecast. It will retrieve weather information for your current location via OWM API. It is currently started by default by starter.py script.
* *./catatumbo/core/interceptor/server/configuration_server.py* - simple JSON server that exposes several REST services via port 8080 and will be called by [Catatumbo WebApp](https://github.com/MBizm/CatatumboWebApp).

## Custom Controller Guide
By deriving your custom controller from neopixel_multibase.py class, building a custom controller is easy and comes already with functionality like support for multiple LED strips and daytime/nighttime brightness adaption.
Getting the French tricolore filling up your strip is a matter of a few lines:

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

# Credits
- [OpenWeatherMap](https://openweathermap.org/) - weather data is provided under the [Open Data Commons Open Database License(ODbL)](http://opendatacommons.org/licenses/odbl/)
- [IPInfo](https://github.com/ipinfo/python)
- [Astral](https://github.com/sffjunkie/astral)
- [Adafruit Lib for WS281x SK681x LEDs](https://github.com/adafruit)
