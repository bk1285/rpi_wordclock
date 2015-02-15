import datetime as dt

class time_dutch():
    '''
    This class returns a given time as a range of LED-indices.
    Illuminating these LEDs represents the current time on a dutch WCA
    range(0,3) +  range(4,6): HET IS

    range(7,11) + range(40,44): VIJF OVER
    range(11,15) + range(40,44): TIEN OVER
    range(22,27) + range(40,44): KWART OVER
    range(15,22) + range(40,44): TWINTIG OVER
    range(7,11) + range(29,33) + range(44,48): VIJF VOOR HALF
    range(44,48): HALF
    range(7,11) + range(40,44) + range(44,48): VIJF OVER HALF
    range(15,22) + range(29,33): TWINTIG VOOR
    range(22,27) + range(29,33): KWART VOOR
    range(11,15) + range(29,33): TIEN VOOR
    range(7,11) + range(29,33): VIJF VOOR

    range(93,99): TWAALF
            range(55,58): EEN
            range(62,66): TWEE
            range(66,70): DRIE
            range(73,77): VIER
            range(51,55): VIJF
            range(103,106): ZES
            range(88,93): ZEVEN
            range(84,88): ACHT
            range(77,82): NEGEN
            range(99,103): TIEN
            range(70,73): ELF
            range(93,99): TWAALF
       
 self.full_hour= range(107,110)
    '''

    def __init__(self):
        self.prefix = range(0,3) +  range(4,6)
        self.minutes=[[], \
            range(7,11) + range(40,44), \
            range(11,15) + range(40,44), \
            range(22,27) + range(40,44), \
            range(15,22) + range(40,44), \
            range(7,11) + range(29,33) + range(44,48), \
            range(44,48), \
            range(7,11) + range(40,44) + range(44,48), \
            range(15,22) + range(29,33), \
            range(22,27) + range(29,33), \
            range(11,15) + range(29,33), \
            range(7,11) + range(29,33) ]
        self.hours= [range(93,99), \
            range(55,58), \
            range(62,66), \
            range(66,70), \
            range(73,77), \
            range(51,55), \
            range(103,106), \
            range(88,93), \
            range(84,88), \
            range(77,82), \
            range(99,103), \
            range(70,73), \
            range(93,99)]
        self.full_hour= range(107,110)

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

