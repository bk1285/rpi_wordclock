import datetime
import os
import time
import wordclock_tools.wordclock_colors as wcc

class plugin:
    '''
    A class to display a nice rainbow
    '''
    def __init__(self, config):
        '''
        Initializations for the startup of the current wordclock plugin
        '''
        # Get plugin name (according to the folder, it is contained in)
        self.name = os.path.dirname(__file__).split('/')[-1]
        self.pretty_name = "Rainbow"
        self.description = "Displays a nice rainbow"

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
                event = wci.waitForEvent(0.1)
                if event == wci.EVENT_BUTTON_RETURN or event == wci.EVENT_EXIT_PLUGIN:
                    return                
                time.sleep(20/1000.0)

    def wheel(self, pos):
        """Generate rainbow colors across 0-255 positions."""
        if pos < 85:
            return wcc.Color(pos * 3, 255 - pos * 3, 0)
        elif pos < 170:
            pos -= 85
            return wcc.Color(255 - pos * 3, 0, pos * 3)
        else:
            pos -= 170
            return wcc.Color(0, pos * 3, 255 - pos * 3)

