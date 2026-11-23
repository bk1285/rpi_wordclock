import unittest
from threading import Lock
from unittest.mock import Mock

from wordclock_tools.wiring import christians_wiring, wiring
from wordclock_tools.wordclock_colors import Color
from wordclock_tools.wordclock_display import wordclock_display
from wordclock_tools.wordclock_screen import wordclock_screen


class FrameDisplayTests(unittest.TestCase):
    def setUp(self):
        self.display = object.__new__(wordclock_display)
        self.display.mutex = Lock()
        self.display.fps = 25
        self.display.strip = Mock()
        self.display.wcl = object.__new__(wiring)
        self.display.wcl.WCA_WIDTH = 11
        self.display.wcl.WCA_HEIGHT = 10
        self.display.wcl.LED_COUNT = 114
        self.display.wcl.wcl = christians_wiring(11, 10)
        self.display.transition_cache_next = wordclock_screen(self.display)
        self.display.transition_cache_curr = wordclock_screen(self.display)
        self.frame = bytes(channel for i in range(114) for channel in (i, 255 - i, i // 2))

    def check_frame(self, brightness):
        self.display.setBrightness(brightness)
        self.display.show_rgb_frame(self.frame)
        expected = {}
        for y in range(10):
            for x in range(11):
                logical = y * 11 + x
                physical = (9 - y) * 11 + (10 - x if y % 2 else x)
                expected[physical] = self.frame[logical * 3:logical * 3 + 3]
        for i in range(110, 114):
            expected[i] = self.frame[i * 3:i * 3 + 3]
        actual = {i: (color.r, color.g, color.b)
                  for i, color in (call.args for call in self.display.strip.setPixelColor.call_args_list)}
        self.assertEqual(actual, {i: tuple(c * brightness // 255 for c in rgb)
                                  for i, rgb in expected.items()})
        self.display.strip.show.assert_called_once_with()

    def test_full_brightness_matrix_minute_pixels_and_screen_snapshot(self):
        self.check_frame(255)
        self.display.setColorBy2DCoordinates(0, 0, Color(1, 2, 3))
        self.display.setColorByMinute(0, Color(1, 2, 3))
        current = self.display.transition_cache_curr
        self.assertEqual(current.matrix[0][0].g, 255)
        self.assertEqual(current.minutes[0].r, 110)

    def test_reduced_brightness(self):
        self.check_frame(96)
