'''
The interceptor is a WSIG server exposing a json REST endpoint. 
It is supposed to runs as an own thread and uses interprocess communication to receive the state of the Catatumbo controller, 
change the configuration and change the available modes, e.g. switching from weather forecast mode to share price mode.

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

@deffield    created: March 2020
@deffield    updated: Updated
'''
from flask import Flask, request
from flask_cors import cross_origin
from catatumbo.core.util.configurations import Configurations
import json5
from catatumbo.starter import CatatumboStart
from catatumbo.core.util.update_thread import fadeBrightness,\
    stopConcurrentThreads

server = Flask(__name__.split('.')[0])

"""
    start the server with listening to the defined port and hostname
    
    :param    host: the hostname to listen on. Defaults to ``'0.0.0.0'`` to listen externally as well.
    :type     host: str
    :param    port: the port of the webserver. Defaults to ``8080``
    :type     host: int
""" 
def startServer(host = "0.0.0.0", port = 8080):
    server.run(host, port)

########################################
#               SERVICES               #
########################################

@server.route('/catatumbo/config/adafruit/getBrightness', methods=['GET', 'POST'])
@cross_origin(origin='*', headers=['Content-Type'])
def getBrightness():
    # get starter and config instance for active mode and configuration information
    starter = CatatumboStart()
    config = Configurations()
        
    bMin = config.getAutoBrightnessMin()
    bCur = starter.getActivedInstance().getBrightness()
    bMax = config.getAutoBrightnessMax()
    
    ret = {Configurations.MIN_BRIGHTNESS : bMin,
            Configurations.CUR_BRIGHTNESS : bCur,
            Configurations.MAX_BRIGHTNESS : bMax}
    
    return json5.dumps(ret, allow_nan = True)

@server.route('/catatumbo/config/adafruit/setBrightness', methods=['POST'])
@cross_origin(origin='*', headers=['Content-Type'])
def setBrightness():
    # get starter and config instance for active mode and configuration information
    config = Configurations()
    instance = CatatumboStart().getActivedInstance()
    
    # Cataumbo app sends two values, maxBrightness will be always defined
    # minBrightness depends whether sunset fade mode is turned on
    data = json5.loads(request.data)
    bMin = data[Configurations.MIN_BRIGHTNESS]
    bMax = data[Configurations.MAX_BRIGHTNESS]
    
    
    if bMax is None:
        bMax = 0.7
    else:
        bMax = int(bMax) / 100
    
    # minBrightness may be None if sunset fading mode is turned off
    if bMin is not None:
        bMin = int(bMin) / 100 
        
    # stop concurrent fading threads
    stopConcurrentThreads()
    
    # temporarily indicate defined brightness value on led strip
    if bMax != config.getAutoBrightnessMax():
        # fade to defined max value
        __fadeBrightness(instance, 
                         bMax,
                         bMin is not None)
    elif bMin is not None and bMin != config.getAutoBrightnessMin():
        # fade to defined min value
        __fadeBrightness(instance, 
                         bMin,
                         bMin is not None)
    elif bMin is None:
        # no sunset/sunrise fading turned on
        # fade to defined max value
        __fadeBrightness(instance, 
                         bMax,
                         False)
    
    config.setAutoBrightnessMin(bMin)
    config.setAutoBrightnessMax(bMax)
    
    return json5.dumps("OK", allow_nan = True)
    
    
########################################
#          UTILITY METHOD              #
########################################

"""
    will fade from the current led brightness level to the changed value and then adapt fading level
    based on sunset/sunrise fading mode at the very end if turned on
    
    :param    instance: the instance of the controller class representing the active mode (weather forecast, share price, ...)
    :type     instance: class instance
    :param    stopLevel: destination brightness value, value between 1.0 and 0.0
    :type     stopLevel: float
    :param    finalDayTimeAdaption: set final brightness dependent on current time and sunset/sunrise fading configuration 
    :type     finalDayTimeAdaption: boolean
"""
def __fadeBrightness(instance, stop, finalDayTimeAdaption):
    fadeBrightness(controller_instance = instance, 
                   startLevel = instance.getBrightness(), 
                   stopLevel = stop,
                   waitTimeMainThread = 0.05,
                   newMainThread = False,
                   delta = 0.05, 
                   waitTimeSubThread = 0.05,
                   finalDayTimeAdaption = finalDayTimeAdaption)



