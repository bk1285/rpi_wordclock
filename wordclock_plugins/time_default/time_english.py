""" Provided by Alexandre"""


class time_english:
    """
    This class returns a given time as a range of LED-indices.
    Illuminating these LEDs represents the current time on an english WCA
    """

    def __init__(self):
        self.prefix = range(0,2) +  range(3,5) # -> IT IS
        self.minutes=[[], \
            # -> FIVE PAST
            range(28,32) + range(44,48), \
            # -> TEN PAST
            range(38,41) + range(44,48), \
            # -> QUARTER PAST
            range(13,20) + range(44,48), \
            # -> TWENTY PAST
            range(22,28) + range(44,48), \
            # -> TWENTYFIVE PAST
            range(22,32) + range(44,48), \
            # -> HALF PAST
            range(33,37) + range(44,48), \
            # -> TWENTYFIVE TO
            range(22,32) + range(42,44), \
            # -> TWENTY TO
            range(22,28) + range(42,44), \
            # -> QUARTER TO
            range(13,20) + range(42,44), \
            # -> TEN TO
            range(38,41) + range(42,44), \
            # -> FIVE TO
            range(28,32) + range(42,44) ]
            # -> TWELVE
        self.hours= [range(93,99), \
            # -> ONE
            range(55,58), \
            # -> TWO
            range(74,77), \
            # -> THREE
            range(61,66), \
            # -> FOUR
            range(66,70), \
            # -> FIVE
            range(70,74), \
            # -> SIX
            range(58,61), \
            # -> SEVEN
            range(88,93), \
            # -> EIGHT
            range(77,82), \
            # -> NINE
            range(51,55), \
            # -> TEN
            range(99,102),\
            # -> ELEVEN
            range(82,88), \
            # -> TWELVE
            range(93,99)]
        # -> OCLOCK
        self.full_hour= range(104,110)

    def get_time(self, time, purist):
        hour=time.hour % 12+(1 if time.minute/5 >= 7 else 0)
        minute=time.minute/5
        # Assemble indices
        return  \
            (self.prefix if not purist else []) + \
            self.minutes[minute] + \
            self.hours[hour] + \
            (self.full_hour if (minute == 0) else [])
