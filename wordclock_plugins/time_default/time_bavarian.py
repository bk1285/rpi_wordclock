import datetime as dt

class time_bavarian():
    '''
    This class returns a given time as a range of LED-indices.
    Illuminating these LEDs represents the current time on a german WCA
    '''

    def __init__(self):
        self.prefix = range(0,2) +  range(3,6)
        self.minutes=[[], \
            range(7,11) + range(35,39), \
            range(11,15) + range(35,39), \
            range(26,33), \
            range(11,15) + range(39,42) + range(44,48), \
            range(7,11) + range(39,42) + range(44,48), \
            range(44,48), \
            range(7,11) + range(35,39) + range(44,48), \
            range(11,15) + range(35,39) + range(44,48), \
            range(22,33), \
            range(11,15) + range(39,42), \
            range(7,11) + range(39,42) ]
        self.hours= [range(49,54), \
            range(57,60), \
            range(55,59), \
            range(67,71), \
            range(84,88), \
            range(73,77), \
            range(100,105), \
            range(60,66), \
            range(89,93), \
            range(80,84), \
            range(93,97), \
            range(77,80), \
            range(49,54)]
        self.full_hour= range(107,110)

    def get_time(self, time, withPrefix=True):
        hour=time.hour%12+(1 if time.minute/5 > 2 else 0)
        minute=time.minute/5
        # Assemble indices
        return  \
            (self.prefix if withPrefix else []) + \
            self.minutes[minute] + \
            self.hours[hour] + \
            ([60] if (hour == 1 and minute != 0) else []) + \
            (self.full_hour if (minute == 0) else [])

