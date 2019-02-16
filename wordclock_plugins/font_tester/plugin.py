import os
import font_matrix
import wordclock_tools.wordclock_colors as wcc

class plugin:
    """
    
    Credits: plotaBot
    """

    def __init__(self, config):
        """
        Initializations for the startup of the current wordclock plugin
        """
        # Get plugin name (according to the folder, it is contained in)
        self.name = os.path.dirname(__file__).split('/')[-1]
        self.pretty_name = "Font-Tester"
        self.description = "Displays all characters set in font_matrix"

	self.taw = font_matrix.font_matrix()
	self.currentC = 0

	self.bg_color = wcc.BLACK  # default background color
        self.word_color = wcc.WHITE  # default word color
        self.minute_color = wcc.BLACK  # default minute color

    def run(self, wcd, wci):
        """
        Displays time until aborted by user interaction on pin button_return
        """
	self.showC(wcd, wci, self.currentC)
        while True:
	    event = wci.waitForEvent(0.2)
	    if (event == wci.EVENT_BUTTON_RIGHT):
		self.currentC += 1
		if self.currentC > self.taw.getCharCount(): self.currentC = 0
		self.showC(wcd, wci, self.currentC)

	    if (event == wci.EVENT_BUTTON_LEFT):
		self.currentC -= 1
		if self.currentC < 0: self.currentC = self.taw.getCharCount()
		self.showC(wcd, wci, self.currentC)

            if (event == wci.EVENT_BUTTON_RETURN) \
                    or (event == wci.EVENT_EXIT_PLUGIN) \
		    or (event == wci.EVENT_NEXT_PLUGIN_REQUESTED):
		return

    def showC(self, wcd, wci, currentC):
        # Set background color
        wcd.setColorToAll(self.bg_color, includeMinutes=True)
	
	taw_indices = self.taw.getC(currentC)
	wcd.setColorBy1DCoordinates(wcd.strip, taw_indices, self.word_color)
	wcd.show()
