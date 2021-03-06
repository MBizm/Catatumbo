'''
Provides procedures for command line options

@author:     MBizm

@copyright:  2019 organization_name. All rights reserved.

@license:    Apache License 2.0

@deffield    created: December 2019
@deffield    updated: Updated
'''
import os
import sys
from optparse import OptionParser

def cmd_options(version, updated, par="basic", argv=None):
    '''Command line options.'''

    program_name = os.path.basename(sys.argv[0])
    program_version = "v%s" % version
    program_build_date = "%s" % updated

    program_version_string = '%%prog %s (%s)' % (program_version, program_build_date)
    program_longdesc = '''''' # optional - give further explanation about what the program does
    program_license = "Copyright 2019 user_name (organization_name)                                            \
                Licensed under the Apache License 2.0\nhttp://www.apache.org/licenses/LICENSE-2.0"

    if argv is None:
        argv = sys.argv[1:]
    try:
        # setup option parser
        parser = OptionParser(version=program_version_string, epilog=program_longdesc, description=program_license)
        if par == "extended" or par == "simple":
            # see https://github.com/MBizm/Adafruit_Blinka/blob/master/src/adafruit_blinka/microcontroller/bcm283x/neopixel.py
            parser.add_option("-p", "--port", dest="port", help="redefines the Raspi GPIO port: D12, D13, D18, D19, D21 [default: %default]")
            parser.add_option("-l", "--length", dest="len", help="defines the number of leds for the strip [default: %default]")
            parser.add_option("-c", "--color_schema", dest="schema", help="defines the color schema of the strip: GRB, RGB, GRBW, RGBW [default: %default]")
        parser.add_option("-b", "--brightness", dest="bright", help="defines the brightness of the strip: 0 - 1.0 [default: %default]")
        if par is not "simple":
            parser.add_option("-m", "--color_mode", dest="mode", help="[1] all temp high, [2] all temp med, [3] all temp low, [4] all cloud, [5] all rain [default: %default]")

        # set defaults
        parser.set_defaults(port="D18", schema="GRBW", mode="1", len="1", bright="0.2")

        # process options
        (opts, args) = parser.parse_args(argv)
    except Exception as e:
        indent = len(program_name) * " "
        sys.stderr.write(program_name + ": " + repr(e) + "\n")
        sys.stderr.write(indent + "  for help use --help")
        return 2
    return opts