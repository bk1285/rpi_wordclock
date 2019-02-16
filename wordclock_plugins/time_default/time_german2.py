class time_german2:
    """
    This class returns a given time as a range of LED-indices.
    Illuminating these LEDs represents the current time on a german WCA in alternative layout german2
    Credits to SebVoss
    """

    def __init__(self):
        self.prefix = range(0,2) +  range(3,6)
        self.minutes=[[], \
            range(7,11) + range(40,44), \
            range(11,15) + range(40,44), \
            range(26,33) + range(40,44), \
            range(15,22) + range(40,44), \
            range(7,11) + range(33,36) + range(44,48), \
            range(44,48), \
            range(7,11) + range(40,44) + range(44,48), \
            range(15,22) + range(33,36), \
            range(26,33) + range(33,36), \
            range(11,15) + range(33,36), \
            range(7,11) + range(33,36) ]
        self.hours= [range(94,99), \
            range(55,58), \
            range(62,66), \
            range(66,70), \
            range(73,77), \
            range(51,55), \
            range(77,82), \
            range(88,94), \
            range(84,88), \
            range(102,106), \
            range(99,103), \
            range(49,52), \
            range(94,99)]
        self.full_hour= range(107,110)

    def get_time(self, time, purist):
        hour=time.hour%12+(1 if time.minute/5 > 4 else 0)
        minute=time.minute/5
        # Assemble indices
        return  \
            (self.prefix if not purist else []) + \
            self.minutes[minute] + \
            self.hours[hour] + \
            ([58] if (hour == 1 and minute != 0) else []) + \
            (self.full_hour if (minute == 0) else [])

