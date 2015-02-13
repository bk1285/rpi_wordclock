class bernds_wiring:
    '''
    A class, holding all information of the wordclock's layout to map given
    timestamps, 2d-coordinates to the corresponding LEDs (corresponding to
    the individual wiring/layout of any wordclock).
    If a different wordclock wiring/layout is chosen, this class needs to be
    adopted.
    '''

    def __init__(self):

        # LED strip configuration:
        self.LED_COUNT   = 125     # Number of LED pixels.
        self.LED_PIN     = 18      # GPIO pin connected to the pixels (must support PWM!).
        self.LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
        self.LED_DMA     = 5       # DMA channel to use for generating signal (try 5)
        self.LED_INVERT  = False   # True to invert the signal (when using NPN transistor level shift)

        self.WCA_WIDTH   = 11      # Wordclock array width
        self.WCA_HEIGHT  = 11      # Wordclock array height

    def setColorBy1DCoordinates(self, strip, ledCoordinates, color):
        '''
        Linear mapping from top-left to bottom right
        '''
        for i in ledCoordinates:
            self.setColorBy2DCoordinates(strip, i%self.WCA_WIDTH, i/self.WCA_WIDTH, color)

    def setColorBy2DCoordinates(self, strip, x, y, color):
        '''
        Mapping coordinates to the wordclocks display
        Needs hardware/wiring dependent implementation
        Final range:
             (0,0): top-left
             (self.WCA_WIDTH-1, self.WCA_HEIGHT-1): bottom-right
        '''
        if x%2 == 0:
            pos = (self.WCA_WIDTH-x-1)*self.WCA_HEIGHT+y+2
        else:
            pos = (self.WCA_WIDTH*self.WCA_HEIGHT)-(self.WCA_HEIGHT*x)-y+1

        strip.setPixelColor(pos, color)

    def mapMinutes(self, min):
        '''
        Access minutes (1,2,3,4)
        Needs hardware/wiring dependent implementation
        This implementation assumes the minutes to be wired as first and last two leds of the led-strip
        '''
        if min == 1:
            return 124
        elif min == 2:
            return 1
        elif min == 3:
            return 123
        elif min == 4:
            return 0
        else:
            print('WARNING: Out of range, when mapping minutes...')
            print(min)
            return 0

    def getMinuteIndices(self):
        '''
        Returns all indices of the led strip, which are representing minutes
        .. todo:: Merge/unify with mapMinutes
        '''
        return [113, 1, 112, 0]

    def getWcaIndices(self):
        '''
        Returns all indices of the led strip, which are part of the word clock array
        '''
        return range(2, self.LED_COUNT-2)


class christians_wiring:
    '''
    A class, holding all information of the wordclock's layout to map given
    timestamps, 2d-coordinates to the corresponding LEDs (corresponding to
    the individual wiring/layout of any wordclock).
    If a different wordclock wiring/layout is chosen, this class needs to be
    adopted.
    '''

    def __init__(self):

        # LED strip configuration:
        self.LED_COUNT   = 114     # Number of LED pixels.
        self.LED_PIN     = 18      # GPIO pin connected to the pixels (must support PWM!).
        self.LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
        self.LED_DMA     = 5       # DMA channel to use for generating signal (try 5)
        self.LED_INVERT  = False   # True to invert the signal (when using NPN transistor level shift)

        self.WCA_WIDTH   = 11      # Wordclock array width
        self.WCA_HEIGHT  = 10      # Wordclock array height

    def setColorBy1DCoordinates(self, strip, ledCoordinates, color):
        '''
        Linear mapping from top-left to bottom right
        '''
        for i in ledCoordinates:
            self.setColorBy2DCoordinates(strip, i%self.WCA_WIDTH, i/self.WCA_WIDTH, color)

    def setColorBy2DCoordinates(self, strip, x, y, color):
        '''
        Mapping coordinates to the wordclocks display
        Needs hardware/wiring dependent implementation
        Final range:
             (0,0): top-left
             (self.WCA_WIDTH-1, self.WCA_HEIGHT-1): bottom-right
        '''
        if y%2 == 0:
            pos = (self.WCA_HEIGHT-y-1)*self.WCA_WIDTH+x
        else:
            pos = (self.WCA_HEIGHT*self.WCA_WIDTH)-(self.WCA_WIDTH*y)-x-1

        strip.setPixelColor(pos, color)

    def mapMinutes(self, min):
        '''
        Access minutes (1,2,3,4)
        Needs hardware/wiring dependent implementation
        This implementation assumes the minutes to be wired as first and last two leds of the led-strip
        '''
        if min == 1:
            return 110
        elif min == 2:
            return 111
        elif min == 3:
            return 112
        elif min == 4:
            return 113
        else:
            print('WARNING: Out of range, when mapping minutes...')
            print(min)
            return 0

    def getMinuteIndices(self):
        '''
        Returns all indices of the led strip, which are representing minutes
        .. todo:: Merge/unify with mapMinutes
        '''
        return [110, 111, 112, 113]

    def getWcaIndices(self):
        '''
        Returns all indices of the led strip, which are part of the word clock array
        '''
        return range(0, self.LED_COUNT-4)

