import datetime
import logging
import os
import time
import wordclock_tools.wordclock_colors as wcc
import wordclock_tools.wordclock_display as wcd


class plugin:
    """
    A class to display the current time (default mode).
    This default mode needs to be adapted to the hardware
    layout of the wordclock (the chosen stencil) and is
    the most essential time display mode of the wordclock.
    """

    def __init__(self, config):
        """
        Initializations for the startup of the current wordclock plugin
        """
        # Get plugin name (according to the folder, it is contained in)
        self.name = os.path.dirname(__file__).split('/')[-1]
        self.pretty_name = "The time"
        self.description = "The minimum, you should expect from a wordclock."

        self.animation = ''.join(config.get('plugin_' + self.name, 'animation'))

        animations = ["fadeOutIn", "typewriter", "none"]

        if self.animation not in animations:
            logging.warning('No animation set for default plugin within the config-file. ' + animations[0] + ' animation will be used.')
            self.animation = animations[0]

        self.animation_speed = config.getint('plugin_' + self.name, 'animation_speed')

        self.play_animation_each_minute = config.getboolean('plugin_time_default', 'play_animation_each_minute')
        self.purist = config.getboolean('plugin_time_default', 'purist')

        self.sleep_begin = datetime.datetime.strptime(config.get('plugin_' + self.name, 'sleep_begin'), '%H:%M').time()
        self.sleep_end = datetime.datetime.strptime(config.get('plugin_' + self.name, 'sleep_end'), '%H:%M').time()
        self.sleep_brightness = config.getint('plugin_' + self.name, 'sleep_brightness')

        # Choose default fgcolor
        fgcolor = ''.join(config.get('plugin_time_default', 'default_fg_color'))

        if fgcolor == 'BLACK':
            self.word_color = wcc.BLACK
            self.minute_color = wcc.BLACK
        elif fgcolor == 'WHITE':
            self.word_color = wcc.WHITE
            self.minute_color = wcc.WHITE
        elif fgcolor == 'WWHITE':
            self.word_color = wcc.WWHITE
            self.minute_color = wcc.WWHITE
        elif fgcolor == 'RED':
            self.word_color = wcc.RED
            self.minute_color = wcc.RED
        elif fgcolor == 'YELLOW':
            self.word_color = wcc.YELLOW
            self.minute_color = wcc.YELLOW
        elif fgcolor == 'LIME':
            self.word_color = wcc.LIME
            self.minute_color = wcc.LIME
        elif fgcolor == 'GREEN':
            self.word_color = wcc.GREEN
            self.minute_color = wcc.GREEN
        elif fgcolor == 'BLUE':
            self.word_color = wcc.BLUE
            self.minute_color = wcc.BLUE
        else:
            print('Could not detect default_fg_color: ' + fgcolor + '.')
            print('Choosing default: warm white')
            self.word_color = wcc.WWHITE
            self.minute_color = wcc.WWHITE

        bgcolor = ''.join(config.get('plugin_time_default', 'default_bg_color'))

        if bgcolor == 'BLACK':
            self.bg_color = wcc.BLACK
        elif bgcolor == 'WHITE':
            self.bg_color = wcc.WHITE
        elif bgcolor == 'WWHITE':
            self.bg_color = wcc.WWHITE
        elif bgcolor == 'RED':
            self.bg_color = wcc.RED
        elif bgcolor == 'YELLOW':
            self.bg_color = wcc.YELLOW
        elif bgcolor == 'LIME':
            self.bg_color = wcc.LIME
        elif bgcolor == 'GREEN':
            self.bg_color = wcc.GREEN
        elif bgcolor == 'BLUE':
            self.bg_color = wcc.BLUE
        else:
            print('Could not detect default_bg_color: ' + bgcolor + '.')
            print('Choosing default: black')
            self.bg_color = wcc.BLACK

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
             [wcc.BLACK, wcc.Color(30, 30, 30), wcc.Color(30, 30, 30)]]
        self.color_mode_pos = 0
        self.rb_pos = 0  # index position for "rainbow"-mode

        self.brightness_mode_pos = config.getint('wordclock_display', 'brightness')
        self.brightness_change = 8

        self.use_brightness_sensor = config.getboolean('wordclock_display', 'use_brightness_sensor')

        print(('Using brigtness sensor : ' + str(self.use_brightness_sensor)))
        if self.use_brightness_sensor:
            print('Importing sensor Library ')
            import board
            import busio
            import adafruit_tsl2561
            i2c = busio.I2C(board.SCL, board.SDA)
            self.sensor = adafruit_tsl2561.TSL2561(i2c)
        # save current brightness for switching back from sleep mode
        self.wake_brightness = self.brightness_mode_pos

    def run(self, wcd, wci):
        """
        Displays time until aborted by user interaction on pin button_return
        """
        # Some initializations of the "previous" minute
        prev_min = -1
        if self.use_brightness_sensor:
            sensorMax = 100.0
            sensorCurrent = 120.0
            brightnessMin = 50.0
            brightnessMax = 255.0

            self.brightness_mode_pos = min(((((brightnessMax - brightnessMin) / sensorMax) * sensorCurrent) + brightnessMin),255)

        while True:
            # Get current time
            now = datetime.datetime.now()
            newBrightness = self.brightness_mode_pos
            if self.use_brightness_sensor:
                try:
                    sensorCurrent = self.sensor.lux
                    if isinstance(sensorCurrent, float):
                        # print('sensorCurrent is ' + str(sensorCurrent))
                        newBrightness = min(((((brightnessMax - brightnessMin) / sensorMax) * sensorCurrent) + brightnessMin),255)
                        newBrightness = int(newBrightness)
                        time.sleep(0.2)
                except IOError as e:
                    print(e)

            # Check if text needs to be displayed
            if wcc.scrollenable:
                try:
                    if datetime.datetime.now() > wcc.scrolldatetime:
                        wcd.showText(wcc.scrolltext)
                        wcc.scrolldatetime = wcc.scrolldatetime + datetime.timedelta(seconds = wcc.scrollrepeat)
                except:
                    print("Date and time not set")

            # Check, if a minute has passed (to render the new time)
            if prev_min < now.minute:
                sleepActive = \
                    self.sleep_begin <= now.time() < self.sleep_end or \
                    self.sleep_end < self.sleep_begin <= now.time() <= datetime.time(23, 59, 59) or \
                    now.time() < self.sleep_end < self.sleep_begin

                wcd.setBrightness(self.sleep_brightness if sleepActive else newBrightness)
 
                # Set background color
                if self.play_animation_each_minute:
                    animation = self.animation
                else:
                    animation = self.animation if now.minute%5 == 0 else 'None'

                self.show_time(wcd, wci, animation, animation_speed=self.animation_speed)
                prev_min = -1 if now.minute == 59 else now.minute

            if newBrightness != self.brightness_mode_pos:
                self.brightness_mode_pos = newBrightness
                wcd.setBrightness(newBrightness)
                self.show_time(wcd, wci, animation='None')

            event = wci.waitForEvent(2)
            # Switch display color, if button_left is pressed
            if event == wci.EVENT_BUTTON_LEFT:
                self.color_mode_pos += 1
                if self.color_mode_pos == len(self.color_modes):
                    self.color_mode_pos = 0
                self.bg_color = self.color_modes[self.color_mode_pos][0]
                self.word_color = self.color_modes[self.color_mode_pos][1]
                self.minute_color = self.color_modes[self.color_mode_pos][2]
                self.show_time(wcd, wci, animation=self.animation, animation_speed=self.animation_speed)
                time.sleep(0.2)
            if (event == wci.EVENT_BUTTON_RETURN) \
                    or (event == wci.EVENT_EXIT_PLUGIN) \
                    or (event == wci.EVENT_NEXT_PLUGIN_REQUESTED):
                wcd.setBrightness(self.wake_brightness)
                wcd.show()
                self.skip_sleep = False
                return
            if event == wci.EVENT_BUTTON_RIGHT:
                time.sleep(wci.lock_time)
                self.color_selection(wcd, wci)

    def show_time(self, wcd, wci, animation=None, animation_speed=25):
        now = datetime.datetime.now()
        # Set background color
        wcd.setColorToAll(self.bg_color, includeMinutes=True)
        # Returns indices, which represent the current time, when being illuminated
        taw_indices = wcd.taw.get_time(now, self.purist)
        wcd.setColorBy1DCoordinates(taw_indices, self.word_color)
        wcd.setMinutes(now, self.minute_color)
        wcd.show(animation, animation_speed)

    def color_selection(self, wcd, wci):
        while True:
            # BEGIN: Rainbow generation as done in rpi_ws281x strandtest example! Thanks to Tony DiCola for providing :)
            if self.rb_pos < 85:
                self.word_color = self.minute_color = wcc.Color(3 * self.rb_pos, 255 - 3 * self.rb_pos, 0)
            elif self.rb_pos < 170:
                self.word_color = self.minute_color = wcc.Color(255 - 3 * (self.rb_pos - 85), 0, 3 * (self.rb_pos - 85))
            else:
                self.word_color = self.minute_color = wcc.Color(0, 3 * (self.rb_pos - 170),
                                                                255 - 3 * (self.rb_pos - 170))
            # END: Rainbow generation as done in rpi_ws281x strandtest example! Thanks to Tony DiCola for providing :)
            # TODO: Evaluate taw_indices only every n-th loop (saving resources)
            now = datetime.datetime.now()  # Set current time
            taw_indices = wcd.taw.get_time(now, self.purist)
            wcd.setColorToAll(self.bg_color, includeMinutes=True)
            wcd.setColorBy1DCoordinates(taw_indices, self.word_color)
            wcd.setMinutes(now, self.minute_color)
            wcd.show()
            self.rb_pos += 1
            if self.rb_pos == 256: self.rb_pos = 0
            event = wci.waitForEvent(0.1)
            if event != wci.EVENT_INVALID:
                time.sleep(wci.lock_time)
                break
        if not self.use_brightness_sensor:
            while True:
                self.brightness_mode_pos += self.brightness_change
                # TODO: Evaluate taw_indices only every n-th loop (saving resources)
                now = datetime.datetime.now()  # Set current time
                taw_indices = wcd.taw.get_time(now, self.purist)
                wcd.setColorToAll(self.bg_color, includeMinutes=True)
                wcd.setColorBy1DCoordinates(taw_indices, self.word_color)
                wcd.setMinutes(now, self.minute_color)
                wcd.setBrightness(self.brightness_mode_pos)
                wcd.show()
                if self.brightness_mode_pos < abs(self.brightness_change) or self.brightness_mode_pos > 255 - abs(
                        self.brightness_change):
                    self.brightness_change *= -1
                event = wci.waitForEvent(0.1)
                if event != wci.EVENT_INVALID:
                    time.sleep(wci.lock_time)
                    return
