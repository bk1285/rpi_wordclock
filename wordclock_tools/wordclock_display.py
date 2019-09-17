import ConfigParser
import fontdemo
import os
from PIL import Image
import wiring
import wordclock_plugins.time_default.time_english as time_english
import wordclock_plugins.time_default.time_german as time_german
import wordclock_plugins.time_default.time_german2 as time_german2
import wordclock_plugins.time_default.time_dutch as time_dutch
import wordclock_plugins.time_default.time_swabian as time_swabian
import wordclock_plugins.time_default.time_swabian2 as time_swabian2
import wordclock_plugins.time_default.time_bavarian as time_bavarian
import wordclock_plugins.time_default.time_swiss_german as time_swiss_german
import wordclock_plugins.time_default.time_swiss_german2 as time_swiss_german2
import wordclock_tools.wordclock_colors as wcc


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
        self.config = config

        self.base_path = config.get('wordclock', 'base_path')

        try:
            default_brightness = config.getint('wordclock_display', 'brightness')
        except:
            default_brightness = 255
            print(
                'WARNING: Default brightness value not set in config-file: '
                'To do so, add a "brightness" between 1..255 to the [wordclock_display]-section.')

        if config.getboolean('wordclock', 'developer_mode'):
            from GTKstrip import GTKstrip
            self.strip = GTKstrip(wci)
            self.default_font = 'wcfont.ttf'
        else:
            try:
                from neopixel import Adafruit_NeoPixel, ws
                self.strip = Adafruit_NeoPixel(self.wcl.LED_COUNT, self.wcl.LED_PIN, self.wcl.LED_FREQ_HZ,
                                               self.wcl.LED_DMA, self.wcl.LED_INVERT, default_brightness , 0,
                                               ws.WS2811_STRIP_GRB)
            except:
                print('Update deprecated external dependency rpi_ws281x. '
                      'For details see also https://github.com/jgarff/rpi_ws281x/blob/master/python/README.md')

            if config.get('wordclock_display', 'default_font') == 'wcfont':
				        self.default_font =  self.base_path + '/wcfont.ttf'
            else:
                self.default_font = os.path.join('/usr/share/fonts/truetype/freefont/',
												 config.get('wordclock_display', 'default_font') + '.ttf')

        # Initialize the NeoPixel object
        self.strip.begin()

        self.default_fg_color = wcc.WWHITE
        self.default_bg_color = wcc.BLACK

        # Choose language
        try:
            language = ''.join(config.get('wordclock_display', 'language'))
        except:
            # For backward compatibility
            language = ''.join(config.get('plugin_time_default', 'language'))

        print('  Setting language to ' + language + '.')
        if language == 'dutch':
            self.taw = time_dutch.time_dutch()
        elif language == 'english':
            self.taw = time_english.time_english()
        elif language == 'german':
            self.taw = time_german.time_german()
        elif language == 'german2':
            self.taw = time_german2.time_german2()
        elif language == 'swabian':
            self.taw = time_swabian.time_swabian()
        elif language == 'swabian2':
            self.taw = time_swabian2.time_swabian2()
        elif language == 'bavarian':
            self.taw = time_bavarian.time_bavarian()
        elif language == 'swiss_german':
            self.taw = time_swiss_german.time_swiss_german()
        elif language == 'swiss_german2':
            self.taw = time_swiss_german2.time_swiss_german2()
        else:
            print('Could not detect language: ' + language + '.')
            print('Choosing default: german')
            self.taw = time_german.time_german()

    def setPixelColor(self, pixel, color):
        """
        Sets the color for a pixel, while considering the brightness, set within the config file
        """
        self.strip.setPixelColor(pixel, color)

    def getBrightness(self):
        """
        Sets the color for a pixel, while considering the brightness, set within the config file
        """
        return self.strip.getBrightness()

    def setBrightness(self, brightness):
        """
        Sets the color for a pixel, while considering the brightness, set within the config file
        """
        self.strip.setBrightness(brightness)
        self.show()

    def setColorBy1DCoordinates(self, *args, **kwargs):
        """
        Sets a pixel at given 1D coordinates
        """
        return self.wcl.setColorBy1DCoordinates(*args, **kwargs)

    def setColorBy2DCoordinates(self, *args, **kwargs):
        """
        Sets a pixel at given 2D coordinates
        """
        return self.wcl.setColorBy2DCoordinates(*args, **kwargs)

    def get_wca_height(self):
        """
        Returns the height of the WCA
        """
        return self.wcl.WCA_HEIGHT

    def get_wca_width(self):
        """
        Returns the height of the WCA
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
        if includeMinutes:
            for i in range(self.wcl.LED_COUNT):
                self.setPixelColor(i, color)
        else:
            for i in self.wcl.getWcaIndices():
                self.setPixelColor(i, color)

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
                self.wcl.setColorBy2DCoordinates(self.strip, x, y, wcc.Color(r, g, b))
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
            animation_range = range(num_of_frames - 1, -1, -1)
        else:
            animation_range = range(0, num_of_frames)

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
        text_as_pixel = fnt.render_text(text, text_width, self.wcl.WCA_HEIGHT, 1)
	
	if self.config.getboolean('wordclock', 'developer_mode'):
		print text
		print text_as_pixel

        # Display text count times
        for i in range(count):

            # Erase previous content
            self.setColorToAll(bg_color, includeMinutes=True)

            # Assure here correct rendering, if the text does not fill the whole display
            render_range = self.wcl.WCA_WIDTH if self.wcl.WCA_WIDTH < text_width else text_width
            for y in range(self.wcl.WCA_HEIGHT):
                for x in range(render_range):
                    self.wcl.setColorBy2DCoordinates(self.strip, x, y,
                                                     fg_color if text_as_pixel.pixels[y * text_width + x] else bg_color)

            # Show first frame for 0.5 seconds
            self.show()
            if self.wci.waitForExit(0.5):
                return

            # Shift text from left to right to show all.
            for cur_offset in range(text_width - self.wcl.WCA_WIDTH + 1):
                for y in range(self.wcl.WCA_HEIGHT):
                    for x in range(self.wcl.WCA_WIDTH):
                        self.wcl.setColorBy2DCoordinates(self.strip, x, y, fg_color if text_as_pixel.pixels[
                            y * text_width + x + cur_offset] else bg_color)
                self.show()
                if self.wci.waitForExit(1.0 / fps):
                    return

    def setMinutes(self, time, color):
        if time.minute % 5 != 0:
            for i in range(1, time.minute % 5 + 1):
                self.setPixelColor(self.wcl.mapMinutes(i), color)

    def show(self):
        """
        This function provides the current color settings to the LEDs
        """
        self.strip.show()
