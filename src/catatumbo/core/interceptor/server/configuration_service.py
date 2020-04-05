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

# allow CORS request from  browser, no IP restriction
# browser will send OPTIONS header before sending CORS request
@server.route('/catatumbo/config/test', methods=['GET', 'POST'])
@cross_origin(origin='*', headers=['Content-Type'])
def get_test():
    config = Configurations()
    ret = [{"id": 1, "text" : "Hello"},
           {"id": 2, "text" : "World!"},
           {"id": 3, "valueConfig" : config.getAutoBrightnessMax()},
           {"id": 4, "valueFrontend" : request.args.get('value', default = -1, type = int)}]
    config.writeConfiguration()
    return json5.dumps(ret)

@server.route('/catatumbo/config/adafruit/getBrightness', methods=['GET', 'POST'])
@cross_origin(origin='*', headers=['Content-Type'])
def getBrightness():
    # gert starter instance for active mode information
    starter = CatatumboStart()
    config = Configurations()
    
    print(starter.getActivedInstance())
    
    bMin = config.getAutoBrightnessMin()
    bCur = starter.getActivedInstance().getBrightness()
    bMax = config.getAutoBrightnessMax()
    
    # check whether static brightness or adaptive brightness is configured
    if bMin is None or bMax is None:
        # static brightness only value 'Brightness' is defined in configuration file
        bMin = None
        bMax = config.getBrightness()    
    
    ret = [{Configurations.MIN_BRIGHTNESS : bMin,
            Configurations.CUR_BRIGHTNESS : bCur,
            Configurations.MAX_BRIGHTNESS : bMax}]
    
    return json5.dumps(ret, allow_nan = True)






