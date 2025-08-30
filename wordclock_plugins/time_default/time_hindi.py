
class time_hindi:
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
        self.prefix = list(range(107,110))
        self.minutes=[[], \
            list(range(74,80)) + list(range(95,100)) + list(range(100,105)), \
            list(range(74,80)) + list(range(87,90)) + list(range(100,105)), \
            list(range(10,14)), \
            list(range(74,80)) + list(range(90,93)) + list(range(100,105)), \
            list(range(74,80)) + list(range(80,85)) + list(range(100,105)), \
            list(range(5,10)), \
            list(range(65,72)) + list(range(80,85)) + list(range(100,105)), \
            list(range(65,72)) + list(range(90,93)) + list(range(100,105)), \
            list(range(0,5)), \
            list(range(65,72)) + list(range(87,90)) + list(range(100,105)), \
            list(range(65,72)) + list(range(95,100)) + list(range(100,105)) ]
        self.hours= [list(range(50,55)), \
            list(range(35,37)), \
            list(range(18,20)), \
            list(range(37,40)), \
            list(range(46,50)), \
            list(range(30,35)), \
            list(range(33,36)), \
            list(range(22,25)), \
            list(range(23,26)), \
            list(range(55,58)), \
            list(range(20,23)), \
            list(range(40,46)), \
            list(range(50,55))]
        self.full_hour= list(range(60,64))

    def get_time(self, time, purist):
        hour=time.hour%12+(1 if time.minute//5 > 6 else 0)
        minute=time.minute//5
        
        if (minute == 6 and hour == 1):
        	return (self.prefix if not purist else []) + \
        		list(range(26,30)) + \
        		self.full_hour
        if (minute == 6 and hour == 2):
        	return (self.prefix if not purist else []) + \
        		list(range(14,18)) + \
        		self.full_hour
        # Assemble indices
        return  \
            (self.prefix if not purist else []) + \
            self.minutes[int(minute)] + \
            self.hours[hour] + \
            (self.full_hour if (minute == 0) else [])

