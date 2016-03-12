import datetime
import os
import time
import time_english
import time_german
import time_swabian
import time_dutch
import time_bavarian
import time_swiss_german
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
        if language == 'dutch':
            self.taw = time_dutch.time_dutch()
        elif language == 'english':
            self.taw = time_english.time_english()
        elif language == 'german':
            self.taw = time_german.time_german()
        elif language == 'swabian':
            self.taw = time_swabian.time_swabian()
        elif language == 'bavarian':
            self.taw = time_bavarian.time_bavarian()
        elif language == 'swiss_german':
            self.taw = time_swiss_german.time_swiss_german()
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
                [wcc.BLACK, wcc.ORANGE, wcc.ORANGE],
                [wcc.BLACK, wcc.ORANGE, wcc.WWHITE],
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
        try:
            self.brightness_mode_pos = config.getint('wordclock_display', 'brightness')
        except:
            print('WARNING: Brightness value not set in config-file: To do so, add a "brightness" between 1..255 to the [wordclock_display]-section.')
            self.brightness_mode_pos = 255
        self.brightness_change = 8

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
            if (event == wci.button_return):
                return # Return to main menu, if button_return is pressed
            if (event == wci.button_right):
                time.sleep(wci.lock_time)
                self.color_selection(wcd, wci)

    def color_selection(self, wcd, wci):
        while True:
            # BEGIN: Rainbow generation as done in rpi_ws281x strandtest example! Thanks to Tony DiCola for providing :)
            if self.rb_pos < 85:
                self.word_color = self.minute_color = wcc.Color(3*self.rb_pos, 255-3*self.rb_pos, 0)
            elif self.rb_pos < 170:
                self.word_color = self.minute_color = wcc.Color(255-3*(self.rb_pos-85), 0, 3*(self.rb_pos-85))
            else:
                self.word_color = self.minute_color = wcc.Color(0, 3*(self.rb_pos-170), 255-3*(self.rb_pos-170))
            # END: Rainbow generation as done in rpi_ws281x strandtest example! Thanks to Tony DiCola for providing :)
            #TODO: Evaluate taw_indices only every n-th loop (saving ressources)
            now = datetime.datetime.now() # Set current time
            taw_indices = self.taw.get_time(now)
            wcd.setColorToAll(self.bg_color, includeMinutes=True)
            wcd.setColorBy1DCoordinates(wcd.strip, taw_indices, self.word_color)
            wcd.setMinutes(now, self.minute_color)
            wcd.show()
            self.rb_pos += 1
            if self.rb_pos == 256: self.rb_pos = 0
            event = wci.waitSecondsForEvent([wci.button_return, wci.button_left, wci.button_right], 0.1)
            if event > 0:
                time.sleep(wci.lock_time)
                break
        while True:
            self.brightness_mode_pos += self.brightness_change
            #TODO: Evaluate taw_indices only every n-th loop (saving ressources)
            now = datetime.datetime.now() # Set current time
            taw_indices = self.taw.get_time(now)
            wcd.setColorToAll(self.bg_color, includeMinutes=True)
            wcd.setColorBy1DCoordinates(wcd.strip, taw_indices, self.word_color)
            wcd.setMinutes(now, self.minute_color)
            wcd.setBrightness(self.brightness_mode_pos)
            wcd.show()
            if self.brightness_mode_pos < abs(self.brightness_change) or self.brightness_mode_pos > 255 - abs(self.brightness_change):
                self.brightness_change *= -1
            event = wci.waitSecondsForEvent([wci.button_return, wci.button_left, wci.button_right], 0.1)
            if event > 0:
                time.sleep(wci.lock_time)
                return

