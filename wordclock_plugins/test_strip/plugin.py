import os
import time

try:
    from rpi_ws281x import Color
except:
    from WXcolors import Color

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
            wcd.setColorToAll(Color(0,0,0), includeMinutes=True)
            """Color wipe each LED to find the error"""
            for i in range(wcd.get_led_count()):
                wcd.setPixelColor(i, Color(255,0,0))
                wcd.show()
                time.sleep(0.1)
                if wci.waitForEvent(0.02) >= 0:
                    return
            time.sleep(10)
