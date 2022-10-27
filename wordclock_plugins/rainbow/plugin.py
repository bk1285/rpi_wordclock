import os
import wordclock_tools.wordclock_colors as wcc

class plugin:
    """
    A class to display the current time (default mode).
    This default mode needs to be adapted to the hardware
    layout of the wordclock (the choosen stancil) and is
    the most essential time display mode of the wordclock.
    """

    def __init__(self, config):
        """
        Initializations for the startup of the current wordclock plugin
        """
        # Get plugin name (according to the folder, it is contained in)
        self.name = os.path.dirname(__file__).split('/')[-1]
        self.pretty_name = "Rainbow"
        self.description = "Displays a nice rainbow"

    def run(self, wcd, wci):
        """
        Displays time until aborted by user interaction on pin button_return
        """
        while True:
            """Draw rainbow that fades across all pixels at once."""
            for j in range(256 * 5):
                #for i in range(wcd.get_led_count()):
                for x in range(wcd.get_wca_width()):
                    for y in range(wcd.get_wca_height()):
                        #wcd.setPixelColor(i, self.wheel((i + j) & 255))
                        wcd.setColorBy2DCoordinates(x,y, self.wheel((x * y + j) & 255))
                wcd.show()
                if wci.waitForEvent(0.05) >= 0:
                    return

    def wheel(self, pos):
        """
        Generate rainbow colors across 0-255 positions.
        """
        if pos < 85:
            return wcc.Color(pos * 3, 255 - pos * 3, 0)
        elif pos < 170:
            pos -= 85
            return wcc.Color(255 - pos * 3, 0, pos * 3)
        else:
            pos -= 170
            return wcc.Color(0, pos * 3, 255 - pos * 3)
