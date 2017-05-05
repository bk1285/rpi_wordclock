import os
import time
import wordclock_tools.wordclock_colors as wcc

class plugin:
    '''
    A class to switch off the LEDs temporarily.
    '''
    def __init__(self, config):
        '''
        Initializations for the startup of the current wordclock plugin
        '''
        # Get plugin name (according to the folder, it is contained in)
        self.name = os.path.dirname(__file__).split('/')[-1]

    def run(self, wcd, wci):
        '''
        Displays nothing until aborted by user interaction on pin button_return
        '''
        emptied = False
        while True:
            """Draw nothing."""
            if not emptied:
                for i in range(114):
                    wcd.setPixelColor(i, wcc.Color(0, 0, 0))
                wcd.show()
                emptied = True
            event = wci.waitForEvent(0.1)
            if event == wci.EVENT_BUTTON_RETURN or event == wci.EVENT_EXIT_PLUGIN:            
                return
            time.sleep(20/1000.0)