# Authored by Markus E.

import os
import wordclock_tools.wordclock_colors as wcc
import random


class plugin:
    """
    A class to display matrix rain
    """

    def __init__(self, config):
        """
        Initializations for the startup of the current wordclock plugin
        """
        # Get plugin name (according to the folder, it is contained in)
        self.name = os.path.dirname(__file__).split('/')[-1]
        self.bg_color = wcc.BLACK;
        self.threshold = 0.9

        self.pretty_name = "Matrix"
        self.description = "Why do my eyes hurt?"

        # Colors from black to green (and a bit gray-ish)
        self.colors = []
        for i in range(0, 8):
            self.colors.append(wcc.Color(0, int(255.0 / 10 * i), 0))
        self.colors.append(wcc.Color(50, 204, 30))
        self.colors.append(wcc.Color(50, 230, 30))
        self.colors.append(wcc.Color(80, 255, 60))

    def run(self, wcd, wci):
        """
        Displays rain until aborted by user interaction on pin button_return
        """
        # initialize rain start: set to end coordinate
        rain = [20 for _ in range(0, 11)]
        while True:
            # Set background color
            wcd.setColorToAll(self.bg_color, includeMinutes=True)

            for x, y in enumerate(rain):
                if y == 20:
                    # reset y coordinate randomly
                    if random.random() > self.threshold:
                        rain[x] = 0
                else:
                    # simple alpha blending using our predefined colors
                    y0 = max(y - 10, 0)
                    y1 = min(9, y);
                    ci = y0 - (y - 10);
                    for yi, yn in enumerate(range(y0, y1 + 1)):
                        color = self.colors[ci + yi]
                        wcd.setColorBy2DCoordinates(x, yn, color)
                    # advance y coordinate
                    rain[x] = y + 1
            wcd.show()
            # input handling
            event = wci.waitForEvent(0.1)
            if event == wci.EVENT_BUTTON_RETURN \
                    or event == wci.EVENT_EXIT_PLUGIN \
                    or event == wci.EVENT_NEXT_PLUGIN_REQUESTED:
                return
            elif event == wci.EVENT_BUTTON_LEFT:
                self.threshold = min(0.95, self.threshold + 0.05)
            elif event == wci.EVENT_BUTTON_RIGHT:
                self.threshold = max(0.7, self.threshold - 0.05)
