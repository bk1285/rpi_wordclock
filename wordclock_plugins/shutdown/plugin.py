import os

class plugin:
    '''
    A class to shutdown the RPI

    ..note:: This should be done before disconnecting the wordclock from its power supply.
    '''

    def __init__(self, config):
        '''
        Initializations for the startup of the current wordclock plugin
        '''
        # Get plugin name (according to the folder, it is contained in)
        self.name = os.path.dirname(__file__).split('/')[-1]

    def run(self, wcd):
        '''
        Shutdown wordclock
        '''
        wcd.showText('Shutting down...    ')
        os.system('shutdown now -h')
        return
