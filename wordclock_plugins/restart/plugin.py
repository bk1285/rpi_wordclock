import os

class plugin:
    '''
    A class to restart the RPI
    '''

    def __init__(self, config):
        '''
        Initializations for the startup of the current wordclock plugin
        '''
        self.name = 'restart'

    def run(self, wcd):
        '''
        Restart wordclock
        '''
        wcd.showText("Restarting...    ")
        os.system("shutdown now -r")
        return
