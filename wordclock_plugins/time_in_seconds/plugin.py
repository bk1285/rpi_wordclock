import datetime
import os
import time
import time_seconds
import wordclock_tools.wordclock_colors as wcc


class plugin:
    """
    Description for lazy reader
    """

    def __init__(self, config):
        """
        Initializations for the startup of the current wordclock plugin
        """
        # Get plugin name (according to the folder, it is contained in)
        self.name = os.path.dirname(__file__).split('/')[-1]
        self.pretty_name = "Seconds"
        self.description = "Shows the current seconds. The fool thinks no time flies"

	self.taw = time_seconds.time_seconds()

	self.bg_color = wcc.BLACK  # default background color
        self.word_color = wcc.WHITE  # default word color
        self.minute_color = wcc.BLACK  # default minute color

    def run(self, wcd, wci):
        """
        Displays time until aborted by user interaction on pin button_return
        """
        # Some initializations of the "previous" minute
        prev_sec = -1

        while True:
            # Get current time
            now = datetime.datetime.now()
            # Check, if a second has passed (to render the new time)
            if prev_sec < now.second:
                # Set background color
                self.show_time(wcd, wci)
                prev_sec = -1 if now.second == 59 else now.second
	    event = wci.waitForEvent(0.1)
            if (event == wci.EVENT_BUTTON_RETURN) \
                    or (event == wci.EVENT_EXIT_PLUGIN) \
		    or (event == wci.EVENT_NEXT_PLUGIN_REQUESTED):
		return

    def show_time(self, wcd, wci):
        now = datetime.datetime.now()
        # Set background color
        wcd.setColorToAll(self.bg_color, includeMinutes=True)
        
	for i in range(110, -1, -110/11):
		taw_indices = self.taw.get_time(now, current=False)
		wcd.setColorBy1DCoordinates(wcd.strip, taw_indices, wcc.Color(i, i, i))
		taw_indices = self.taw.get_time(now, current=True)
		wcd.setColorBy1DCoordinates(wcd.strip, taw_indices, self.word_color)
		wcd.setMinutes(now, self.minute_color)
		wcd.show()
		time.sleep(0.05)
