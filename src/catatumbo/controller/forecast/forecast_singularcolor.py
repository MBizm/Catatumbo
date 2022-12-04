#!/usr/bin/env python
# encoding: utf-8
'''
This is a sample of colors for forecast apps
Colors are defined on base class based on the perceived colors resulting from an WS2811 LED strip.

Current version of the class only addresses RGBW capable chips

@author:     MBizm

@copyright:  2021 organization_name. All rights reserved.

@license:    Apache License 2.0

@deffield    created: November 2021
@deffield    updated: Updated
'''
from catatumbo.core.neopixel_colors import NeoPixelColors


class SingularForecastNeoPixelColors(NeoPixelColors):
    """
    STATIC CLASS ATTRIBUTES
    """
    W_HITMP = None  # high temperature, no rain, no clouds
    W_HITMP_RAINY = None  # high temperature, rainy

    W_MIDTMP = None  # mid temperature, no rain, no clouds
    W_MIDTMP_RAINY = None  # mid temperature, rainy

    W_LOWTMP = None  # low temperature, no rain, no clouds
    W_LOWTMP_RAINY = None  # low temperature, rainy

    W_SNOW = None
    W_STORM = None

    """
        initializer for RGBW LED strip
    """

    def __initDerivedColors__(self):
        super().__initDerivedColors__()

        type(self).W_HITMP = SingularForecastNeoPixelColors.W_RED  # high temperature, no rain, no clouds
        type(self).W_HITMP_RAINY = SingularForecastNeoPixelColors.W_CYAN  # high temperature, rainy

        type(self).W_MIDTMP = SingularForecastNeoPixelColors.W_LIGHT_ORANGE # mid temperature, no rain, no clouds
        type(self).W_MIDTMP_RAINY = SingularForecastNeoPixelColors.W_LIGHT_BLUE  # mid temperature, rainy

        type(self).W_LOWTMP = SingularForecastNeoPixelColors.W_LIGHT_GREEN  # low temperature, no rain, no clouds
        type(self).W_LOWTMP_RAINY = SingularForecastNeoPixelColors.W_BLUE  # low temperature, rainy

        type(self).W_SNOW = SingularForecastNeoPixelColors.W_LIGHT_WHITE
        type(self).W_STORM = SingularForecastNeoPixelColors.W_LIGHT_MAGENTA

