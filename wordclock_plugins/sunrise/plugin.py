from astral import moon, sun, geocoder
import datetime
import logging
import os
import pytz
import wordclock_tools.wordclock_colors as wcc

class plugin:
    """
    A class to display the time of sunrise/sunset
    Uses the astral library to retrieve information...
    """

    def __init__(self, config):
        """
        Initializations for the startup of the weather forecast
        """
        # Get plugin name (according to the folder, it is contained in)
        self.name = os.path.dirname(__file__).split('/')[-1]
        self.pretty_name = "Sunrise"
        self.description = "Displays the current times of sunrise and sunset."

        self.location = geocoder.lookup(config.get('plugin_' + self.name, 'location'), geocoder.database())
        logging.debug('Location for sunrise plugin set to ' + self.location.name)

        self.bg_color_index = 0  # default background color: black
        self.word_color_index = 2  # default word color: warm white
        self.minute_color_index = 2  # default minute color: warm white

    def run(self, wcd, wci):
        """
        Displaying current time for sunrise/sunset
        """
        # Get data of sunrise
        sun_data = sun.sun(self.location.observer, tzinfo=pytz.timezone(self.location.timezone))

        # Display data of sunrise
        wcd.animate(self.name, 'sunrise', invert=True)
        wcd.setColorToAll(wcc.colors[self.bg_color_index], includeMinutes=True)
        taw_indices = wcd.taw.get_time(sun_data['sunrise'], purist=True)
        wcd.setColorBy1DCoordinates(taw_indices, wcc.colors[self.word_color_index])
        wcd.show()
        if wci.waitForExit(3.0):
            return

        # Display data of sunset
        wcd.animate(self.name, 'sunrise')
        wcd.setColorToAll(wcc.colors[self.bg_color_index], includeMinutes=True)
        taw_indices = wcd.taw.get_time(sun_data['sunset'], purist=True)
        wcd.setColorBy1DCoordinates(taw_indices, wcc.colors[self.word_color_index])
        wcd.show()
        if wci.waitForExit(3.0):
            return
            
        # Display current moon phase
        moon_phase = int(moon.phase())
        for i in range(0, moon_phase):
            wcd.showIcon('sunrise', 'moon_' + str(i).zfill(2))
            if wci.waitForExit(0.1):
                return
        if wci.waitForExit(3.0):
            return
