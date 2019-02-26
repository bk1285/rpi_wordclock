import os
#import font_matrix
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

	#self.taw = font_matrix.font_matrix()
	self.currentText = 0
	self.textBox = ['first Text', 'second Text 4 fun!', '3rd Text']

	self.bg_color = wcc.BLACK  # default background color
        self.word_color = wcc.WHITE  # default word color
        self.minute_color = wcc.BLACK  # default minute color

    def run(self, wcd, wci):
        """
        Displays time until aborted by user interaction on pin button_return
        """
	self.showText(wcd, wci, self.textBox[self.currentText])
        while True:
	    event = wci.waitForEvent(0.2)
	    if (event == wci.EVENT_BUTTON_RIGHT):
		self.currentText += 1
		if self.currentText > len(self.textBox)-1: self.currentText = 0
		self.showText(wcd, wci, self.textBox[self.currentText])

	    if (event == wci.EVENT_BUTTON_LEFT):
		self.currentText -= 1
		if self.currentText < 0: self.currentText = len(self.textBox)-1
		self.showText(wcd, wci, self.textBox[self.currentText])

            if (event == wci.EVENT_BUTTON_RETURN) \
                    or (event == wci.EVENT_EXIT_PLUGIN) \
		    or (event == wci.EVENT_NEXT_PLUGIN_REQUESTED):
		return

    def showText(self, wcd, wci, text):
        # Set background color
        wcd.setColorToAll(self.bg_color, includeMinutes=True)
	
	#taw_indices = self.taw.getC(currentC)
	#wcd.setColorBy1DCoordinates(wcd.strip, taw_indices, self.word_color)
	wcd.show()
