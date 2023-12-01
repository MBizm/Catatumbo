from catatumbo.controller.forecast.adafruit_forecast import NeoPixelForecast
from catatumbo.controller.forecast.forecast_singularcolor import SingularForecastNeoPixelColors


class NeoPixelSingularForecast(NeoPixelForecast):

    def __init__(self, color_schema):
        super().__init__(color_schema)

    """
        return the mask for retrieving the weather report for the next 12 hours
    """

    def _getMask(self, color_mode, offset):
        # for now we just return the next 12 hours
        mask = 0x0F

        # shift by offset to adapt to current time
        mask = mask << offset

        return mask

    """
        consolidates weather extreme of previous weather data with current one in below order:
        -   Prio 1: storm
        -   Prio 2: snow
        -   Prio 3: rain
        -   Prio 4: low/high temperature
        Weather data of multiple entries will be normalized to result in one set of the extremes
    """

    def _fillSampleBoard(self, cdate, index, sampleboard, weather):
        # get 3-byte or 4-byte color representation based on weather condition
        # get map for current condition
        updatedMap = super().mapWeatherConditions(weather.get_temperature(unit='celsius')['temp'],
                                                  weather.get_clouds(),
                                                  0 if len(weather.get_rain()) == 0 else
                                                  list(weather.get_rain().values())[0],
                                                  cdate,
                                                  weather.get_weather_code(),
                                                  len(weather.get_snow()) > 0,
                                                  weather.get_wind()['speed'],
                                                  weather.get_humidity(),
                                                  weather.get_pressure()['press']
                                                  )

        if len(sampleboard) > 0:
            previousMap = sampleboard[0]
        else:
            # lazy initialization...
            previousMap = updatedMap

        # transfer extreme values from previous set
        # temperature transfer only relevant for non-extreme weather conditions
        if previousMap["cloud"] > updatedMap["cloud"]:
            updatedMap["cloud"] = previousMap["cloud"]
        if previousMap["rain"] > updatedMap["rain"]:
            updatedMap["rain"] = previousMap["rain"]
        if previousMap["wind"] > updatedMap["wind"]:
            updatedMap["wind"] = previousMap["wind"]
        if previousMap["humidity"] > updatedMap["humidity"]:
            updatedMap["humidity"] = previousMap["humidity"]
        if previousMap["pressure"] < updatedMap["pressure"]:
            updatedMap["pressure"] = previousMap["pressure"]

        # handle weather extremes
        if updatedMap["CATAcode"] == type(self).CONDITION_STORM or \
                previousMap["CATAcode"] == type(self).CONDITION_STORM:
            updatedMap["color"] = SingularForecastNeoPixelColors.W_STORM
            updatedMap["debug"] = "storm"
            if previousMap["CATAcode"] == type(self).CONDITION_STORM:
                updatedMap["OWMcode"] = previousMap["OWMcode"]
            updatedMap["CATAcode"] = type(self).CONDITION_STORM
        elif updatedMap["CATAcode"] == type(self).CONDITION_SNOW or \
                previousMap["CATAcode"] == type(self).CONDITION_SNOW:
            updatedMap["color"] = SingularForecastNeoPixelColors.W_SNOW
            updatedMap["debug"] = "snow"
            if previousMap["CATAcode"] == type(self).CONDITION_SNOW:
                updatedMap["OWMcode"] = previousMap["OWMcode"]
            updatedMap["CATAcode"] = type(self).CONDITION_SNOW
        # handle non-extreme weather conditions
        else:
            if updatedMap["CATAcode"] & type(self).CONDITION_SLRAI == type(self).CONDITION_SLRAI or \
                    updatedMap["CATAcode"] & type(self).CONDITION_RAI == type(self).CONDITION_RAI or \
                    previousMap["CATAcode"] & type(self).CONDITION_SLRAI == type(self).CONDITION_SLRAI or \
                    previousMap["CATAcode"] & type(self).CONDITION_RAI == type(self).CONDITION_RAI:
                if previousMap["CATAcode"] == type(self).CONDITION_RAI or \
                        previousMap["CATAcode"] == type(self).CONDITION_SLRAI and not (
                        updatedMap["CATAcode"] == type(self).CONDITION_RAI):
                    updatedMap["OWMcode"] = previousMap["OWMcode"]
                updatedMap["CATAcode"] = type(self).CONDITION_RAI

            if updatedMap["CATAcode"] & type(self).CONDITION_LTMP == type(self).CONDITION_LTMP or \
                    previousMap["CATAcode"] & type(self).CONDITION_LTMP == type(self).CONDITION_LTMP:
                if previousMap["temp"] < updatedMap["temp"]:
                    updatedMap["temp"] = previousMap["temp"]
                updatedMap["CATAcode"] = updatedMap["CATAcode"] | type(self).CONDITION_LTMP
            elif updatedMap["CATAcode"] & type(self).CONDITION_HTMP == type(self).CONDITION_HTMP or \
                    previousMap["CATAcode"] & type(self).CONDITION_HTMP == type(self).CONDITION_HTMP:
                if previousMap["temp"] > updatedMap["temp"]:
                    updatedMap["temp"] = previousMap["temp"]
                updatedMap["CATAcode"] = updatedMap["CATAcode"] | type(self).CONDITION_HTMP

            # final color alignment
            if updatedMap["CATAcode"] & type(self).CONDITION_HTMP == type(self).CONDITION_HTMP:
                if updatedMap["CATAcode"] & type(self).CONDITION_RAI == type(self).CONDITION_RAI:
                    updatedMap["color"] = SingularForecastNeoPixelColors.W_HITMP_RAINY
                    updatedMap["debug"] = "rainy, high temp"
                else:
                    updatedMap["color"] = SingularForecastNeoPixelColors.W_HITMP
                    updatedMap["debug"] = "high temp"
            elif updatedMap["CATAcode"] & type(self).CONDITION_LTMP == type(self).CONDITION_LTMP:
                if updatedMap["CATAcode"] & type(self).CONDITION_RAI == type(self).CONDITION_RAI:
                    updatedMap["color"] = SingularForecastNeoPixelColors.W_LOWTMP_RAINY
                    updatedMap["debug"] = "rainy, low temp"
                else:
                    updatedMap["color"] = SingularForecastNeoPixelColors.W_LOWTMP
                    updatedMap["debug"] = "low temp"
            elif updatedMap["CATAcode"] & type(self).CONDITION_RAI == type(self).CONDITION_RAI:
                updatedMap["color"] = SingularForecastNeoPixelColors.W_MIDTMP_RAINY
                updatedMap["debug"] = "rainy, mid temp"
            else:
                updatedMap["color"] = SingularForecastNeoPixelColors.W_MIDTMP
                updatedMap["debug"] = "mid temp"

        return {0: updatedMap}
