class font_matrix:
    """
    This class returns a given time as a range of LED-indices.
    Illuminating these LEDs represents the current time on a german WCA
    """

    def __init__(self):
	self.replacement=[range(11,16) + range(22,24) + range(25,27) + [33] + [35] + [37] + range(44,47) + [48] + range(55,57) + range(58,60) + range (66,71) + range(77,79) + range(80,82) + range(88,93), \
	    []]
        self.a=[[24] + [34] + [36] + [44] + [48] + range(55,60) + [66] + [70] + [77] + [81] + [88] + [92], \
	    range(62,64) + [72] + [75] + [83] + [86] + range(95,98)]
	self.b=[range(22,26) + [33] + [37] + [44] + [48] + range(55,59) + [66] + [70] + [77] + [81] + range(88,92), \
	    [28] + [39] + [50] + range(61,64) + [72] + [75] + [83] + [86] + range(94,97)]
	self.c=[range(24,27) + [34] + [44] + [55] + [66] + [78] + range(90,93), \
	    range(52,54) + [62] + [73] + [84] + range(96,98)]
	self.d=[range(22,25) + [33] + [36] + [44] + [48] + [55] + [59] + [66] + [70] + [77] + [80] + range(88,91), \
	    [31] + [42] + [53] + range(62,65) + [72] + [75] + [83] + [86] + range(95,98)]
	self.e=[range(22,27) + [33] + [44] + range(55,59) + [66] + [77] + range(88,93), \
	    range(51,53) + [61] + [64] + range(72,76) + [83] + range(95,97)]
	self.f=[range(22,27) + [33] + [44] + range(55,59) + [66] + [77] + [88], \
	    range(30,32) + [40] + [51] + range(61,64) + [73] + [84] + [95]]
	self.g=[range(23,27) + [33] + [44] + [55] + [66] + range(69,71) + [77] + [81] + range(89,93), \
	    range(51,53) + [61] + [64] + [72] + [75] + range(84,87) + [97] + range(106,108)]
	self.h=[[22] + [26] + [33] + [37] + [44] + [48] + range(55,60) + [66] + [70] + [77] + [81] + [88] + [92], \
	    [28] + [39] + [50] + range(61,64) + [72] + [75] + [83] + [86] + [94] + [97]]

	self.charList = (self.replacement + \
		self.a + \
		self.b + \
		self.c + \
		self.d + \
		self.e + \
		self.f + \
		self.g + \
		self.h)
    def getC(self, currentC):
        return (self.charList[currentC*2] + \
	    self.charList[(currentC*2)+1])

    def getCharCount(self):
	return ((len(self.charList)/2)-1)
