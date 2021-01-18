import os
import time


class plugin:
    """
    A class to shutdown the RPI

    ..note:: This should be done before disconnecting the wordclock from its power supply.
    """

    def __init__(self, config):
        """
        Initializations for the startup of the current wordclock plugin
        """
        # Get plugin name (according to the folder, it is contained in)
        self.name = os.path.dirname(__file__).split('/')[-1]
        self.pretty_name = "Shutdown"
        self.description = "Switches the wordclock off"

    def run(self, wcd, wci):
        """
        Shutdown wordclock
        """
        wcd.showText('Shutting down...    ')
        wcd.showIcon(plugin=self.name, iconName='logo')
        os.system('shutdown now -h')
        time.sleep(10)
        return
