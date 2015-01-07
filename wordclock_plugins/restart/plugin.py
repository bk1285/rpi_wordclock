import os

class plugin:
    '''
    A class to restart the RPI
    '''

    def __init__(self, config):
        '''
        Initializations for the startup of the current wordclock plugin
        '''
        # Get plugin name (according to the folder, it is contained in)
        self.name = os.path.dirname(__file__).split('/')[-1]

    def run(self, wcd):
        '''
        Restart wordclock
        '''
        wcd.showText("Restarting...    ")
        os.system("shutdown now -r")
        return
