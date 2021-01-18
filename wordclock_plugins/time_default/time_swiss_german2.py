# coding: utf8

class time_swiss_german2:
    """
    This class returns a given time as a range of LED-indices.
    Illuminating these LEDs represents the current time on a swiss_german WCA
    """

    def __init__(self):
        self.prefix = [0] + range(2,5) +  range(6,10)  # -> D ZYT ISCH
        self.minutes=[[], \
            # -> FÜF AB
            range(12,15) + range(36,38), \
            # -> ZÄÄ AB
            range(29,32) + range(36,38), \
            # -> VIERTU AB
            range(15,21) + range(36,38), \
            # -> ZWÄNZG AB
            range(22,28) + range(36,38), \
            # -> FÜF VOR HAUBI
            range(12,15) + range(33,36) + range(39,44), \
            # -> HAUBI
            range(39,44), \
            # -> FÜF AB HAUBI
            range(12,15) + range(36,38) + range(39,44), \
            # -> ZWÄNZG VOR
            range(22,28) + range(33,36), \
            # -> VIERTU VOR
            range(15,21) + range(33,36), \
            # -> ZÄÄ VOR
            range(29,32) + range(33,36), \
            # -> FÜF VOR
            range(12,15) + range(33,36) ]
        self.hours= [range(104,110), \
            # -> EIS
            range(100,103), \
            # -> ZWÖI
            range(44,48), \
            # -> DRÜ
            range(84,87), \
            # -> VIERI
            range(88,93), \
            # -> FÜFI
            range(66,70), \
            # -> SÄCHSI
            range(48,54), \
            # -> SIBNI
            range(71,76), \
            # -> ACHTI
            range(55,60), \
            # -> NÜNI
            range(94,98), \
            # -> ZÄNI
            range(79,83), \
            # -> EUFI
            range(62,66), \
            # -> ZWÖUFI
            range(104,110)]
        self.full_hour= []

    def get_time(self, time, purist):
        hour=time.hour%12+(1 if time.minute/5 > 4 else 0)
        minute=time.minute/5
        # Assemble indices
        return  \
            (self.prefix if not purist else []) + \
            self.minutes[minute] + \
            self.hours[hour]
