import datetime
import os
import time
import time_german
import time_swabian
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
        language = config.get('plugin_' + self.name, 'language')
        if language == 'german':
            self.taw = time_german.time_german()
        elif language == 'swabian':
            self.taw = time_swabian.time_swabian()
        else:
            print('Could not detect language: ' + language + '.')
            print('Choosing default: german')
            self.taw = time_german.time_german()

        self.bg_color     = wcc.BLACK  # default background color
        self.word_color   = wcc.WWHITE # default word color
        self.minute_color = wcc.WWHITE # default minute color

        # Other color modes...
        self.color_modes = \
               [[wcc.BLACK, wcc.WWHITE, wcc.WWHITE],
                [wcc.BLACK, wcc.WHITE, wcc.WHITE],
                [wcc.BLACK, wcc.PINK, wcc.GREEN],
                [wcc.BLACK, wcc.RED, wcc.YELLOW],
                [wcc.BLACK, wcc.BLUE, wcc.RED],
                [wcc.BLACK, wcc.RED, wcc.BLUE],
                [wcc.YELLOW, wcc.RED, wcc.BLUE],
                [wcc.RED, wcc.BLUE, wcc.BLUE],
                [wcc.RED, wcc.WHITE, wcc.WHITE],
                [wcc.GREEN, wcc.YELLOW, wcc.PINK],
                [wcc.WWHITE, wcc.BLACK, wcc.BLACK],
                [wcc.BLACK, wcc.Color(30,30,30), wcc.Color(30,30,30)]]
        self.color_mode_pos = 0
        self.rb_pos = 0 # index position for "rainbow"-mode

    def run(self, wcd, wci):
        '''
        Displays time until aborted by user interaction on pin button_return
        '''
        while True:
            # Set background color
            wcd.setColorToAll(self.bg_color, includeMinutes=True)
            # Set current time
            now = datetime.datetime.now()
            # Returns indices, which represent the current time, when beeing illuminated
            taw_indices = self.taw.get_time(now)
            #TODO: Improve rendering of time during while-loop: Render array only once per 5 minutes...
            wcd.setColorBy1DCoordinates(wcd.strip, taw_indices, self.word_color)
            wcd.setMinutes(now, self.minute_color)
            wcd.show()
            event = wci.waitSecondsForEvent([wci.button_left, wci.button_return, wci.button_right], 10)
            # Switch display color, if button_left is pressed
            if (event == wci.button_left):
                self.color_mode_pos += 1
                if self.color_mode_pos == len(self.color_modes):
                    self.color_mode_pos = 0
                self.bg_color     = self.color_modes[self.color_mode_pos][0]
                self.word_color   = self.color_modes[self.color_mode_pos][1]
                self.minute_color = self.color_modes[self.color_mode_pos][2]
                time.sleep(0.2)
            # Return to main menu, if button_return is pressed
            if (event == wci.button_return):
                return
            if (event == wci.button_right):
                self.bg_color = wcc.BLACK
                wcd.setColorToAll(self.bg_color, includeMinutes=True)
                while wci.getPinState(wci.button_right):
                    # BEGIN: Rainbow generation as done in rpi_ws281x strandtest example! Thanks to Tony DiCola for providing :)
                    if self.rb_pos < 85:
                        self.word_color = self.minute_color = wcc.Color(3*self.rb_pos, 255-3*self.rb_pos, 0)
                    elif self.rb_pos < 170:
                        self.word_color = self.minute_color = wcc.Color(255-3*(self.rb_pos-85), 0, 3*(self.rb_pos-85))
                    else:
                        self.word_color = self.minute_color = wcc.Color(0, 3*(self.rb_pos-170), 255-3*(self.rb_pos-170))
                    # END: Rainbow generation as done in rpi_ws281x strandtest example! Thanks to Tony DiCola for providing :)
                    wcd.setColorBy1DCoordinates(wcd.strip, taw_indices, self.word_color)
                    wcd.setMinutes(now, self.minute_color)
                    wcd.show()
                    self.rb_pos += 1
                    if self.rb_pos == 256: self.rb_pos = 0
                    time.sleep(0.02)

