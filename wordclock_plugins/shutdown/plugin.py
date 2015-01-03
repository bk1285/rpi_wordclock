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
        self.name = 'shutdown'

    def run(self, wcd):
        '''
        Shutdown wordclock
        '''
        wcd.showText('Shutting down...    ')
        os.system('shutdown now -h')
        return
