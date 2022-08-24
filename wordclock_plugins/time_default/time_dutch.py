
class time_dutch:
    """
    This class returns a given time as a range of LED-indices.
    Illuminating these LEDs represents the current time on a dutch WCA 11x10

    range(0,3) +  range(4,6): HET IS

    range(7,11) + range(40,44): VIJF OVER
    range(11,15) + range(40,44): TIEN OVER
    range(28,33) + range(40,44): KWART OVER
    range(11,15) + range(18,22) + range(33,37): TIEN VOOR HALF
    range(7,11) + range(18,22) + range(33,37): VIJF VOOR HALF
    range(33,37): HALF
    range(7,11) + range(22,26) + range(33,37): VIJF OVER HALF
    range(11,15) + range(22,26) + range(33,37): TIEN OVER HALF
    range(28,33) + range(44,48): KWART VOOR
    range(11,15) + range(44,48): TIEN VOOR
    range(7,11) + range(44,48): VIJF VOOR

    range(99,105): TWAALF
            range(51,54): EEN
            range(55,59): TWEE
            range(62,66): DRIE
            range(66,70): VIER
            range(70,74): VIJF
            range(74,77): ZES
            range(77,82): ZEVEN
            range(88,92): ACHT
            range(83,88): NEGEN
            range(91,95): TIEN
            range(96,99): ELF
            range(99,105): TWAALF

    self.full_hour= range(107,110)
    """

    def __init__(self):
        self.prefix = list(range(0,3)) +  list(range(4,6))
        self.minutes=[[], \
            list(range(7,11)) + list(range(40,44)), \
            list(range(11,15)) + list(range(40,44)), \
            list(range(28,33)) + list(range(40,44)), \
            list(range(11,15)) + list(range(18,22)) + list(range(33,37)), \
            list(range(7,11)) + list(range(18,22)) + list(range(33,37)), \
            list(range(33,37)), \
            list(range(7,11)) + list(range(22,26)) + list(range(33,37)), \
            list(range(11,15)) + list(range(22,26)) + list(range(33,37)), \
            list(range(28,33)) + list(range(44,48)), \
            list(range(11,15)) + list(range(44,48)), \
            list(range(7,11)) + list(range(44,48)) ]
        self.hours= [list(range(99,105)), \
            list(range(51,54)), \
            list(range(55,59)), \
            list(range(62,66)), \
            list(range(66,70)), \
            list(range(70,74)), \
            list(range(74,77)), \
            list(range(77,82)), \
            list(range(88,92)), \
            list(range(83,88)), \
            list(range(91,95)), \
            list(range(96,99)), \
            list(range(99,105))]
        self.full_hour= list(range(107,110))

    def get_time(self, time, purist):
        hour=time.hour%12+(1 if time.minute//5 > 3 else 0)
        minute=time.minute//5
        # Assemble indices
        return  \
            (self.prefix if not purist else []) + \
            self.minutes[int(minute)] + \
            self.hours[hour] + \
            (self.full_hour if (minute == 0) else [])

