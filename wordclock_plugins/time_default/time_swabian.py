
class time_swabian:
    """
    This class returns a given time as a range of LED-indices.
    Illuminating these LEDs represents the current time on a german WCA in swabian
    """

    def __init__(self):
        self.prefix = list(range(0,2)) +  list(range(3,6))
        self.minutes=[[], \
            list(range(7,11)) + list(range(35,39)), \
            list(range(11,15)) + list(range(35,39)), \
            list(range(26,33)), \
            list(range(11,15)) + list(range(39,42)) + list(range(44,48)), \
            list(range(7,11)) + list(range(39,42)) + list(range(44,48)), \
            list(range(44,48)), \
            list(range(7,11)) + list(range(35,39)) + list(range(44,48)), \
            list(range(15,22)) + list(range(39,42)), \
            list(range(22,33)), \
            list(range(11,15)) + list(range(39,42)), \
            list(range(7,11)) + list(range(39,42)) ]
        self.hours= [list(range(49,54)), \
            list(range(57,60)), \
            list(range(55,59)), \
            list(range(67,71)), \
            list(range(84,88)), \
            list(range(73,77)), \
            list(range(100,105)), \
            list(range(60,66)), \
            list(range(89,93)), \
            list(range(80,84)), \
            list(range(93,97)), \
            list(range(77,80)), \
            list(range(49,54))]
        self.full_hour= list(range(107,110))

    def get_time(self, time, purist):
        hour=time.hour%12+(1 if time.minute//5 > 2 else 0)
        minute=time.minute//5
        # Assemble indices
        return  \
            (self.prefix if not purist else []) + \
            self.minutes[minute] + \
            self.hours[hour] + \
            ([60] if (hour == 1 and minute != 0) else []) + \
            (self.full_hour if (minute == 0) else [])
