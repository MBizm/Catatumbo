'''
Created on 19.10.2019

@author: MBizm
'''
import math
import numpy as np

def calculateHue(share, index):
    # define angle by position in grid defined by share and index value
    arcAlpha = math.atan2(index, share)
    # math lib will return negative arc if in quadrant 3 or 4
    if(arcAlpha < 0):
        arcAlpha = 2 * math.pi + arcAlpha
    
    return np.degrees(arcAlpha)

if __name__ == '__main__':
    print(calculateHue(2.5, 0)) #0
    print(calculateHue(0, 2.5)) #90 --> PI/2
    print(calculateHue(-2.5, 0)) #180 --> PI
    print(calculateHue(2.5, 2.5)) #45 --> PI/4
    print(calculateHue(-2.5, -2.5)) #225 --> 5/4PI OR -3/4PI
    print(calculateHue(0, -2.5)) #270 --> 3/2PI OR -PI/2
    print(calculateHue(2.5, -2.5)) #315 --> 7/4PI OR -PI/4