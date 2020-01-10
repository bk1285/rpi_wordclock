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
        self.wcl = wcl

    def setBrightness(self, brightness, brightness_before):

        for i in range(self.wcl.LED_COUNT):
            neoPixelColor = self.strip.getPixelColor(i)
            blue = ((neoPixelColor & 255)/brightness_before) * brightness
            green = (((neoPixelColor >> 8) & 255)/brightness_before) * brightness
            red = (((neoPixelColor >> 16) & 255)/brightness_before) * brightness
           
            color = wcc.Color(red, green, blue)
            self.strip.setPixelColor(i, color.neopixel())