
class time_swedish:
    """
    This class returns a given time as a range of LED-indices.
    Illuminating these LEDs represents the current time on a swedish WCA
    """

    def __init__(self):
        self.prefix = list(range(0,7)) +  list(range(8,10))
        self.minutes=[[], \
            list(range(11,14)) + list(range(44,48)), \
            list(range(17,20)) + list(range(44,48)), \
            list(range(22,27)) + list(range(44,48)), \
            list(range(33,38)) + list(range(44,48)), \
            list(range(11,14)) + list(range(15,16)) + list(range(51,55)), \
            list(range(51,55)), \
            list(range(11,14)) + list(range(44,48)) + list(range(51,55)), \
            list(range(33,38)) + list(range(39,40)), \
            list(range(22,27)) + list(range(28,29)), \
            list(range(17,20)) + list(range(21,22)), \
            list(range(11,14)) + list(range(15,16)) ]
        self.hours= [list(range(106,110)), \
            list(range(55,58)), \
            list(range(63,66)), \
            list(range(66,69)), \
            list(range(73,77)), \
            list(range(77,80)), \
            list(range(85,88)), \
            list(range(88,91)), \
            list(range(91,95)), \
            list(range(96,99)), \
            list(range(99,102)), \
            list(range(102,106)), \
            list(range(106,110))]
#        self.full_hour= list(range(107,110))

    def get_time(self, time, purist):
        hour=time.hour%12+(1 if time.minute//5 > 4 else 0)
        minute=time.minute//5
        # Assemble indices
        return  \
            (self.prefix if not purist else []) + \
            self.minutes[minute] + \
            self.hours[hour]# + \
#            ([60] if (hour == 1 and minute != 0) else [])# + \
#            (self.full_hour if (minute == 0) else [])

