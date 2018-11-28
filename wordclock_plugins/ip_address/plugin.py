import os
import netifaces


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
        self.interface = config.get('plugin_' + self.name, 'interface')
        self.pretty_name = "IP address"
        self.description = "Displays the wordclocks current IP."

    def run(self, wcd, wci):
        """
        Show ip of the wordclock
        """
        try:
            ip = netifaces.ifaddresses(self.interface)[2][0]['addr']
            wcd.showText(ip)
        except:
            wcd.showText('No ip.')
        return
