class time_french:
    """
    This class returns a given time as a range of LED-indices.
    Illuminating these LEDs represents the current time on an french WCA
    """

    def __init__(self):
        self.prefix = range(0,2) + range(3,6) # -> IL EST
        self.hours= [range(28,33), \
            # -> UNE
            range(7,10), \
            # -> DEUX
            range(11,15), \
            # -> TROIS
            range(17,22), \
            # -> QUATRE
            range(22,28), \
            # -> CINQ
            range(33,37), \
            # -> SIX
            range(37,40), \
            # -> SEPT
            range(40,44), \
            # -> HUIT
            range(44,48), \
            # -> NEUF
            range(48,52), \
            # -> DIX
            range(52,55), \
            # -> ONZE
            range(55,59), \
            # -> DOUZE
            range(28,33)]
        self.interfix= [ \
            # -> HEURE
            range(60,65), \
            # -> HEURES
            range(60,66)]
        self.minutes=[[], \
            # -> CINQ
            range(94,98), \
            # -> DIX
            range(74,77), \
            # -> ET QUART
            range(77,79) + range(80,85), \
            # -> VINGT
            range(88,93), \
            # -> VINGT-CINQ
            range(88,98), \
            # -> ET DEMIE
            range(99,101) + range(102,107), \
            # -> MOINS VINGT-CINQ
            range(66,71) + range(88,98), \
            # -> MOINS VINGT
            range(66,71) + range(88,93), \
            # -> MOINS QUART
            range(66,71) + range(80,85), \
            # -> MOINS DIX
            range(66,71) + range(74,77), \
            # -> MOINS CINQ
            range(66,71) + range(94,98)]

    def get_time(self, time, purist):
        hour=time.hour % 12+(1 if time.minute//5 >= 7 else 0)
        minute=time.minute//5
        # Assemble indices
        return  \
            (self.prefix if not purist else []) + \
            self.hours[hour] + \
            (self.interfix[0] if (hour == 1) else self.interfix[1]) + \
            self.minutes[minute]
