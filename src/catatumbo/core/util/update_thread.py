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



activeMainThread = None
activeFadingThread = None


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
    global activeMainThread
    
    # stop concurrent fading threads
    stopConcurrentThreads()
    
    # next run - update every half an hour
    activeMainThread = Timer(controller_instance.UpdateFrequency, queueUpdate, (controller_instance, color_mode))
    activeMainThread.start()
    
    #the tasks...
    # update color scale
    controller_instance.fillStrips(color_mode)
    # adapt brightness
    controller_instance.adaptBrightnessToLocalDaytime()
    
"""
    will stop and reset threads that are already running
"""
def stopConcurrentThreads():
    global activeMainThread
    global activeFadingThread
    
    print("#### " + str(datetime.now()) + " Stopping concurrent threads")
    
    # to be safe... stop concurrent threads
    # TODO only pause main thread if we suspend forecast mode
    #if activeMainThread is not None:
    #    activeMainThread.cancel()
    if activeFadingThread is not None:
        activeFadingThread.cancel()
        activeFadingThread = None
    
"""
    utility method for separate thread that fades the brightness level in increasing velocity
    from startLevel brightness to stopLevel brightness.
    
    Looking at the most distant values of startLevel = 1.0 and stopLevel = 0.0
    and a initial waitTime of 10min + intermediate adaption time of 6 sec (decrease of 0.01 by intermediate step):
        iteration duration (min)    10    5    2.5    1.25    0.625    0.3125    0.15625
        brightness (after itera.)   1.0   0.5  0.25   0.125   0.0625   0.03125   0.015625
        time interm. trans. (min)   5     2.5  1.25   0.625   0.3125   0.15625
    
    :param    controller_instance: the instance of the controller class representing the active mode (weather forecast, share price, ...)
    :type     controller_instance: class instance
    :param    startLevel: initial brightness value, value between 1.0 and 0.0
    :type     startLevel: float
    :param    stopLevel: destination brightness value, value between 1.0 and 0.0
    :type     stopLevel: float
    :param    waitTimeMainThread: seconds to wait till next iteration of larger cycles
    :type     waitTimeMainThread: int
    :param    newMainThread: defines whether this is a main iteration with decreasing step size and time or an intermediate iteration with constant time and step size
                                if true, it will set up a next iteration of the main thread
    :type     newMainThread: boolean
    :param    delta: subtraction/addition value for brightness adaption, used in intermediate iterations
    :type     delta: float
    :param    waitTimeSubThread: seconds to wait till next iteration of sub cycles
    :type     waitTimeSubThread: int
    :param    finalDayTimeAdaption: special case - set final brightness dependent on current time and sunset/sunrise fading configuration 
    :type     finalDayTimeAdaption: boolean
"""
def fadeBrightness(controller_instance, startLevel, stopLevel, waitTimeMainThread, newMainThread, delta = 0, waitTimeSubThread = 6, finalDayTimeAdaption = False):
    intermediateStepSize = 0.01
    global activeFadingThread
    
    # define stop criteria
    if abs(startLevel - stopLevel) < intermediateStepSize:
        # stop main iteration
        return
    if startLevel > stopLevel and startLevel + delta < stopLevel:
        # assure we reach the final value
        controller_instance.setBrightness(stopLevel)
        
        # check if brightness shall be faded based on local sunrise/sunset fading configuration
        if finalDayTimeAdaption:
            controller_instance.adaptBrightnessToLocalDaytime()
        
        # stop intermediate iteration
        return
    if startLevel < stopLevel and startLevel + delta > stopLevel:
        # assure we reach the final value
        controller_instance.setBrightness(stopLevel)
        
        # check if brightness shall be faded based on local sunrise/sunset fading configuration
        if finalDayTimeAdaption:
            controller_instance.adaptBrightnessToLocalDaytime()
        
        # stop intermediate iteration
        return
    
    # set current brightness
    controller_instance.setBrightness(round(startLevel + delta, 2))
    #print("{0} - current brightness: {1}".format(datetime.now().strftime("%A, %d. %B %Y %I:%M%p"), round(startLevel + delta, 2)))
    
    # start intermediate decrease with constant 0.01 step size every 6 seconds
    if startLevel > stopLevel:
        # fading out - set new lower boundary for intermediate iteration started by main iteration
        activeFadingThread = Timer(waitTimeSubThread, 
                              fadeBrightness,
                              # parameter list
                              (controller_instance, 
                               startLevel,
                               stopLevel + ((startLevel - stopLevel) / 2) if newMainThread == True else stopLevel,
                               waitTimeSubThread,
                               False,
                               delta - intermediateStepSize,
                               waitTimeSubThread,
                               finalDayTimeAdaption)
                              )
        activeFadingThread.start()
        # for testing purpose without threading
        #self.fadeBrightness(startLevel, stopLevel + ((startLevel - stopLevel) / 2) if newMainThread == True else stopLevel, 
        #                    6, False, delta - intermediateStepSize)
    elif startLevel < stopLevel:
        # fading in - set new upper boundary for intermediate iteration started by main iteration
        activeFadingThread = Timer(waitTimeSubThread, 
                              fadeBrightness,
                              # parameter list
                              (controller_instance, 
                               startLevel,
                               stopLevel - ((stopLevel - startLevel) / 2) if newMainThread == True else stopLevel,
                               waitTimeSubThread,
                               False,
                               delta + intermediateStepSize,
                               waitTimeSubThread,
                               finalDayTimeAdaption)
                              )
        activeFadingThread.start()          
        # for testing purpose without threading
        #controller_instance.fadeBrightness(startLevel, stopLevel - ((stopLevel - startLevel) / 2) if newMainThread == True else stopLevel,
        #                    6, False, delta + intermediateStepSize)
    
    # start new main iteration for adjustable iteration
    if newMainThread == True:
        if startLevel > stopLevel:
            # fading out - decrease brightness by half the distance between current startLevel and stopLevel and cut time by half
            activeMainThread = Timer(waitTimeMainThread, 
                                  fadeBrightness,
                                  # parameter list
                                  (controller_instance, 
                                   startLevel - ((startLevel - stopLevel) / 2),
                                   stopLevel,
                                   waitTimeMainThread / 2,
                                   True,
                                   0,
                                   waitTimeSubThread,
                                   finalDayTimeAdaption)
                                  )
            activeMainThread.start()
            # for testing purpose without threading
            #controller_instance.fadeBrightness(startLevel - ((startLevel - stopLevel) / 2), stopLevel, waitTimeMainThread / 2, True)
        elif startLevel < stopLevel:
            # fading in - decrease brightness by half the distance between current startLevel and stopLevel and cut time by half
            activeMainThread = Timer(waitTimeMainThread, 
                                  fadeBrightness,
                                  # parameter list
                                  (controller_instance, 
                                   startLevel + ((stopLevel - startLevel) / 2),
                                   stopLevel,
                                   waitTimeMainThread / 2,
                                   0,
                                   waitTimeSubThread,
                                   finalDayTimeAdaption)
                                  )
            activeMainThread.start()
            # for testing purpose without threading
            #np.fadeBrightness(startLevel + ((stopLevel - startLevel) / 2), stopLevel, waitTime / 2, True)
