
class time_dutch:
    """
    This class returns a given time as a range of LED-indices.
    Illuminating these LEDs represents the current time on a dutch WCA
    range(0,3) +  range(4,6): HET IS

    range(18,22) + range(51,55): VIJF OVER
    range(22,26) + range(51,55): TIEN OVER
    range(33,38) + range(51,55): KWART OVER
    range(26,33) + range(51,55): TWINTIG OVER
    range(18,22) + range(40,44) + range(55,59): VIJF VOOR HALF
    range(55,59): HALF
    range(18,22) + range(51,55) + range(55,59): VIJF OVER HALF
    range(26,33) + range(40,44): TWINTIG VOOR
    range(33,38) + range(40,44): KWART VOOR
    range(22,26) + range(40,44): TIEN VOOR
    range(18,22) + range(40,44): VIJF VOOR

    range(104,110): TWAALF
            range(66,69): EEN
            range(73,77): TWEE
            range(77,81): DRIE
            range(84,88): VIER
            range(62,66): VIJF
            range(114,116): ZES
            range(99,104): ZEVEN
            range(95,99): ACHT
            range(88,93): NEGEN
            range(110,114): TIEN
            range(81,84): ELF
            range(104,110): TWAALF

 self.full_hour= range(118,121)
    """

    def __init__(self):
        self.prefix = range(0,3) +  range(4,6)
        self.minutes=[[], \
            range(18,22) + range(51,55), \
            range(22,26) + range(51,55), \
            range(33,38) + range(51,55), \
            range(26,33) + range(51,55), \
            range(18,22) + range(40,44) + range(55,59), \
            range(55,59), \
            range(18,22) + range(51,55) + range(55,59), \
            range(26,33) + range(40,44), \
            range(33,38) + range(40,44), \
            range(22,26) + range(40,44), \
            range(18,22) + range(40,44) ]
        self.hours= [range(104,110), \
            range(66,69), \
            range(73,77), \
            range(77,81), \
            range(84,88), \
            range(62,66), \
            range(114,116), \
            range(99,104), \
            range(95,99), \
            range(88,93), \
            range(110,114), \
            range(81,84), \
            range(104,110)]
        self.full_hour= range(118,121)

    def get_time(self, time, withPrefix=True):
        hour=time.hour%12+(1 if time.minute/5 > 4 else 0)
        minute=time.minute/5
        # Assemble indices
        return  \
            (self.prefix if withPrefix else []) + \
            self.minutes[minute] + \
            self.hours[hour] + \
            ([60] if (hour == 1 and minute != 0) else []) + \
            (self.full_hour if (minute == 0) else [])

