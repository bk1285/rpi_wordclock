import ast
import logging

class wiring:
    """
    A class, holding all information of the wordclock's layout to map given
    timestamps, 2d-coordinates to the corresponding LEDs (corresponding to
    the individual wiring/layout of any wordclock).
    If a different wordclock wiring/layout is chosen, this class needs to be
    adopted.
    """

    def __init__(self, config):

        # LED strip configuration:
        try:
            language = ''.join(config.get('wordclock_display', 'language'))
        except:
            # For backward compatibility
            language = ''.join(config.get('plugin_time_default', 'language'))
        
        stencil_content = ast.literal_eval(config.get('language_options', language))
        self.WCA_HEIGHT = len(stencil_content)
        self.WCA_WIDTH = len(stencil_content[0])
        self.LED_COUNT = self.WCA_WIDTH * self.WCA_HEIGHT + 4  # Number of LED pixels.
        self.LED_PIN = 18  # GPIO pin connected to the pixels (must support PWM!).
        self.LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
        self.LED_DMA = 10  # DMA channel to use for generating signal
        self.LED_INVERT = False  # True to invert the signal (when using NPN transistor level shift)
        wiring_layout = config.get('wordclock_display', 'wiring_layout')

        logging.info('Wiring configuration')
        logging.info('  WCA_WIDTH: ' + str(self.WCA_WIDTH))
        logging.info('  WCA_HEIGHT: ' + str(self.WCA_HEIGHT))
        logging.info('  Num of LEDs: ' + str(self.LED_COUNT))
        logging.info('  Wiring layout: ' + str(wiring_layout))

        if config.getboolean('wordclock', 'developer_mode'):
            self.wcl = gtk_wiring(self.WCA_WIDTH, self.WCA_HEIGHT)
            logging.warning('Developer mode overwrites wiring layout to gtk_wiring!')
        elif wiring_layout == 'bernds_wiring':
            self.wcl = bernds_wiring(self.WCA_WIDTH, self.WCA_HEIGHT)
        elif wiring_layout == 'christians_wiring':
            self.wcl = christians_wiring(self.WCA_WIDTH, self.WCA_HEIGHT)
        elif wiring_layout == 'timos_wiring':
            self.wcl = timos_wiring(self.WCA_WIDTH, self.WCA_HEIGHT)
        elif wiring_layout == 'mini_wiring':
            self.LED_COUNT = self.WCA_HEIGHT * (self.WCA_WIDTH + 1) + 3
            self.wcl = mini_wiring(self.WCA_WIDTH, self.WCA_HEIGHT)
        elif wiring_layout == 'sebastians_wiring':
            self.LED_COUNT = 150
            self.wcl = sebastians_wiring(self.WCA_WIDTH, self.WCA_HEIGHT)
        elif wiring_layout == 'mini_wiring2':
            self.LED_COUNT = self.WCA_HEIGHT * (self.WCA_WIDTH + 1) + 4
            self.wcl = mini_wiring2(self.WCA_WIDTH, self.WCA_HEIGHT)
        elif wiring_layout == 'micro_net_wiring':
            self.wcl = micro_net_wiring(self.WCA_WIDTH, self.WCA_HEIGHT)
        elif wiring_layout == 'webdisaster_wiring':
            self.wcl = webdisaster_wiring(self.WCA_WIDTH, self.WCA_HEIGHT)
        elif wiring_layout == 'momonunu_wiring':
            self.wcl = momonunu_wiring(self.self.WCA_WIDTH, self.WCA_HEIGHT)
        else:
            logging.warning('No valid wiring layout found. Falling back to default!')
            self.wcl = bernds_wiring(self.WCA_WIDTH, self.WCA_HEIGHT)

    def setColorBy1DCoordinate(self, strip, i, color):
        """
        Linear mapping from top-left to bottom right
        """
        self.setColorBy2DCoordinates(strip, i % self.WCA_WIDTH, i / self.WCA_WIDTH, color)

    def setColorBy1DCoordinates(self, strip, ledCoordinates, color):
        """
        Linear mapping from top-left to bottom right
        """
        for i in ledCoordinates:
            self.setColorBy1DCoordinate(strip, i % self.WCA_WIDTH, int(i / self.WCA_WIDTH), color)

    def setColorBy2DCoordinates(self, strip, x, y, color):
        """
        Assignes a color to the 2D coordinates of the wordclocks display
        """
        strip.setPixelColor(self.wcl.getStripIndexFrom2D(x, y), color)

    def setColorToMinute(self, strip, min, color):
        """
        Assignes a color to a minute LED
        """
        strip.setPixelColor(self.mapMinutes(min), color)

    def getStripIndexFrom2D(self, x, y):
        return self.wcl.getStripIndexFrom2D(x, y)

    def mapMinutes(self, min):
        """
        Access minutes (1,2,3,4)
        """
        return self.wcl.mapMinutes(min)


