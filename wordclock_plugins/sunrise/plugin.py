from astral import Astral
import datetime
import os
import wordclock_tools.wordclock_colors as wcc
import wordclock_plugins.time_default.time_english as time_english
import wordclock_plugins.time_default.time_german as time_german
import wordclock_plugins.time_default.time_german2 as time_german2
import wordclock_plugins.time_default.time_dutch as time_dutch
import wordclock_plugins.time_default.time_swabian as time_swabian
import wordclock_plugins.time_default.time_swabian2 as time_swabian2
import wordclock_plugins.time_default.time_bavarian as time_bavarian
import wordclock_plugins.time_default.time_swiss_german as time_swiss_german
import wordclock_plugins.time_default.time_swiss_german2 as time_swiss_german2


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

        self.astral_at_location = Astral()[config.get('plugin_' + self.name, 'location')]

        # Choose language to display sunrise
        language = ''.join(config.get('plugin_time_default', 'language'))
        if language == 'english':
            self.taw = time_english.time_english()
        elif language == 'german':
            self.taw = time_german.time_german()
        elif language == 'german2':
            self.taw = time_german2.time_german2()
	elif language == 'swabian':
            self.taw = time_swabian.time_swabian()
	elif language == 'swabian2':
            self.taw = time_swabian2.time_swabian2()
        elif language == 'dutch':
            self.taw = time_dutch.time_dutch()
	elif language == 'bavarian':
            self.taw = time_bavarian.time_bavarian()
        elif language == 'swiss_german':
            self.taw = time_swiss_german.time_swiss_german()
	elif language == 'swiss_german2':
            self.taw = time_swiss_german2.time_swiss_german2()
        else:
            print('Could not detect language: ' + language + '.')
            print('Choosing default: german')
            self.taw = wcp_time_german.time_german()

        self.bg_color_index = 0  # default background color: black
        self.word_color_index = 2  # default word color: warm white
        self.minute_color_index = 2  # default minute color: warm white

    def run(self, wcd, wci):
        """
        Displaying current time for sunrise/sunset
        """
        # Get data of sunrise
        sun_data = self.astral_at_location.sun(date=datetime.datetime.now(), local=True)
        # Display data of sunrise
        wcd.animate(self.name, 'sunrise', invert=True)
        wcd.setColorToAll(wcc.colors[self.bg_color_index], includeMinutes=True)
        taw_indices = self.taw.get_time(sun_data['sunrise'], withPrefix=False)
        wcd.setColorBy1DCoordinates(wcd.strip, taw_indices, wcc.colors[self.word_color_index])
        wcd.show()
        if wci.waitForExit(3.0):
            return
        # Display data of sunset
        wcd.animate(self.name, 'sunrise')
        wcd.setColorToAll(wcc.colors[self.bg_color_index], includeMinutes=True)
        taw_indices = self.taw.get_time(sun_data['sunset'], withPrefix=False)
        wcd.setColorBy1DCoordinates(wcd.strip, taw_indices, wcc.colors[self.word_color_index])
        wcd.show()
        if wci.waitForExit(3.0):
            return
        # Display current moon phase
        moon_phase = int(self.astral_at_location.moon_phase(datetime.datetime.now()))
        for i in range(0, moon_phase):
            wcd.showIcon('sunrise', 'moon_' + str(i).zfill(2))
            if wci.waitForExit(0.1):
                return
        if wci.waitForExit(3.0):
            return
