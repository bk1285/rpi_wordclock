from astral import Astral
import datetime
import time
import wordclock_tools.wordclock_colors as wcc
import wordclock_plugins.time_german.time_german as wcp_time_german

class plugin:
    '''
    A class to display the time of sunrise/sunset
    Uses the astral library to retrieve information...
    '''

    def __init__(self, config):
        '''
        Initializations for the startup of the weather forecast
        '''
        self.name = 'sunrise'
        self.astral_at_location = Astral()[config.get('plugin_sunrise', 'location')]
        self.time_german = wcp_time_german.time_german()
        self.bg_color_index     = 0 # default background color: black
        self.word_color_index   = 2 # default word color: warm white
        self.minute_color_index = 2 # default minute color: warm white

    def run(self, wcd):
        '''
        Displaying current time for sunrise/sunset
        '''
        # Get data of sunrise
        sun_data = self.astral_at_location.sun(date=datetime.datetime.now(), local=True)
        # Display data of sunrise
        wcd.animate(self.name, 'sunrise', invert=True)
        wcd.setColorToAll(wcc.colors[self.bg_color_index], includeMinutes=True)
        time_german_indices = self.time_german.get_time(sun_data['sunrise'], withPrefix=False)
        wcd.wcl.setColorBy1DCoordinates(wcd.strip, time_german_indices, wcc.colors[self.word_color_index])
        wcd.show()
        time.sleep(3)
        # Display data of sunset
        wcd.animate(self.name, 'sunrise')
        wcd.setColorToAll(wcc.colors[self.bg_color_index], includeMinutes=True)
        time_german_indices = self.time_german.get_time(sun_data['sunset'], withPrefix=False)
        wcd.wcl.setColorBy1DCoordinates(wcd.strip, time_german_indices, wcc.colors[self.word_color_index])
        wcd.show()
        time.sleep(3)
        moon_phase = self.astral_at_location.moon_phase(datetime.datetime.now())
        for i in range(0, moon_phase):
            wcd.showIcon('sunrise', 'moon_'+str(i).zfill(2))
            time.sleep(0.1)
        time.sleep(3)

