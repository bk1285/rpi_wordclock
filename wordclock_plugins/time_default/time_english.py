""" Provided by Alexandre"""


class time_english:
    """
    This class returns a given time as a range of LED-indices.
    Illuminating these LEDs represents the current time on an english WCA
    """

    def __init__(self):
        self.prefix = list(range(0,2)) +  list(range(3,5)) # -> IT IS
        self.minutes=[[], \
            # -> FIVE PAST
            list(range(28,32)) + list(range(44,48)), \
            # -> TEN PAST
            list(range(38,41)) + list(range(44,48)), \
            # -> QUARTER PAST
            list(range(13,20)) + list(range(44,48)), \
            # -> TWENTY PAST
            list(range(22,28)) + list(range(44,48)), \
            # -> TWENTYFIVE PAST
            list(range(22,32)) + list(range(44,48)), \
            # -> HALF PAST
            list(range(33,37)) + list(range(44,48)), \
            # -> TWENTYFIVE TO
            list(range(22,32)) + list(range(42,44)), \
            # -> TWENTY TO
            list(range(22,28)) + list(range(42,44)), \
            # -> QUARTER TO
            list(range(13,20)) + list(range(42,44)), \
            # -> TEN TO
            list(range(38,41)) + list(range(42,44)), \
            # -> FIVE TO
            list(range(28,32)) + list(range(42,44)) ]
            # -> TWELVE
        self.hours= [list(range(93,99)), \
            # -> ONE
            list(range(55,58)), \
            # -> TWO
            list(range(74,77)), \
            # -> THREE
            list(range(61,66)), \
            # -> FOUR
            list(range(66,70)), \
            # -> FIVE
            list(range(70,74)), \
            # -> SIX
            list(range(58,61)), \
            # -> SEVEN
            list(range(88,93)), \
            # -> EIGHT
            list(range(77,82)), \
            # -> NINE
            list(range(51,55)), \
            # -> TEN
            list(range(99,102)),\
            # -> ELEVEN
            list(range(82,88)), \
            # -> TWELVE
            list(range(93,99))]
        # -> OCLOCK
        self.full_hour= list(range(104,110))

    def get_time(self, time, purist):
        hour=time.hour % 12+(1 if time.minute//5 >= 7 else 0)
        minute=time.minute//5
        # Assemble indices
        return  \
            (self.prefix if not purist else []) + \
            self.minutes[minute] + \
            self.hours[hour] + \
            (self.full_hour if (minute == 0) else [])
