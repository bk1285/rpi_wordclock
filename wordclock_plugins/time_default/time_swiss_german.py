# coding: utf8


class time_swiss_german:
    """
    This class returns a given time as a range of LED-indices.
    Illuminating these LEDs represents the current time on a swiss_german WCA
    """

    def __init__(self):
        self.prefix = list(range(0,2)) +  list(range(3,7))  # -> ES ISCH
        self.minutes=[[], \
            # -> FÜF AB
            list(range(8,11)) + list(range(33,35)), \
            # -> ZÄÄ AB
            list(range(19,22)) + list(range(33,35)), \
            # -> VIERTU AB
            list(range(11,17)) + list(range(33,35)), \
            # -> ZWÄNZG AB
            list(range(22,28)) + list(range(33,35)), \
            # -> FÜF VOR HAUBI
            list(range(8,11)) + list(range(30,33)) + list(range(36,41)), \
            # -> HAUBI
            list(range(36,41)), \
            # -> FÜF AB HAUBI
            list(range(8,11)) + list(range(33,35)) + list(range(36,41)), \
            # -> ZWÄNZG VOR
            list(range(22,28)) + list(range(30,33)), \
            # -> VIERTU VOR
            list(range(11,17)) + list(range(30,33)), \
            # -> ZÄÄ VOR
            list(range(19,22)) + list(range(30,33)), \
            # -> FÜF VOR
            list(range(8,11)) + list(range(30,33)) ]
            # -> ZWÖUFI
        self.hours= [list(range(99,105)), \
            # -> EIS
            list(range(44,47)), \
            # -> ZWÖI
            list(range(47,51)), \
            # -> DRÜ
            list(range(52,55)), \
            # -> VIERI
            list(range(55,60)), \
            # -> FÜFI
            list(range(60,64)), \
            # -> SÄCHSI
            list(range(66,72)), \
            # -> SIBNI
            list(range(72,77)), \
            # -> ACHTI
            list(range(77,82)), \
            # -> NÜNI
            list(range(82,86)), \
            # -> ZÄNI
            list(range(88,92)), \
            # -> EUFI
            list(range(95,99)), \
            # -> ZWÖUFI
            list(range(99,105))]
        self.full_hour= list(range(107,110))

    def get_time(self, time, purist):
        hour=time.hour%12+(1 if time.minute//5 > 4 else 0)
        minute=time.minute//5
        # Assemble indices
        return  \
            (self.prefix if not purist else []) + \
            self.minutes[int(minute)] + \
            self.hours[hour]
