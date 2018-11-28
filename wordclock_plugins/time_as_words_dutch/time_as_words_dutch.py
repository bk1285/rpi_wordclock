
class time_as_words_dutch():
    """
    This class returns a given time as words (string)::
    """

    def __init__(self):
        self.prefix = "HET IS "
        self.minutes = ["",
            "VIJF OVER ", \
            "TIEN OVER ", \
            "KWART OVER ", \
            "TWINTIG OVER ", \
            "VIJF VOOR HALF ", \
            "HALF ", \
            "VIJF OVER HALF ", \
            "TWINTIG VOOR ", \
            "KWART VOOR ", \
            "TIEN VOOR ", \
            "VIJF VOOR "]
        self.hours = ["TWAALF", \
            "EEN", \
            "TWEE", \
            "DRIE", \
            "VIER", \
            "VIJF", \
            "ZES", \
            "ZEVEN", \
            "ACHT", \
            "NEGEN", \
            "TIEN", \
            "ELF", \
            "TWAALF"]
        self.full_hour_suffix = " UUR"

    def get_time(self, time, withPrefix=True):
        hour=time.hour%12+(1 if time.minute/5 > 4 else 0)
        minute=time.minute/5
        # Assemble string
        return str(
            (self.prefix if withPrefix else "") +
            self.minutes[minute] +
            self.hours[hour] + \
            # Append "S" to "EIN" (in case of "EIN UHR")
            ("" if (hour == 1 and minute != 0) else "") + \
            (self.full_hour_suffix if (minute == 0) else "")) + " " + \
            ('*' * int(time.minute % 5))

