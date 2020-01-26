from neopixel import Adafruit_NeoPixel, ws
import wordclock_tools.wordclock_colors as wcc
import logging

class wordclock_strip_neopixel(Adafruit_NeoPixel):

    def __init__(self, wcl):
        try:
            super(wordclock_strip_neopixel, self).__init__(wcl.LED_COUNT, wcl.LED_PIN, wcl.LED_FREQ_HZ,
                                                wcl.LED_DMA, wcl.LED_INVERT, 255 , 0, ws.WS2811_STRIP_GRB)
        except:
            logging.error('Update deprecated external dependency rpi_ws281x. '
                    'For details see also https://github.com/jgarff/rpi_ws281x/blob/master/python/README.md')