class base_wiring:
    """
    A class, holding all information of the wordclock's layout to map given
    timestamps, 2d-coordinates to the corresponding LEDs (corresponding to
    the individual wiring/layout of any wordclock).
    If a different wordclock wiring/layout is chosen, select or implement a child class.
    """

    def __init__(self, WCA_WIDTH, WCA_HEIGHT):
        self.WCA_WIDTH = WCA_WIDTH
        self.WCA_HEIGHT = WCA_HEIGHT
        self.LED_COUNT = self.WCA_WIDTH * self.WCA_HEIGHT + 4

    def getStripIndexFrom2D(self, x, y):
        """
        Mapping coordinates to the wordclocks display
        Implementation is hardware/wiring dependent
        Final range:
             (0,0): top-left
             (self.WCA_WIDTH-1, self.WCA_HEIGHT-1): bottom-right
        """
        if x % 2 == 0:
            return (self.WCA_WIDTH - x - 1) * self.WCA_HEIGHT + y + 2
        else:
            return (self.WCA_WIDTH - x) * self.WCA_HEIGHT - y + 1

    def mapMinutes(self, min):
        """
        Access minutes (1,2,3,4)
        Implementation is hardware/wiring dependent
        This implementation assumes the minutes to be wired as first and last two leds of the led-strip
        """
        if min < 1 or min > 4:
            logging.error('Minute index of range. Expected 1,2,3 or 4, but received ' + min)
            return 0
        return self.mapMinutesInternal(min)

    def mapMinutesInternal(self, min):
        if min == 1:
            return self.LED_COUNT - 1
        elif min == 2:
            return 1
        elif min == 3:
            return self.LED_COUNT - 2
        elif min == 4:
            return 0

    def mapMinutesInternalAtBegin(self, min):
        """
        This implementation assumes the minutes to be wired as the first four leds of the led-strip
        """
        return min - 1

    def mapMinutesInternalLedsAtEnd(self, min):
        """
        This implementation assumes the minutes to be wired as the last four leds of the led-strip
        """
        return self.LED_COUNT - 5 + min


class bernds_wiring(base_wiring):
    pass

class gtk_wiring(base_wiring):

    def getStripIndexFrom2D(self, x, y):
        return y * self.WCA_WIDTH + x

    def mapMinutesInternal(self, min):
        return self.mapMinutesInternalLedsAtEnd(min)


class christians_wiring(base_wiring):

    def getStripIndexFrom2D(self, x, y):
        if y % 2 == 0:
            return (self.WCA_HEIGHT - y - 1) * self.WCA_WIDTH + x
        else:
            return (self.WCA_HEIGHT - y) * self.WCA_WIDTH - x - 1

    def mapMinutesInternal(self, min):
        return self.mapMinutesInternalLedsAtEnd(min)


class timos_wiring(base_wiring):

    def getStripIndexFrom2D(self, x, y):
        if x % 2 == 0:  # even columns 0,2,4,6,8,10
            return (x) * self.WCA_HEIGHT + y + 2  # last +2 for the minute LEDs before the WCA
        else:  # odd columns 1,3,5,7,9
            return (self.WCA_HEIGHT) + (self.WCA_HEIGHT * x) - y + 1

    def mapMinutesInternal(self, min):
        """
        This implementation assumes the minutes to be wired as first and last two leds of the led-strip
        """
        if min == 1:
            return 1
        elif min == 2:
            return self.LED_COUNT - 1
        elif min == 3:
            return self.LED_COUNT - 2
        elif min == 4:
            return 0


