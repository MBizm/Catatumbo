'''
Central threading utility for brightness and 

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

@deffield    created: April 2020
@deffield    updated: Updated
'''

from threading import Timer
from datetime import datetime



activeThread = None


########################################
#        THREAD UTILITY METHOD         #
########################################
"""
    regular thread update method for updating forecast values
    
    :param    controller_instance: the instance of the controller class representing the active mode (weather forecast, share price, ...)
    :type     controller_instance: class instance
    :param    color_mode: selected forecast mode; see MODE_TODAY, MODE_TOMORROW_DAYTIME, MODE_ALL
    :type     color_mode: str
"""      
def queueUpdate(controller_instance, color_mode):
    global activeThread
    
    # to be safe... stop concurrent threads
    if activeThread is not None:
        activeThread.stop()
    
    # next run - update every half an hour
    activeThread = Timer(controller_instance.UpdateFrequency, queueUpdate, (controller_instance, color_mode))
    activeThread.start()
    
    #the tasks...
    # update color scale
    controller_instance.fillStrips(color_mode)
    # adapt brightness
    controller_instance.adaptBrightnessToLocalDaytime()
    
"""
    utility method for separate thread that fades the brightness level in increasing velocity
    from startLevel brightness to stopLevel brightness.
    
    Looking at the most distant values of startLevel = 1.0 and stopLevel = 0.0
    and a initial waitTime of 10min + intermediate adaption time of 6 sec (decrease of 0.01 by intermediate step):
        iteration duration (min)    10    5    2.5    1.25    0.625    0.3125    0.15625
        brightness (after itera.)   1.0   0.5  0.25   0.125   0.0625   0.03125   0.015625
        time interm. trans. (min)   5     2.5  1.25   0.625   0.3125   0.15625
    
    :param    startLevel: initial brightness value, value between 1.0 and 0.0
    :type     startLevel: float
    :param    stopLevel: destination brightness value, value between 1.0 and 0.0
    :type     stopLevel: float
    :param    waitTime: seconds to wait till next iteration
    :type     waitTime: int
    :param    newMainThread: defines whether this is a main iteration with decreasing step size and time or an intermediate iteration with constant time and step size
                                if true, it will set up a next iteration of the main thread
    :type     newMainThread: boolean
    :param    delta: subtraction/addition value for brightness adaption, used in intermediate iterations
    :type     delta: float
"""
def fadeBrightness(np, startLevel, stopLevel, waitTime, newMainThread, delta = 0):
    intermediateStepSize = 0.01
    
    # define stop criteria
    if abs(startLevel - stopLevel) < intermediateStepSize:
        # stop main iteration
        return
    if startLevel > stopLevel and startLevel + delta < stopLevel:
        # stop intermediate iteration
        return
    if startLevel < stopLevel and startLevel + delta > stopLevel:
        # stop intermediate iteration
        return
    
    # TODO test
    print("{0} - current brightness: {1}".format(datetime.now().strftime("%A, %d. %B %Y %I:%M%p"), startLevel + delta))
    # set current brightness
    np.setBrightness(startLevel + delta)
    
    # start intermediate decrease with constant 0.01 step size every 6 seconds
    if startLevel > stopLevel:
        # fading out - set new lower boundary for intermediate iteration started by main iteration
        Timer(6, 
              fadeBrightness,
              # parameter list
              (np, 
               startLevel,
               stopLevel + ((startLevel - stopLevel) / 2) if newMainThread == True else stopLevel,
               6,
               False,
               delta - intermediateStepSize)
              ).start()
        # for testing purpose without threading
        #self.fadeBrightness(startLevel, stopLevel + ((startLevel - stopLevel) / 2) if newMainThread == True else stopLevel, 
        #                    6, False, delta - intermediateStepSize)
    elif startLevel < stopLevel:
        # fading in - set new upper boundary for intermediate iteration started by main iteration
        Timer(6, 
              fadeBrightness,
              # parameter list
              (np, 
               startLevel,
               stopLevel - ((stopLevel - startLevel) / 2) if newMainThread == True else stopLevel,
               6,
               False,
               delta + intermediateStepSize)
              ).start()          
        # for testing purpose without threading
        #np.fadeBrightness(startLevel, stopLevel - ((stopLevel - startLevel) / 2) if newMainThread == True else stopLevel,
        #                    6, False, delta + intermediateStepSize)
    
    # start new main iteration for adjustable iteration
    if newMainThread == True:
        if startLevel > stopLevel:
            # fading out - decrease brightness by half the distance between current startLevel and stopLevel and cut time by half
            Timer(waitTime, 
                  fadeBrightness,
                  # parameter list
                  (np, 
                   startLevel - ((startLevel - stopLevel) / 2),
                   stopLevel,
                   waitTime / 2,
                   True)
                  ).start()
            # for testing purpose without threading
            #np.fadeBrightness(startLevel - ((startLevel - stopLevel) / 2), stopLevel, waitTime / 2, True)
        elif startLevel < stopLevel:
            # fading in - decrease brightness by half the distance between current startLevel and stopLevel and cut time by half
            Timer(waitTime, 
                  fadeBrightness,
                  # parameter list
                  (np, 
                   startLevel + ((stopLevel - startLevel) / 2),
                   stopLevel,
                   waitTime / 2,
                   True)
                  ).start()
            # for testing purpose without threading
            #np.fadeBrightness(startLevel + ((stopLevel - startLevel) / 2), stopLevel, waitTime / 2, True)
