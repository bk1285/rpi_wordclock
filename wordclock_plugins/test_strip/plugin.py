import os
import time
import wordclock_tools.wordclock_colors as wcc

class plugin:
    """
    A class to test the led strip for errors. Color wipe will stop at the error LED
    """

    def __init__(self, config):
        """
        Initializations for the startup of the current wordclock plugin
        """
        # Get plugin name (according to the folder, it is contained in)
        self.name = os.path.dirname(__file__).split('/')[-1]
        self.pretty_name = "Test-Strip"
        self.description = "Test the strip for errors"

    def run(self, wcd, wci):
        """
        Displays time until aborted by user interaction on pin button_return
        """
        while True:
            """Reset all LEDs"""
            wcd.resetDisplay()
            """Color wipe each LED to find the error"""
            for x in range(wcd.get_wca_width()):
                for y in range(wcd.get_wca_height()):
                    #wcd.setPixelColor(i, self.wheel((i + j) & 255))
                    wcd.setColorBy2DCoordinates(x,y, wcc.Color(255, 0, 0))
                    wcd.show()
                    time.sleep(0.05)
                    if wci.waitForEvent(0.02) >= 0:
                        return
            for x in range(0,4):
                wcd.setColorByMinute(x, wcc.Color(255, 0, 0))
                wcd.show()
                time.sleep(0.05)
                if wci.waitForEvent(0.02) >= 0:
                    return
            time.sleep(5)
