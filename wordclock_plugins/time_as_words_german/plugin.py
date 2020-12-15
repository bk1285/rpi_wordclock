import datetime
import os
from . import time_as_words_german
import wordclock_tools.wordclock_colors as wcc


class plugin:
    """
    A class displaying the current time on a german WCA as real words...
    """

    def __init__(self, config):
        """
        Initializations for the startup of the current wordclock plugin
        """
        # Get plugin name (according to the folder, it is contained in)
        self.name = os.path.dirname(__file__).split('/')[-1]
        self.pretty_name = "Time as words (german)"
        self.description = "Displays the current time as words."

        self.taw = time_as_words_german.time_as_words_german()
        self.bg_color_index = 0  # default background color: black
        self.word_color_index = 2  # default word color: warm white

    def run(self, wcd, wci):
        """
        Displays time in words.
        User interaction on pin button_return needs to be implemented on demand.
        """
        # Set background color
        wcd.setColorToAll(wcc.colors[self.bg_color_index], includeMinutes=True)
        # Set current time
        now = datetime.datetime.now()
        wcd.showText(self.taw.get_time(now))