class mini_wiring(base_wiring):

    def __init__(self, WCA_WIDTH, WCA_HEIGHT):
        self.WCA_WIDTH = WCA_WIDTH
        self.WCA_HEIGHT = WCA_HEIGHT + 1
        self.LED_COUNT = self.WCA_WIDTH * self.WCA_HEIGHT + 4

    def getStripIndexFrom2D(self, x, y):
        if x % 2 == 0:
            return (self.WCA_WIDTH * self.WCA_HEIGHT) - (self.WCA_HEIGHT * x) - y + 2
        else:
            return (self.WCA_WIDTH - x - 1) * self.WCA_HEIGHT + y + 4

    def mapMinutesInternal(self, min):
        return self.mapMinutesInternalAtBegin(min)


class sebastians_wiring(base_wiring):
    """
    This wiring layout allows for a wordclock setup, which requires only
    a single (the very last) led to be soldered.
    """

    def __init__(self, WCA_WIDTH, WCA_HEIGHT):
        self.WCA_WIDTH = WCA_WIDTH
        self.WCA_HEIGHT = WCA_HEIGHT + 1
        self.LED_COUNT = 150

    def getStripIndexFrom2D(self, x, y):
        if x % 2 == 0:
            return (self.WCA_WIDTH - x - 1) * self.WCA_HEIGHT + y + 16
        else:
            return (self.WCA_WIDTH * self.WCA_HEIGHT) - (self.WCA_HEIGHT * x) - y + 14

    def mapMinutesInternal(self, min):
        """
        This implementation assumes the minutes to be wired as first and last two leds of the led-strip
        """
        if min == 1:
            return self.LED_COUNT - 1
        elif min == 2:
            return 12
        elif min == 3:
            return self.LED_COUNT - 11
        elif min == 4:
            return 0


class mini_wiring2(base_wiring):
    """
    This wiring layout allows for a wordclock setup, which requires only
    a single (the very last) led to be soldered.
    """

    def __init__(self, WCA_WIDTH, WCA_HEIGHT):
        self.WCA_WIDTH = WCA_WIDTH
        self.WCA_HEIGHT = WCA_HEIGHT + 1
        self.LED_COUNT = self.WCA_WIDTH * self.WCA_HEIGHT + 3

    def getStripIndexFrom2D(self, x, y):
        if x % 2 == 0:
            return (self.WCA_WIDTH - x - 1) * self.WCA_HEIGHT + y + 2
        else:
            return (self.WCA_WIDTH * self.WCA_HEIGHT) - (self.WCA_HEIGHT * x) - y


class micro_net_wiring(base_wiring):
    """
    This class implements the wiring layout as described in
    https://www.mikrocontroller.net/articles/WordClock_mit_WS2812#Anschluss_WS2812-Streifen_f.C3.BCr_WordClock12h
    """

    def getStripIndexFrom2D(self, x, y):
        if y % 2 == 0:
            return y * self.WCA_WIDTH + x + 4
        else:
            return (y + 1) * self.WCA_WIDTH - x + 3

    def mapMinutesInternal(self, min):
        """
        This implementation assumes the minutes to be wired as the first four leds of the led-strip
        """
        if min == 1:
            return 3
        elif min == 2:
            return 0
        elif min == 3:
            return 2
        elif min == 4:
            return 1


class webdisaster_wiring(base_wiring):
    """
    This class implements the wiring layout as described in
    https://www.mikrocontroller.net/articles/WordClock_mit_WS2812#Anschluss_WS2812-Streifen_f.C3.BCr_WordClock12h
    """

    def getStripIndexFrom2D(self, x, y):
        if y % 2 == 0:
            return y * self.WCA_WIDTH + x
        else:
            return (y + 1) * self.WCA_WIDTH - x - 1

    def mapMinutesInternal(self, min):
        """
        This implementation assumes the minutes to be wired as the last four leds of the led-strip
        """
        return self.mapMinutesInternalLedsAtEnd(self, min)

class momonunu_wiring(base_wiring):
    """
    Costum Wiring because I messed up Bernds
    """

    def getStripIndexFrom2D(self, x, y):
        if y % 2 == 0:
            return (x * WCA_HEIGHT + 2) + (WCA_HEIGHT - y - 1)
        else:
            return (x * WCA_HEIGHT + 2) + y

    def mapMinutesInternal(self, min):
        if min == 1:
            return self.LED_COUNT - 1
        elif min == 2:
            return self.LED_COUNT - 2
        elif min == 3:
            return 1
        elif min == 4:
            return 0

