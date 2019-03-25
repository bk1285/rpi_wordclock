
import wordclock_tools.wordclock_colors as wcc


class wordclock_screen:

    def __init__(self, wcd):
        self.matrix = [[wcc.BLACK for _ in range(wcd.get_wca_height())] for _ in
                                      range(wcd.get_wca_width())]

        size = wcd.get_wca_height() * wcd.get_wca_width()
        rest = wcd.get_led_count() - size

        self.minutes = [wcc.BLACK for _ in range(4)]
        if rest >= 4: # subtract minutes
            rest -= 4

        self.misc = [wcc.BLACK for _ in range(rest)]
