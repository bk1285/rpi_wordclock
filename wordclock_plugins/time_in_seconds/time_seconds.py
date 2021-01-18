
class time_seconds:
    """
    This class returns a given time as a range of LED-indices.
    Illuminating these LEDs represents the current time on a german WCA
    """

    def __init__(self):
        self.leftDigit=[range(23,26) + range(33,34) + range(37,38) + range(44,45) + range(47,49) + range(55,56) + range(57,58) + range(59,60) + range(66,68) + range(70,71) + range(77,78) + range(81,82) + range(89,92), \
            range(24,25) + range(34,36) + range(46,47) + range(57,58) + range(68,69) + range(79,80) + range(89,92), \
            range(23,26) + range(33,34) + range(37,38) + range(48,49) + range(58,59) + range(68,69) + range(78,79) + range(88,93), \
            range(22,27) + range(36,37) + range(46,47) + range(58,59) + range(70,71) + range(77,78) + range(81,82) + range(89,92), \
            range(25,26) + range(35,37) + range(45,46) + range(47,48) + range(55,56) + range(58,59) + range(66,71) + range(80,81) + range(91,92), \
	    range(22,27) + range(33,34) + range(44,48) + range(59,60) + range(70,71) + range(77,78) + range(81,82) + range(89,92), \
            range(24,26) + range(34,35) + range(44,45) + range(55,59) + range(66,67) + range(70,71) + range(77,78) + range(81,82) + range(89,92), \
            range(22,27) + range(37,38) + range(47,48) + range(57,58) + range(67,68) + range(78,79) + range(89,90), \
            range(23,26) + range(33,34) + range(37,38) + range(44,45) + range(48,49) + range(56,59) + range(66,67) + range(70,71) + range(77,78) + range(81,82) + range(89,92), \
            range(23,26) + range(33,34) + range(37,38) + range(44,45) + range(48,49) + range(56,60) + range(70,71) + range(80,81) + range(89,91) ]

    def get_time(self, seconds):
        decimal=seconds/10
	ones=seconds%10
	self.rightDigit = []
	for i in self.leftDigit[ones]:
		self.rightDigit.insert(i, i+6)
        # Assemble indices
        return  \
            (self.leftDigit[decimal] + \
             self.rightDigit)

