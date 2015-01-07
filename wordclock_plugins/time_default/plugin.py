import datetime
import os
import time
import time_german
import wordclock_tools.buttons as wcb
import wordclock_tools.wordclock_colors as wcc

class plugin:
    '''
    A class to display the current time (default mode).
    This default mode needs to be adapted to the hardware
    layout of the wordclock (the choosen stancil) and is
    the most essential time display mode of the wordclock.
    '''

    def __init__(self, config):
        '''
        Initializations for the startup of the current wordclock plugin
        '''
        # Get plugin name (according to the folder, it is contained in)
        self.name = os.path.dirname(__file__).split('/')[-1]

        # Choose language
        language = config.get('plugin_time_default', 'language')
        if language == 'german':
            self.taw = time_german.time_german()
        else:
            print('Could not detect language: ' + language + '.')
            print('Choosing default: german')
            self.taw = time_german.time_german()

        self.bg_color_index     = 0 # default background color: black
        self.word_color_index   = 2 # default word color: warm white
        self.minute_color_index = 2 # default minute color: warm white

    def run(self, wcd):
        '''
        Displays time until aborted by user interaction on pin button_return
        '''
        while True:
            # Set background color
            wcd.setColorToAll(wcc.colors[self.bg_color_index], includeMinutes=True)
            # Set current time
            now = datetime.datetime.now()
            # Returns indices, which represent the current time, when beeing illuminated
            taw_indices = self.taw.get_time(now)
            #TODO: Improve rendering of time during while-loop: Render array only once per 5 minutes...
            wcd.wcl.setColorBy1DCoordinates(wcd.strip, taw_indices, wcc.colors[self.word_color_index])
            wcd.setMinutes(now, wcc.colors[self.minute_color_index])
            wcd.show()
            event = wcd.waitSecondsForEvent([wcb.button_left, wcb.button_return, wcb.button_right], 10)
            # Switch display color, if button_left is pressed
            if (event == wcb.button_left):
                self.word_color_index +=1
                if self.word_color_index == wcc.num_of_colors:
                    self.word_color_index = 0
                self.minute_color_index = self.word_color_index
                time.sleep(0.2)
            # Return to main menu, if button_return is pressed
            if (event == wcb.button_return):
                return
