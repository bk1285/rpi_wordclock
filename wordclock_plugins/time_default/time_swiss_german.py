# coding: utf8

import datetime as dt

class time_swiss_german():
    '''
    This class returns a given time as a range of LED-indices.
    Illuminating these LEDs represents the current time on a swiss_german WCA
    '''

    def __init__(self):
        self.prefix = range(0,2) +  range(3,7)  # -> ES ISCH
        self.minutes=[[], \
            # -> FÜF AB
            range(8,11) + range(33,35), \
            # -> ZÄÄ AB
            range(19,22) + range(33,35), \
            # -> VIERTU AB
            range(11,17) + range(33,35), \
            # -> ZWÄNZG AB
            range(22,28) + range(33,35), \
            # -> FÜF VOR HAUBI
            range(8,11) + range(30,33) + range(36,41), \
            # -> HAUBI
            range(36,41), \
            # -> FÜF AB HAUBI
            range(8,11) + range(33,35) + range(36,41), \
            # -> ZWÄNZG VOR
            range(22,28) + range(30,33), \
            # -> VIERTU VOR
            range(11,17) + range(30,33), \
            # -> ZÄÄ VOR
            range(19,22) + range(30,33), \
            # -> FÜF VOR
            range(8,11) + range(30,33) ]
            # -> ZWÖUFI
        self.hours= [range(99,105), \
            # -> EIS
            range(44,47), \
            # -> ZWÖI
            range(47,51), \
            # -> DRÜ
            range(52,55), \
            # -> VIERI
            range(55,60), \
            # -> FÜFI
            range(60,64), \
            # -> SÄCHSI
            range(66,72), \
            # -> SIBNI
            range(72,77), \
            # -> ACHTI
            range(77,82), \
            # -> NÜNI
            range(82,86), \
            # -> ZÄNI
            range(88,92), \
            # -> EUFI
            range(95,99), \
            # -> ZWÖUFI
            range(99,105)]
        self.full_hour= range(107,110)

    def get_time(self, time, withPrefix=True):
        hour=time.hour%12+(1 if time.minute/5 > 4 else 0)
        minute=time.minute/5
        # Assemble indices
        return  \
            (self.prefix if withPrefix else []) + \
            self.minutes[minute] + \
            self.hours[hour]
