import datetime
import os
import time
import time_seconds
import wordclock_tools.wordclock_colors as wcc


class plugin:
    """
    Drink mate and do some yoga while watching the time being over and over the same again.
    'The definition of insanity is doing the same thing over and over and expecting different results.' - Albert Einstein
    Credits: plotaBot
    """

    def __init__(self, config):
        """
        Initializations for the startup of the current wordclock plugin
        """
        # Get plugin name (according to the folder, it is contained in)
        self.name = os.path.dirname(__file__).split('/')[-1]
        self.pretty_name = "Seconds"
        self.description = "Shows the current seconds. The fool thinks no time flies;)"

	self.taw = time_seconds.time_seconds()

	self.bg_color = wcc.BLACK  # default background color
        self.word_color = wcc.WHITE  # default word color
        self.minute_color = wcc.BLACK  # default minute color

    def run(self, wcd, wci):
        """
        Displays time until aborted by user interaction on pin button_return
        """
        # Some initializations of the "previous" second
        prev_sec = -1

        while True:
            # Get current time
            now_sec = datetime.datetime.now().second
            # Check, if a second has passed (to render the new time)
            if prev_sec != now_sec:
                self.show_time(wcd, wci, now_sec)
                prev_sec = now_sec
            event = wci.waitForEvent(0.05)
            if (event == wci.EVENT_BUTTON_RETURN) \
                    or (event == wci.EVENT_EXIT_PLUGIN) \
		            or (event == wci.EVENT_NEXT_PLUGIN_REQUESTED):
                return

    def show_time(self, wcd, wci, currentSecond):
        # Set background color
        wcd.setColorToAll(self.bg_color, includeMinutes=True)
        #show seconds based on numbers defined in time_seconds
	for i in range(110, -1, -110/11):
		#previous seconds, dimming down
		taw_indices = self.taw.get_time(currentSecond-1 if currentSecond != 0 else 59)
		wcd.setColorBy1DCoordinates(taw_indices, wcc.Color(i, i, i))
		#current seconds
		taw_indices = self.taw.get_time(currentSecond)
		wcd.setColorBy1DCoordinates(taw_indices, self.word_color)
		wcd.show()
		time.sleep(0.05)
