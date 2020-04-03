'''
The interceptor is a WSIG server exposing a json REST endpoint. 
It runs as an own instance and uses interprocess communication to receive the state of the Catatumbo controller, 
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
from flask import Flask, json
from flask_cors import cross_origin
from adafruit.core.util.configurations import Configurations

server = Flask(__name__)

# allow CORS request from  browser, no IP restriction
# browser will send OPTIONS header before sending CORS request
@server.route('/interceptor/test', methods=['GET', 'POST'])
@cross_origin(origin='localhost', headers=['Content-Type'])
def get_test():
    config = Configurations()
    ret = [{"id": 1, "text" : "Hello"},
           {"id": 2, "text" : "World!"},
           {"id": 3, "text" : config.getAutoBrightnessMax()}]
    config.writeConfiguration()
    return json.dumps(ret)

if __name__ == '__main__':
    server.run(host="0.0.0.0", port=8080)