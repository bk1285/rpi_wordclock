import configparser
import fontdemo
import itertools
import logging
import os
from copy import deepcopy
from PIL import Image
from . import wiring
from time import sleep
from threading import Lock
import wordclock_plugins.time_default.time_bavarian as time_bavarian
import wordclock_plugins.time_default.time_dutch as time_dutch
import wordclock_plugins.time_default.time_english as time_english
import wordclock_plugins.time_default.time_french as time_french
import wordclock_plugins.time_default.time_german as time_german
import wordclock_plugins.time_default.time_german2 as time_german2
import wordclock_plugins.time_default.time_italian as time_italian
import wordclock_plugins.time_default.time_romanian as time_romanian
import wordclock_plugins.time_default.time_dutch as time_dutch
import wordclock_plugins.time_default.time_swabian as time_swabian
import wordclock_plugins.time_default.time_swabian2 as time_swabian2
import wordclock_plugins.time_default.time_swiss_german as time_swiss_german
import wordclock_plugins.time_default.time_swiss_german2 as time_swiss_german2
import wordclock_plugins.time_default.time_swedish as time_swedish
import wordclock_tools.wordclock_colors as wcc
import wordclock_tools.wordclock_screen as wordclock_screen
import colorsys


class wordclock_display:
    """
    Class to display any content on the wordclock display
    Depends on the (individual) wordclock layout/wiring
    """

    def __init__(self, config, wci):
        """
        Initialization
        """
        # Get the wordclocks wiring-layout
        self.wcl = wiring.wiring(config)
        self.wci = wci

        self.transition_cache_next = wordclock_screen.wordclock_screen(self)
        self.transition_cache_curr = wordclock_screen.wordclock_screen(self)

        self.config = config
        self.base_path = config.get('wordclock', 'base_path')
        self.mutex = Lock()

        self.setBrightness(config.getint('wordclock_display', 'brightness'))

        if config.getboolean('wordclock', 'developer_mode'):
            import wordclock_tools.wordclock_strip_wx as wcs_wx
            self.strip = wcs_wx.WxStrip(wci)
        else:
            import wordclock_tools.wordclock_strip_neopixel as wcs_neo
            self.strip = wcs_neo.wordclock_strip_neopixel(self.wcl)

        if config.get('wordclock_display', 'default_font') == 'wcfont':
            self.default_font =  self.base_path + '/wcfont.ttf'
        else:
            self.default_font = os.path.join('/usr/share/fonts/truetype/freefont/', config.get('wordclock_display', 'default_font') + '.ttf')

        self.strip.begin()

        # Choose default fgcolor
        fgcolor = ''.join(config.get('plugin_time_default', 'default_fg_color'))

        if fgcolor == 'BLACK':
            self.default_fg_color = wcc.BLACK
        elif fgcolor == 'WHITE':
            self.default_fg_color = wcc.WHITE
        elif fgcolor == 'WWHITE':
            self.default_fg_color = wcc.WWHITE
        elif fgcolor == 'RED':
            self.default_fg_color = wcc.RED
        elif fgcolor == 'YELLOW':
            self.default_fg_color = wcc.YELLOW
        elif fgcolor == 'LIME':
            self.default_fg_color = wcc.LIME
        elif fgcolor == 'GREEN':
            self.default_fg_color = wcc.GREEN
        elif fgcolor == 'BLUE':
            self.default_fg_color = wcc.BLUE
        else:
            print('Could not detect default_fg_color: ' + fgcolor + '.')
            print('Choosing default: warm white')
            self.default_fg_color = wcc.WWHITE

        # Choose default bgcolor
        bgcolor = ''.join(config.get('plugin_time_default', 'default_bg_color'))

        if bgcolor == 'BLACK':
            self.default_bg_color = wcc.BLACK
        elif bgcolor == 'WHITE':
            self.default_bg_color = wcc.WHITE
        elif bgcolor == 'WWHITE':
            self.default_bg_color = wcc.WWHITE
        elif bgcolor == 'RED':
            self.default_bg_color = wcc.RED
        elif bgcolor == 'YELLOW':
            self.default_bg_color = wcc.YELLOW
        elif bgcolor == 'LIME':
            self.default_bg_color = wcc.LIME
        elif bgcolor == 'GREEN':
            self.default_bg_color = wcc.GREEN
        elif bgcolor == 'BLUE':
            self.default_bg_color = wcc.BLUE
        else:
            print('Could not detect default_bg_color: ' + bgcolor + '.')
            print('Choosing default: black')
            self.default_bg_color = wcc.BLACK

        # For backward compatibility
        language = ''.join(config.get('wordclock_display', 'language'))
        logging.info('Setting language to ' + language + '.')
        if language == 'bavarian':
            self.taw = time_bavarian.time_bavarian()
        elif language == 'dutch':
            self.taw = time_dutch.time_dutch()
        elif language == 'english':
            self.taw = time_english.time_english()
        elif language == 'french':
            self.taw = time_french.time_french()
        elif language == 'german':
            self.taw = time_german.time_german()
        elif language == 'german2':
            self.taw = time_german2.time_german2()
        elif language == 'italian':
            self.taw = time_italian.time_italian()
        elif language == 'romanian':
            self.taw = time_romanian.time_romanian()
        elif language == 'swabian':
            self.taw = time_swabian.time_swabian()
        elif language == 'swabian2':
            self.taw = time_swabian2.time_swabian2()
        elif language == 'swedish':
            self.taw = time_swedish.time_swedish()
        elif language == 'swiss_german':
            self.taw = time_swiss_german.time_swiss_german()
        elif language == 'swiss_german2':
            self.taw = time_swiss_german2.time_swiss_german2()
        else:
            logging.error('Could not detect language: ' + language + '.')
            logging.info('Choosing default: german')
            self.taw = time_german.time_german()

        self.fps = self.config.getint('wordclock', 'animation_fps')


    def getBrightness(self):
        """
        Returns the current brightness of the wordclock display
        """
        return self.brightness

    def setBrightness(self, brightness):
        """
        Sets the provided brightness to the wordclock display
        """
        self.brightness = max(min(brightness, 255), 0)

    def setBrightnessAndShow(self, brightness):
        """
        Sets the provided brightness to the wordclock display
        """
        with self.mutex:
            self.setBrightness(brightness)
        self.show()

    def setColorBy1DCoordinates(self, ledCoordinates, color):
        """
        Sets a pixel at given 1D coordinates
        """
        for i in ledCoordinates:
            self.setColorBy2DCoordinates(i % self.get_wca_width(), i // self.get_wca_width(), color)

    def setColorBy2DCoordinates(self, x, y, color):
        """
        Sets a pixel at given 2D coordinates
        """
        self.transition_cache_next.matrix[x][y] = color

    def setColorByMinute(self, min, color):
        if min >= 0 and min < 4:
            self.transition_cache_next.minutes[min] = color

    def get_wca_height(self):
        """
        Returns the height of the WCA
        """
        return self.wcl.WCA_HEIGHT

    def get_wca_width(self):
        """
        Returns the width of the WCA
        """
        return self.wcl.WCA_WIDTH

    def get_led_count(self):
        """
        Returns the overall number of LEDs
        """
        return self.wcl.LED_COUNT

    def dispRes(self):
        """
        Returns the resolution of the wordclock array as string
        E.g. to choose the correct resolution of animations and icons
        """
        return str(self.wcl.WCA_WIDTH) + 'x' + str(self.wcl.WCA_HEIGHT)

    def setColorToAll(self, color, includeMinutes=True):
        """
        Sets a given color to all leds
        If includeMinutes is set to True, color will also be applied to the minute-leds.
        """
        for x in range(self.get_wca_width()):
            for y in range(self.get_wca_height()):
                self.transition_cache_next.matrix[x][y] = color
        if includeMinutes:
            for m in range(4):
                self.transition_cache_next.minutes[m] = color

    def setColorTemperatureToAll(self, temperature, includeMinutes=True):
        """
        Sets a color to all leds based on the provided temperature in Kelvin
        If includeMinutes is set to True, color will also be applied to the minute-leds.
        """
        self.setColorToAll(wcc.color_temperature_to_rgb(temperature), includeMinutes)

    def resetDisplay(self):
        """
        Reset display
        """
        self.setColorToAll(wcc.BLACK, True)

    def showIcon(self, plugin, iconName):
        """
        Dispays an icon with a specified name.
        The icon needs to be provided within the graphics/icons folder.
        """
        self.setImage(
            self.base_path + '/wordclock_plugins/' + plugin + '/icons/' + self.dispRes() + '/' + iconName + '.png')

    def setImage(self, absPathToImage):
        """
        Set image (provided as absolute path) to current display
        """
        img = Image.open(absPathToImage)
        width, height = img.size
        for x in range(0, width):
            for y in range(0, height):
                rgb_img = img.convert('RGB')
                r, g, b = rgb_img.getpixel((x, y))
                self.setColorBy2DCoordinates(x, y, wcc.Color(r, g, b))
        self.show()

    def animate(self, plugin, animationName, fps=10, count=1, invert=False):
        """
        Runs an animation
        plugin: Plugin-name
        num_of_frames: Number of frames to be displayed
        count: Number of runs
        fps: frames per second
        invert: Invert order of animation
        """
        animation_dir = self.base_path + '/wordclock_plugins/' + plugin + '/animations/' + self.dispRes() + '/' + animationName + '/'
        num_of_frames = len([file_count for file_count in os.listdir(animation_dir)])

        if invert:
            animation_range = list(range(num_of_frames - 1, -1, -1))
        else:
            animation_range = list(range(0, num_of_frames))

        for _ in range(count):
            for i in animation_range:
                self.setImage(animation_dir + str(i).zfill(3) + '.png')
                if self.wci.waitForExit(1.0 / fps):
                    return

    def showText(self, text, font=None, fg_color=None, bg_color=None, fps=10, count=1):
        """
        Display text on display
        """
        if font is None:
            font = self.default_font
        if fg_color is None:
            fg_color = self.default_fg_color
        if bg_color is None:
            bg_color = self.default_bg_color

        text = '    ' + text + '    '

        fnt = fontdemo.Font(font, self.wcl.WCA_HEIGHT)

        text_width, text_height, text_max_descent = fnt.text_dimensions(text)
        text_as_pixel = fnt.render_text(text)

        # Display text count times
        for i in range(count):

            # Erase previous content
            self.setColorToAll(bg_color, includeMinutes=True)

            # Assure here correct rendering, if the text does not fill the whole display
            render_range = self.wcl.WCA_WIDTH if self.wcl.WCA_WIDTH < text_width else text_width
            for y in range(text_height):
                for x in range(render_range):
                    self.setColorBy2DCoordinates(x, y, fg_color if text_as_pixel.pixels[y * text_width + x] else bg_color)

            # Show first frame for 0.5 seconds
            self.show()
            if self.wci.waitForExit(0.5):
                return

            # Shift text from left to right to show all.
            for cur_offset in range(text_width - self.wcl.WCA_WIDTH + 1):
                for y in range(text_height):
                    for x in range(self.wcl.WCA_WIDTH):
                        self.setColorBy2DCoordinates(x, y, fg_color if text_as_pixel.pixels[y * text_width + x + cur_offset] else bg_color)
                self.show()
                if self.wci.waitForExit(1.0 / fps):
                    return

    def setMinutes(self, time, color):
        if time.minute % 5 != 0:
            for i in range(0, time.minute % 5):
                self.transition_cache_next.minutes[i] = color

    def apply_brightness(self, color):
        [h, s, v] = colorsys.rgb_to_hsv(color.r/255.0, color.g/255.0, color.b/255.0)
        [r, g, b] = colorsys.hsv_to_rgb(h, s, v * self.brightness/255.0)
        return wcc.Color(int(r*255.0), int(g*255.0), int(b*255.0))

    def render_transition_step(self, transition_cache_step):
        for x in range(self.get_wca_width()):
            for y in range(self.get_wca_height()):
                self.wcl.setColorBy2DCoordinates(self.strip, x, y, self.apply_brightness(transition_cache_step.matrix[x][y]))
        for m in range(4):
            self.wcl.setColorToMinute(self.strip, m + 1, self.apply_brightness(transition_cache_step.minutes[m]))
        self.strip.show()

    def show(self, animation = None, animation_speed = 5):
        """
        This function provides the current color settings to the LEDs
        """
        animation = None if self.fps == 0 else animation

        if animation == 'typewriter':
            transition_cache = wordclock_screen.wordclock_screen(self)
            for y in range(self.get_wca_height()):
                for x in range(self.get_wca_width()):
                    if self.transition_cache_next.matrix[x][y] is not wcc.BLACK:
                        transition_cache.matrix[x][y] = self.transition_cache_next.matrix[x][y]
                        self.render_transition_step(transition_cache)
                        sleep(1.0/animation_speed)
            self.transition_cache_curr = deepcopy(self.transition_cache_next)
            self.render_transition_step(self.transition_cache_curr)
        elif animation == 'fadeOutIn':
            with self.mutex:
                brightness = self.getBrightness()
                while self.getBrightness() > 0:
                    self.setBrightness(self.getBrightness() - animation_speed)
                    self.render_transition_step(self.transition_cache_curr)
                    sleep(1.0/self.fps)
                self.transition_cache_curr = deepcopy(self.transition_cache_next)
                while self.getBrightness() < brightness:
                    self.setBrightness(self.getBrightness() + animation_speed)
                    self.render_transition_step(self.transition_cache_curr)
                    sleep(1.0/self.fps)
        else: # no animation
            self.transition_cache_curr = deepcopy(self.transition_cache_next)
            self.render_transition_step(self.transition_cache_curr)

