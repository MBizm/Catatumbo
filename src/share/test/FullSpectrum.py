'''
Created on 19.10.2019

@author: MBizm
'''
import math
import numpy as np
import colorsys
from tkinter import Tk, Canvas, font, mainloop

MAX_VALUE = 2.5

def calculateHue(share, index):
    # define angle by position in grid defined by share and index value
    arcAlpha = math.atan2(index, -share)
    # math lib will return negative arc if in quadrant 3 or 4
    if(arcAlpha < 0):
        arcAlpha = 2 * math.pi + arcAlpha
    
    return np.degrees(arcAlpha)

def _from_rgb(rgb):
    #translates an rgb tuple of int to a tkinter friendly color code
    return "#%02x%02x%02x" % rgb

def normalizeValue(value):
    if(value > MAX_VALUE):
        value = MAX_VALUE
    elif(value < -MAX_VALUE):
        value = -MAX_VALUE
    return round(value, 1)

def calculatePriceDelta(value1, value2):
    delta = deltaValueAbs(value1, value2)
    return np.max((delta, abs(value1)))

def deltaValueAbs(value1, value2):
    return abs(deltaValue(value1, value2))

def deltaValue(value1, value2):
    return round(value1-value2, 1)


if __name__ == '__main__':
    print(calculateHue(2.5, 0)) #0
    print(calculateHue(0, 2.5)) #90 --> PI/2
    print(calculateHue(-2.5, 0)) #180 --> PI
    print(calculateHue(2.5, 2.5)) #45 --> PI/4
    print(calculateHue(-2.5, -2.5)) #225 --> 5/4PI OR -3/4PI
    print(calculateHue(0, -2.5)) #270 --> 3/2PI OR -PI/2
    print(calculateHue(2.5, -2.5)) #315 --> 7/4PI OR -PI/4
    
    #initialize canvas
    root = Tk()
    root.geometry("550x550")
    root.title("Share Price to Lead Index - Full Spectrum")
    canvas = Canvas(root, width=550, height=550)
    canvas.pack()
    
    f = font.Font(size=10, family="Times", slant="roman", weight="normal")
    
    for x in range(int(-10*MAX_VALUE), int(10*MAX_VALUE+1), 1):
        for y in range(int(10*MAX_VALUE), int(-10*MAX_VALUE-1), -1):   
            color = colorsys.hsv_to_rgb(1/360*calculateHue(normalizeValue(x), normalizeValue(y)),
                                        1/(2*MAX_VALUE)*calculatePriceDelta(x/10, y/10),
                                        1)
                    
            canvas.create_rectangle(10*deltaValueAbs(-25, x)+10,            #x1
                                    10*deltaValueAbs(25, y)+10,             #y1
                                    10*deltaValueAbs(-25, x) + 20,          #x2
                                    10*deltaValueAbs(25, y) + 20,           #y2
                                    fill=_from_rgb((int(255*color[0]),
                                                    int(255*color[1]),
                                                    int(255*color[2]))))
            if((abs(x) == 25 and y == 0) or (abs(y) == 25 and x == 0)):
                print(str(x) + ":" + str(y) + " - ", 
                      (1/360*calculateHue(normalizeValue(x), normalizeValue(y)), 1/(2*MAX_VALUE)*deltaValueAbs(x/10, y/10), 1),
                      color)
            
            
    for x in range(int(-10*MAX_VALUE), int(10*MAX_VALUE+1), 1):
        for y in range(int(10*MAX_VALUE), int(-10*MAX_VALUE-1), -1):
            text = str(deltaValue(x/10, y/10))  
            if(x % 5 == 0 and y % 5 == 0):
                canvas.create_text(10*deltaValueAbs(-25, x)+f.measure(text),    #x
                                   10*deltaValueAbs(25, y) + 15,                #y
                                   text=text,
                                   fill = 'black',
                                   font = f)
        
    mainloop()
                
                
                
    