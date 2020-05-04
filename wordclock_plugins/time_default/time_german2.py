class time_german2:
    """
    This class returns a given time as a range of LED-indices.
    Illuminating these LEDs represents the current time on a german WCA in alternative layout german2
    Credits to SebVoss
    """

    def __init__(self):
        self.prefix = list(range(0,2)) +  list(range(3,6))
        self.minutes=[[], \
            list(range(7,11)) + list(range(40,44)), \
            list(range(11,15)) + list(range(40,44)), \
            list(range(26,33)) + list(range(40,44)), \
            list(range(15,22)) + list(range(40,44)), \
            list(range(7,11)) + list(range(33,36)) + list(range(44,48)), \
            list(range(44,48)), \
            list(range(7,11)) + list(range(40,44)) + list(range(44,48)), \
            list(range(15,22)) + list(range(33,36)), \
            list(range(26,33)) + list(range(33,36)), \
            list(range(11,15)) + list(range(33,36)), \
            list(range(7,11)) + list(range(33,36)) ]
        self.hours= [list(range(94,99)), \
            list(range(55,58)), \
            list(range(62,66)), \
            list(range(66,70)), \
            list(range(73,77)), \
            list(range(51,55)), \
            list(range(77,82)), \
            list(range(88,94)), \
            list(range(84,88)), \
            list(range(102,106)), \
            list(range(99,103)), \
            list(range(49,52)), \
            list(range(94,99))]
        self.full_hour= list(range(107,110))

    def get_time(self, time, purist):
        hour=time.hour%12+(1 if time.minute/5 > 4 else 0)
        minute=time.minute/5
        # Assemble indices
        return  \
            (self.prefix if not purist else []) + \
            self.minutes[int(minute)] + \
            self.hours[hour] + \
            ([58] if (hour == 1 and minute != 0) else []) + \
            (self.full_hour if (minute == 0) else [])

