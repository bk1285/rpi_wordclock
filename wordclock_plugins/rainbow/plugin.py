import datetime
import os
import time
import RPi.GPIO as GPIO
from neopixel import *

class plugin:
    '''
    A class to display the current time (default mode).
    This default mode needs to be adapted to the hardware
    layout of the wordclock (the choosen stancil) and is
    the most essential time display mode of the wordclock.
    '''

    def __init__(self, config):
        '''
        Initializations for the startup of the current wordclock plugin
        '''
        # Get plugin name (according to the folder, it is contained in)
        self.name = os.path.dirname(__file__).split('/')[-1]

    def run(self, wcd, wci):
        '''
        Displays time until aborted by user interaction on pin button_return
        '''
        while True:
            """Draw rainbow that fades across all pixels at once."""
            for j in range(256*5):
                for i in range(114):
                    wcd.setPixelColor(i, self.wheel((i+j) & 255))
                wcd.show()
                if not GPIO.input(22) or GPIO.input(8):
                    print('Pin ' + str(22) + ' pressed.')
                    return
                time.sleep(20/1000.0)

    def wheel(self, pos):
        """Generate rainbow colors across 0-255 positions."""
        if pos < 85:
            return Color(pos * 3, 255 - pos * 3, 0)
        elif pos < 170:
            pos -= 85
            return Color(255 - pos * 3, 0, pos * 3)
        else:
            pos -= 170
            return Color(0, pos * 3, 255 - pos * 3)   

