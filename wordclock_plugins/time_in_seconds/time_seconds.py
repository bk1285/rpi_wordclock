class time_seconds:
    """
    This class returns a given time as a range of LED-indices.
    Illuminating these LEDs represents the current time on a german WCA
    """

    def __init__(self):
        self.rightDigit = []
        self.leftDigit = [list(range(23, 26)) + list(range(33, 34)) + list(range(37, 38)) + list(range(44, 45)) + list(
            range(47, 49)) + list(range(55, 56)) + list(range(57, 58)) + list(range(59, 60)) + list(
            range(66, 68)) + list(range(70, 71)) + list(range(77, 78)) + list(range(81, 82)) + list(range(89, 92)), \
                          list(range(24, 25)) + list(range(34, 36)) + list(range(46, 47)) + list(range(57, 58)) + list(
                              range(68, 69)) + list(range(79, 80)) + list(range(89, 92)), \
                          list(range(23, 26)) + list(range(33, 34)) + list(range(37, 38)) + list(range(48, 49)) + list(
                              range(58, 59)) + list(range(68, 69)) + list(range(78, 79)) + list(range(88, 93)), \
                          list(range(22, 27)) + list(range(36, 37)) + list(range(46, 47)) + list(range(58, 59)) + list(
                              range(70, 71)) + list(range(77, 78)) + list(range(81, 82)) + list(range(89, 92)), \
                          list(range(25, 26)) + list(range(35, 37)) + list(range(45, 46)) + list(range(47, 48)) + list(
                              range(55, 56)) + list(range(58, 59)) + list(range(66, 71)) + list(range(80, 81)) + list(
                              range(91, 92)), \
                          list(range(22, 27)) + list(range(33, 34)) + list(range(44, 48)) + list(range(59, 60)) + list(
                              range(70, 71)) + list(range(77, 78)) + list(range(81, 82)) + list(range(89, 92)), \
                          list(range(24, 26)) + list(range(34, 35)) + list(range(44, 45)) + list(range(55, 59)) + list(
                              range(66, 67)) + list(range(70, 71)) + list(range(77, 78)) + list(range(81, 82)) + list(
                              range(89, 92)), \
                          list(range(22, 27)) + list(range(37, 38)) + list(range(47, 48)) + list(range(57, 58)) + list(
                              range(67, 68)) + list(range(78, 79)) + list(range(89, 90)), \
                          list(range(23, 26)) + list(range(33, 34)) + list(range(37, 38)) + list(range(44, 45)) + list(
                              range(48, 49)) + list(range(56, 59)) + list(range(66, 67)) + list(range(70, 71)) + list(
                              range(77, 78)) + list(range(81, 82)) + list(range(89, 92)), \
                          list(range(23, 26)) + list(range(33, 34)) + list(range(37, 38)) + list(range(44, 45)) + list(
                              range(48, 49)) + list(range(56, 60)) + list(range(70, 71)) + list(range(80, 81)) + list(
                              range(89, 91))]

    def get_time(self, seconds):
        decimal = seconds / 10
        ones = seconds % 10
        self.rightDigit = []
        for i in self.leftDigit[ones]:
            self.rightDigit.insert(i, i + 6)
        # Assemble indices
        return \
            (self.leftDigit[int(decimal)] + \
             self.rightDigit)
