# Simple test of brightness change for NeoPixels on Raspberry Pi
import time 
import board
import neopixel

# Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18
# NeoPixels must be connected to D10, D12, D18 or D21 to work.
PIXEL_PIN = board.D18

# The number of NeoPixels
NUM_PIXELS = 60

# defines the time in seconds that it will take to from an illuminated to faded state
# calculation will be based on 190 individual steps for dimming from which 100 are twice the speed - step divider 280
CYCLE_TIME = 15

# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.GRBW

# Only of relevance for neopixel.GRBW and neopixel.RGBW
# will activate the white LED with 1/4th intensity for all colors
WHITE_LED_ON = True

def init():
    global PIXEL_PIN
    global NUM_PIXELS
    global CYCLE_TIME
    global ORDER
    global sampleboard
    
    if(ORDER == neopixel.GRBW or ORDER == neopixel.RGBW):
        if WHITE_LED_ON:
            # color space of tertiary colors with white LED support, starting with full white (all LEDs) and ending with white LED section
            sampleboard = ((255,255,255,63),
                           (255,0,0,63), 
                           (255,127,0,63),
                           (255,255,0,63),
                           (127,255,0,63), 
                           (0,255,0,63),
                           (0,255,127,63),
                           (0,255,255,63),
                           (0,127,255,63),
                           (0,0,255,63),
                           (127,0,255,63),
                           (255,0,255,63),
                           (255,0,127,63), 
                           (0,0,0,63))
        else:
            # color space of tertiary colors, starting with full white (all LEDs) and ending with white LED section
            sampleboard = ((255,255,255,255),
                           (255,0,0,0), 
                           (255,127,0,0),
                           (255,255,0,0),
                           (127,255,0,0), 
                           (0,255,0,0),
                           (0,255,127,0),
                           (0,255,255,0),
                           (0,127,255,0),
                           (0,0,255,0),
                           (127,0,255,0),
                           (255,0,255,0),
                           (255,0,127,0), 
                           (0,0,0,255))
    elif(ORDER == neopixel.GRB or ORDER == neopixel.RGB):
        # color space of tertiary colors, starting with full white (all LEDs)
        sampleboard = ((255,255,255),
                       (255,0,0), 
                       (255,127,0),
                       (255,255,0),
                       (127,255,0), 
                       (0,255,0),
                       (0,255,127),
                       (0,255,255),
                       (0,127,255),
                       (0,0,255),
                       (127,0,255),
                       (255,0,255),
                       (255,0,127))
    
    global sectionsize 
    sectionsize = int(NUM_PIXELS / len(sampleboard))
    

def setBrightness(brightness, delay):
    pixels.brightness = brightness
    pixels.show()
    #print('brightness level: ' + str(brightness))
    time.sleep(delay)


if __name__ == '__main__':
        
    sampleboard = (())
    sectionsize = 0
    
    init()
    
    pixels = neopixel.NeoPixel(PIXEL_PIN, NUM_PIXELS, brightness=0.2, auto_write=False,
                               pixel_order=ORDER)

    #print('addressable pixels: ' + str(NUM_PIXELS) + ' section size: ' + str(sectionsize))
    
    # preset pixel colors
    for i in range(NUM_PIXELS-1):
        # fill up remaining pixels
        if(int(i / sectionsize) >= len(sampleboard)):
            pixels[i+1] = sampleboard[len(sampleboard) - 1] 
        # preset pixel colors according to color space set  
        else:  
            #print('i: ' + str(i) + ' section: ' + str(int(i / sectionsize)))
            pixels[i+1] = sampleboard[int(i / sectionsize)]
    pixels.show()
    
    while True:
        # direction = 0 - fading from illuminated state, direction = 1 - illuminating
        for direction in range (0, 2, 1):
            # iterating brightness level in the range of 1.0 and 0.1, step size 0.01
            for i in range(100, 0, -1):
                
                # iterating brightness level in the range of 0.0 and 0.099, step size 0.001
                if i == 100 and direction == 1:
                    for j in range(99, 0, -1):
                        setBrightness(abs(100 * direction - j) / 1000,
                                      CYCLE_TIME / (2 * (90 + 50)))
                
                # iterating brightness level in the range of 1.0 and 0.1, step size 0.01
                # skip the range between 0.1 and 0
                if (direction == 0 and i >= 10) or (direction == 1 and i <= 90):
                    setBrightness(abs(100 * direction - i) / 100,
                                  CYCLE_TIME / (90 + 50))
                
                # iterating brightness level in the range of 0.099 and 0.0, step size 0.001
                if i == 10 and direction == 0:
                    for j in range(99, 0, -1):
                        setBrightness(abs(100 * direction - j) / 1000,
                                      CYCLE_TIME / (2 * (90 + 50)))