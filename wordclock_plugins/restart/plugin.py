import os
import time


class plugin:
    """
    A class to restart the RPI
    """

    def __init__(self, config):
        """
        Initializations for the startup of the current wordclock plugin
        """
        # Get plugin name (according to the folder, it is contained in)
        self.name = os.path.dirname(__file__).split('/')[-1]
        self.pretty_name = "Restart"
        self.description = "Restarts the wordclock"

    def run(self, wcd, wci):
        """
        Restart wordclock
        """
        wcd.showText("Restarting...    ")
        wcd.showIcon(plugin=self.name, iconName='logo')
        os.system("shutdown now -r")
        time.sleep(10)
        return
