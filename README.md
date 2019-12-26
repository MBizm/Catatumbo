# Catatumbo
Catatumbo is an Adaptive Smart Home Lightning project that lets your home indicate information of relevance for you. Say you want to your led strip to show how your favorite share price correlates to how the the leading index is performing.
The project is named after the famous weather spectacle *'Faros del Catatumbo'*, showing up as silent thunderstorms over the marshlands of Catatumbo river in Venezuela. 

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

*   Connecting multiple strips transparently, see example [here] (https://github.com/MBizm/Catatumbo/blob/master/src/test/adafruit/forecast/neopixel_multibase_test.py)
*   Having two separate instances being controlled by your Raspberry, see example [here](https://github.com/MBizm/Catatumbo/blob/master/src/test/adafruit/forecast/neopixel_base_threadtest.py)

_REMARK: Multi-strip support currently depends on adapted Adafruit Blinka lib. This version of the driver supports several GPIO pins (12, 13, 18, 19, 21). For avoiding interference between the instances, pin 18 and 21 is recommended. Find the adapted version of Adafruit Blinka [here](https://github.com/MBizm/Adafruit_Blinka)._ 



# Projects
## Forecast
Visualizes the weather forecast based on OpenWeatherMap data.
**This project currently awaits porting to Adafruit. It will be available soon.** 
### Forecast-VisualizeTk
Is a simple Python script that renders the weather forecast for temperature (R), cloud coverage (G), rain/snow (B) in RGB scales as well a combined scale.
![Forecast visualization example for London showing weather forecast for the next days in color bars](https://github.com/MBizm/Catatumbo/blob/master/docs/forecast/visualizeTk/example-London.png)
### Forecast-FruitStrip
*#### coming soon ####*

## Stock
Visualizes a defined share and compares its performance against its leading index. The timeline will represent the performance in the form of a color graph, letting you know when your share performed well or bad and how it performed in comparison to the leading index.
**This project currently awaits porting to Adafruit. It will be available soon.** 
## Stock-VisualizeTk
A simple script that shows the full color spectrum how share price and leading index correlate. The closer both indices are, the more it will tend to neutral white. The more the values differentiate, the more it will tend to one of the HSV color circle representation. Find the sample script [here](https://github.com/MBizm/Catatumbo/blob/master/src/test/visualizeTk/stock/FullSpectrum.py).
![Stock price comparison matrix showing the performance of a share correlated to its leading index](https://raw.githubusercontent.com/MBizm/Catatumbo/master/docs/stock/Full%20Spectrum.png)


# Credits
- [OpenWeatherMap](https://openweathermap.org/) - weather data is provided under the [Open Data Commons Open Database License(ODbL)](http://opendatacommons.org/licenses/odbl/)
- [Adafruit Lib for WS281x SK681x leds](https://github.com/adafruit)
