import os


class plugin:
    """
    A class to switch off the LEDs temporarily.
    """

    def __init__(self, config):
        """
        Initializations for the startup of the current wordclock plugin
        """
        # Get plugin name (according to the folder, it is contained in)
        self.name = os.path.dirname(__file__).split('/')[-1]
        self.pretty_name = "LEDs off"
        self.description = "Disables the wordclock display."

    def run(self, wcd, wci):
        """
        Displays nothing until aborted by user interaction on pin button_return
        """
        wcd.resetDisplay()
        wcd.show()
        wci.waitForEvent()
