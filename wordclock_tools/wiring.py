import ast

class wiring:
    '''
    A class, holding all information of the wordclock's layout to map given
    timestamps, 2d-coordinates to the corresponding LEDs (corresponding to
    the individual wiring/layout of any wordclock).
    If a different wordclock wiring/layout is chosen, this class needs to be
    adopted.
    '''

    def __init__(self, config):

        # LED strip configuration:
        language=config.get('stancil_parameter', 'language')
        stancil_content  = ast.literal_eval(config.get('language_options', language))
        self.WCA_HEIGHT  = len(stancil_content)
        self.WCA_WIDTH   = len(stancil_content[0].decode('utf-8'))
        self.LED_COUNT   = self.WCA_WIDTH*self.WCA_HEIGHT+4 # Number of LED pixels.
        self.LED_PIN     = 18      # GPIO pin connected to the pixels (must support PWM!).
        self.LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
        self.LED_DMA     = 5       # DMA channel to use for generating signal (try 5)
        self.LED_INVERT  = False   # True to invert the signal (when using NPN transistor level shift)
        print('Wiring configuration')
        print('  WCA_WIDTH: ' + str(self.WCA_WIDTH))
        print('  WCA_HEIGHT: ' + str(self.WCA_HEIGHT))
        print('  Num of LEDs: ' + str(self.LED_COUNT))

        wiring_layout = config.get('wordclock_display', 'wiring_layout')
        if wiring_layout == 'bernds_wiring':
            self.wcl = bernds_wiring(self.WCA_WIDTH, self.WCA_HEIGHT)
        elif wiring_layout == 'christians_wiring':
            self.wcl = christians_wiring(self.WCA_WIDTH, self.WCA_HEIGHT)
        elif wiring_layout == 'timos_wiring':
            self.wcl = timos_wiring(self.WCA_WIDTH, self.WCA_HEIGHT)
        else:
            print('Warning: No valid wiring layout found. Falling back to default!')
            self.wcl = bernds_wiring(self.WCA_WIDTH, self.WCA_HEIGHT)

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
        strip.setPixelColor(self.wcl.getStripIndexFrom2D(x,y), color)
    def getStripIndexFrom2D(self, x,y):
        return self.wcl.getStripIndexFrom2D(x,y)

    def mapMinutes(self, min):
        '''
        Access minutes (1,2,3,4)
        '''
        return self.wcl.mapMinutes(min)

class bernds_wiring:
    '''
    A class, holding all information of the wordclock's layout to map given
    timestamps, 2d-coordinates to the corresponding LEDs (corresponding to
    the individual wiring/layout of any wordclock).
    If a different wordclock wiring/layout is chosen, this class needs to be
    adopted.
    '''

    def __init__(self, WCA_WIDTH, WCA_HEIGHT):
        self.WCA_WIDTH   = WCA_WIDTH
        self.WCA_HEIGHT  = WCA_HEIGHT
        self.LED_COUNT   = self.WCA_WIDTH*self.WCA_HEIGHT+4

    def getStripIndexFrom2D(self, x, y):
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
        return pos

    def mapMinutes(self, min):
        '''
        Access minutes (1,2,3,4)
        Needs hardware/wiring dependent implementation
        This implementation assumes the minutes to be wired as first and last two leds of the led-strip
        '''
        if min == 1:
            return self.LED_COUNT-1
        elif min == 2:
            return 1
        elif min == 3:
            return self.LED_COUNT-2
        elif min == 4:
            return 0
        else:
            print('WARNING: Out of range, when mapping minutes...')
            print(min)
            return 0

class christians_wiring:
    '''
    A class, holding all information of the wordclock's layout to map given
    timestamps, 2d-coordinates to the corresponding LEDs (corresponding to
    the individual wiring/layout of any wordclock).
    If a different wordclock wiring/layout is chosen, this class needs to be
    adopted.
    '''

    def __init__(self, WCA_WIDTH, WCA_HEIGHT):
        self.WCA_WIDTH   = WCA_WIDTH
        self.WCA_HEIGHT  = WCA_HEIGHT
        self.LED_COUNT   = self.WCA_WIDTH*self.WCA_HEIGHT+4

    def getStripIndexFrom2D(self, x, y):
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
        return pos

    def mapMinutes(self, min):
        '''
        Access minutes (1,2,3,4)
        Needs hardware/wiring dependent implementation
        This implementation assumes the minutes to be wired as the last four leds of the led-strip
        '''
        if min == 1:
            return self.LED_COUNT-4
        elif min == 2:
            return self.LED_COUNT-3
        elif min == 3:
            return self.LED_COUNT-2
        elif min == 4:
            return self.LED_COUNT-1
        else:
            print('WARNING: Out of range, when mapping minutes...')
            print(min)
            return 0


class timos_wiring:
    '''
    A class, holding all information of the wordclock's layout to map given
    timestamps, 2d-coordinates to the corresponding LEDs (corresponding to
    the individual wiring/layout of any wordclock).
    If a different wordclock wiring/layout is chosen, this class needs to be
    adopted.
    '''

    def __init__(self, WCA_WIDTH, WCA_HEIGHT):
        self.WCA_WIDTH   = WCA_WIDTH
        self.WCA_HEIGHT  = WCA_HEIGHT
        self.LED_COUNT   = self.WCA_WIDTH*self.WCA_HEIGHT+4

    def getStripIndexFrom2D(self, x, y):
        '''
        Mapping coordinates to the wordclocks display
        Needs hardware/wiring dependent implementation
        Final range:
             (0,0): top-left
             (self.WCA_WIDTH-1, self.WCA_HEIGHT-1): bottom-right
        '''
        if x%2 == 0:   # even columns 0,2,4,6,8,10
            pos = (x)*self.WCA_HEIGHT+y+2     # last +2 for the minute LEDs before the WCA
        else:          # odd columns 1,3,5,7,9
            pos = (self.WCA_HEIGHT)+(self.WCA_HEIGHT*x)-y+1
        return pos

    def mapMinutes(self, min):
        '''
        Access minutes (1,2,3,4)
        Needs hardware/wiring dependent implementation
        This implementation assumes the minutes to be wired as first and last two leds of the led-strip
        '''
        if min == 1:
            return 1
        elif min == 2:
            return self.LED_COUNT-1
        elif min == 3:
            return self.LED_COUNT-2
        elif min == 4:
            return 0
        else:
            print('WARNING: Out of range, when mapping minutes...')
            print(min)
            return 0
