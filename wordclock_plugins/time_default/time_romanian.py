""" Provided by Darius"""


class time_romanian:
    """
    This class returns a given time as a range of LED-indices.
    Illuminating these LEDs represents the current time on a romanian WCA
    """

    def __init__(self):
        self.prefix = range(0,4) +  range(6,9) # -> ESTE ORA
        self.minutes=[[], \
            # -> SI CINCI
            range(97,99) + range(99,104), \
            # -> SI ZECE
            range(66,68) + range(82,86), \
            # -> SI UN SFERT
            range(66,68) + range(86,88) + range(105,110), \
            # -> SI DOUAZECI
            range(66,68) + range(88,96), \
            # -> SI DOUAZECI SI CINCI
            range(66,68) + range(88,96) + range(97,99) + range(99,104), \
            # -> SI TREIZECI
            range(66,68) + range(69,77), \
            # -> FARA DOUAZECI SI CINCI
            range(77,81) + range(88,96) + range(97,99) + range(99,104), \
            # -> FARA DOUAZECI
            range(77,81) + range(88,96), \
            # -> FARA UN SFERT
            range(77,81) + range(86,88) + range(105,110), \
            # -> FARA ZECE
            range(77,81) + range(82,96), \
            # -> FARA CINCI
            range(77,81) + range(99,104) ]
            # -> DOUA SPRE ZECE
        self.hours= [range(11,15) + range(16,19) + range(28,32), \
            # -> UNU
            range(48,51), \
            # -> DOUA
            range(11,15), \
            # -> TREI
            range(51,55), \
            # -> PATRU
            range(44,49), \
            # -> CINCI
            range(50,65), \
            # -> SASE
            range(40,44), \
            # -> SAPTE
            range(55,60), \
            # -> OPT
            range(37,40), \
            # -> NOUA
            range(33,37), \
            # -> ZECE
            range(28,32),\
            # -> UNSPREZECE
            range(22,32), \
            # -> DOUA SPRE ZECE
            range(11,15) + range(16,19) + range(28,32)]
        self.full_hour= range(0,0)

    def get_time(self, time, purist):
        hour=time.hour % 12+(1 if time.minute/5 >= 7 else 0)
        minute=time.minute/5
        # Assemble indices
        return  \
            (self.prefix if not purist else []) + \
            self.minutes[minute] + \
            self.hours[hour] + \
            (self.full_hour if (minute == 0) else [])
