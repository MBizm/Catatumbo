#!/usr/bin/env python
# encoding: utf-8
'''
Test program for simple NeoPixelBase
This script shows the simplest way to initialize an led strip, rendering the tricolore.


@author:     MBizm

@copyright:  2019 organization_name. All rights reserved.

@license:    Apache License 2.0

@deffield    created: December 2019
@deffield    updated: Updated
'''
from catatumbo.core.neopixel_base import NeoPixelBase
from catatumbo.core.util.cmd_functions import cmd_options
from catatumbo.core.neopixel_colors import NeoPixelColors

########################################
#                MAIN                  #
########################################
if __name__ == '__main__':
    # interpret cmd line arguments
    opts = cmd_options(NeoPixelBase.__version__, 
                       NeoPixelBase.__updated__,
                       par = "simple")
    
    np = NeoPixelBase(pixelpin     = opts.port, 
                      pixelnum     = int(opts.len), 
                      pixelorder   = opts.schema, 
                      color_schema = NeoPixelColors,
                      brightness   = float(opts.bright))
    
    # preset sampleboard - Viva la France!
    sampleboard = (NeoPixelColors.W_BLUE,
                   NeoPixelColors.W_WHITE,
                   NeoPixelColors.W_RED)    

    np.setPixelBySampleboard(sampleboard)
    
