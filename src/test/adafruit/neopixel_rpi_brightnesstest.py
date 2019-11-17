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

def init():
    global PIXEL_PIN
    global NUM_PIXELS
    global CYCLE_TIME
    global ORDER
    global sampleboard
    
    if(ORDER == neopixel.GRBW or ORDER == neopixel.RGBW):
        # TODO if RGBW/GRBW
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
    
    global sectionsize 
    sectionsize = int(NUM_PIXELS / len(sampleboard))
    # TODO check if re-adjustment is required
    # adjust number of addressable pixels depending on section size - leave remaining pixels blank
    global NUM_PIXELS 
    NUM_PIXELS = sectionsize * len(sampleboard)
    

def setBrightness(brightness, delay):
    pixels.brightness = brightness
    pixels.show()
    print('brightness level: ' + str(brightness) + ' delay: ' + str(delay))
    time.sleep(delay)


if __name__ == '__main__':
        
    sampleboard = (())
    sectionsize = 0
    
    init()
    
    pixels = neopixel.NeoPixel(PIXEL_PIN, NUM_PIXELS, brightness=0.2, auto_write=False,
                               pixel_order=ORDER)

    print('addressable pixels: ' + str(NUM_PIXELS) + ' section size: ' + str(sectionsize))
    
    # TODO check ranges -1 ... +1
    for i in range(NUM_PIXELS-1):
        #print('i: ' + str(i) + ' section: ' + str(int(i / sectionsize)))
        pixels[i+1] = sampleboard[int(i / sectionsize)]
    
    pixels.show()
    
    n = 0
    
    while True:
        for direction in range (0, 2, 1):
            for i in range(100, 9, -1):
                
                if i == 100 and direction == 1:
                    for i in range(95, 0, -1):
                        setBrightness(abs(100 * direction - i) / 1000,
                                      CYCLE_TIME / (280 * 2))
                        n = n + 1
                
                setBrightness(abs(100 * direction - i) / 100,
                              CYCLE_TIME / (280 * 1))
                n = n + 1
                
                if i == 10 and direction == 0:
                    for i in range(95, 0, -1):
                        setBrightness(abs(100 * direction - i) / 1000,
                                      CYCLE_TIME / (280 * 2))
                        n = n + 1