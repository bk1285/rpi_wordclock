import datetime as dt

class time_italian():
    '''
    This class returns a given time as a range of LED-indices.
    Illuminating these LEDs represents the current time on a italian WCA
    '''

    def __init__(self):
        self.prefix = range(0,0)
        self.minutes=[[], \
            range(93,99) + range(77,78), \
            range(99,104) + range(77,78), \
            range(82,88) + range(79,81) + range(77,78), \
            range(88,93) + range(77,78), \
            range(88,99) + range(77,78), \
            range(105,110)+ range(77,78), \
            range(88,99) + range(73,77), \
            range(88,93) + range(73,77), \
            range(82,88) + range(73,77) + range(79,81), \
            range(99,104) + range(73,77), \
            range(93,99) + range(73,77) ]
        self.hours= [range(5,7) + range(0,4) +range(44,50), \
            range(13,17) + range(11,12), \
            range(18,21) + range(0,4) +  range(5,7), \
            range(22,25) + range(0,4) +  range(5,7), \
            range(55,62) + range(0,4) +  range(5,7), \
            range(66,72) + range(0,4) +  range(5,7), \
            range(63,66) + range(0,4) +  range(5,7), \
            range(50,55) + range(0,4) +  range(5,7), \
            range(25,29) + range(0,4) +  range(5,7), \
            range(29,33) + range(0,4) +  range(5,7), \
            range(33,38) + range(0,4) +  range(5,7), \
            range(38,44) + range(0,4) +  range(5,7), \
            range(44,50) + range(0,4) +  range(5,7)]
        self.full_hour= range(0,0)

    def get_time(self, time, withPrefix=True):
        hour=time.hour%12+(1 if time.minute/5 > 6 else 0)
        minute=time.minute/5
        # Assemble indices
        return  \
            (self.prefix if withPrefix else []) + \
            self.minutes[minute] + \
            self.hours[hour] + \
            (self.full_hour if (minute == 0) else [])
