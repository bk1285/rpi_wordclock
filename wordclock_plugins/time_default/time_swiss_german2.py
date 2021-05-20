# coding: utf8

class time_swiss_german2:
    """
    This class returns a given time as a range of LED-indices.
    Illuminating these LEDs represents the current time on a swiss_german WCA
    """

    def __init__(self):
        self.prefix = [0] + list(range(2,5)) +  list(range(6,10))  # -> D ZYT ISCH
        self.minutes=[[], \
            # -> FÜF AB
            list(range(12,15)) + list(range(36,38)), \
            # -> ZÄÄ AB
            list(range(29,32)) + list(range(36,38)), \
            # -> VIERTU AB
            list(range(15,21)) + list(range(36,38)), \
            # -> ZWÄNZG AB
            list(range(22,28)) + list(range(36,38)), \
            # -> FÜF VOR HAUBI
            list(range(12,15)) + list(range(33,36)) + list(range(39,44)), \
            # -> HAUBI
            list(range(39,44)), \
            # -> FÜF AB HAUBI
            list(range(12,15)) + list(range(36,38)) + list(range(39,44)), \
            # -> ZWÄNZG VOR
            list(range(22,28)) + list(range(33,36)), \
            # -> VIERTU VOR
            list(range(15,21)) + list(range(33,36)), \
            # -> ZÄÄ VOR
            list(range(29,32)) + list(range(33,36)), \
            # -> FÜF VOR
            list(range(12,15)) + list(range(33,36)) ]
        self.hours= [list(range(104,110)), \
            # -> EIS
            list(range(100,103)), \
            # -> ZWÖI
            list(range(44,48)), \
            # -> DRÜ
            list(range(84,87)), \
            # -> VIERI
            list(range(88,93)), \
            # -> FÜFI
            list(range(66,70)), \
            # -> SÄCHSI
            list(range(48,54)), \
            # -> SIBNI
            list(range(71,76)), \
            # -> ACHTI
            list(range(55,60)), \
            # -> NÜNI
            list(range(94,98)), \
            # -> ZÄNI
            list(range(79,83)), \
            # -> EUFI
            list(range(62,66)), \
            # -> ZWÖUFI
            list(range(104,110))]
        self.full_hour= []

    def get_time(self, time, purist):
        hour=time.hour%12+(1 if time.minute/5 > 4 else 0)
        minute=time.minute/5
        # Assemble indices
        return  \
            (self.prefix if not purist else []) + \
            self.minutes[int(minute)] + \
            self.hours[hour]
