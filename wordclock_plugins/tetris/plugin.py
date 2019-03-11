# Authored by Markus E.
# https://github.com/mrksngl

import os
import wordclock_tools.wordclock_colors as wcc
import random
import time
from brick import brick
from time import sleep


class plugin:
    """
    A class to display some tetris
    """

    def __init__(self, config):
        """
        Initializations for the startup of the current wordclock plugin
        """
        # Get plugin name (according to the folder, it is contained in)
        self.name = os.path.dirname(__file__).split('/')[-1]
        self.pretty_name = "Tetris"
        self.description = "For the players."

        self.bg_color = wcc.BLACK;

        self.bricks = [brick([[0, 0, 0, 0],
                              [1, 1, 1, 1],
                              [0, 0, 0, 0],
                              [0, 0, 0, 0]],
                             wcc.Color(255, 0, 0)),
                       brick([[1, 0, 0],
                              [1, 1, 1],
                              [0, 0, 0]],
                             wcc.Color(255, 255, 0)),
                       brick([[0, 0, 1],
                              [1, 1, 1],
                              [0, 0, 0]],
                             wcc.Color(0, 0, 255)),
                       brick([[1, 1],
                              [1, 1]],
                             wcc.Color(255, 0, 255)),
                       brick([[0, 1, 1],
                              [1, 1, 0, ],
                              [0, 0, 0]],
                             wcc.Color(0, 255, 255)),
                       brick([[0, 1, 0],
                              [1, 1, 1],
                              [0, 0, 0]],
                             wcc.Color(0, 255, 0)),
                       brick([[1, 1, 0],
                              [0, 1, 1],
                              [0, 0, 0]],
                             wcc.Color(255, 255, 255))]

    def run(self, wcd, wci):
        """
        Displays interactive tetris until gameover
        """
        H = wcd.get_wca_height()
        W = wcd.get_wca_width()

        # Reset game
        wcd.setColorToAll(self.bg_color, includeMinutes=True)
        self.field = [[None for _ in range(W)] for _ in range(H)]
        lines = 0

        lastevent = -1

        while True:
            # choose brick and rotation
            brick = random.choice(self.bricks).clone()
            for _ in range(random.randint(0, 4)):
                brick = brick.rotate_cw()

            x = int((W - brick.outerWidth) / 2)
            y = -brick.padTop - brick.innerHeight + 1

            # drop brick
            t = time.time()
            while True:
                # check for collision
                if self.collision(brick, x, y):
                    # brick hit the highest line: settle
                    self.carve(brick, x, y - 1)
                    if y <= 0:  # at top: game over
                        self.gameover(wcd)
                        return
                    # brick hit the highest line: settle
                    lines += self.clear_lines(wcd)  # clear full lines
                    break;

                # brick and redraw
                self.carve(brick, x, y)
                self.draw(wcd)

                event = wci.waitForEvent(0.01)
                # check the time
                d = time.time() - t
                timeout = d > max(0.2, (0.5 - 0.02 * lines))  # make game harder over time
                if timeout and H - brick.innerHeight - brick.padTop == y:
                    # at end of field: settle brick and move on
                    lines += self.clear_lines(wcd)
                    lastevent = -1
                    break;

                # remove brick again (do not redraw by now)
                self.uncarve(brick, x, y)

                if timeout:  # next line
                    y += 1
                    t = time.time()

                if lastevent == event:
                    continue

                lastevent = event

                if event == wci.EVENT_BUTTON_RETURN:
                    brickr = brick.rotate_cw()
                    # simple wall bounce
                    if not self.collision(brickr, x, y):
                        brick = brickr
                    elif not self.collision(brickr, x - 1, y):
                        brick = brickr
                        x -= 1
                    elif not self.collision(brickr, x + 1, y):
                        brick = brickr
                        x += 1
                    # adjust x and y
                    x = min(max(-brick.padLeft, x), W - brick.innerWidth - brick.padLeft)
                    y = max(-brick.padTop - brick.innerHeight + 1, y)
                elif event == wci.EVENT_BUTTON_LEFT:
                    # move brick to the left
                    nx = max(-brick.padLeft, x - 1)
                    if not self.collision(brick, nx, y):
                        x = nx
                elif event == wci.EVENT_BUTTON_RIGHT:
                    # move brick to the right
                    nx = min(x + 1, W - brick.innerWidth - brick.padLeft)
                    if not self.collision(brick, nx, y):
                        x = nx
                elif event == wci.EVENT_EXIT_PLUGIN or event == wci.EVENT_NEXT_PLUGIN_REQUESTED:
                    return

    def clear_lines(self, wcd):
        # get all full lines
        rows = [x for x, row in enumerate(self.field) if
                reduce(lambda x, y: x and y, map(lambda x: x is not None, row), True)]
        if len(rows):
            for k in range(4):  # blink them 2 times
                for r, row in enumerate(self.field):
                    for c, cell in enumerate(row):
                        if k % 2 == 0 and r in rows:
                            wcd.setColorBy2DCoordinates(c, r, self.bg_color)
                        else:
                            wcd.setColorBy2DCoordinates(c, r,
                                                        cell.color if cell is not None else self.bg_color)
                # redraw
                wcd.show()
                sleep(0.3)
        for row in rows:  # clear lines
            for k in reversed(range(row)):
                self.field[k + 1] = self.field[k][:]
        self.draw(wcd)
        return len(rows)

    def gameover(self, wcd):
        for k in range(10):  # blink all lines 5 times
            for r, row in enumerate(self.field):
                for c, cell in enumerate(row):
                    if k % 2 == 0:
                        wcd.setColorBy2DCoordinates(c, r, self.bg_color)
                    else:
                        wcd.setColorBy2DCoordinates(c, r, cell.color if cell is not None else self.bg_color)
            wcd.show()
            sleep(0.3)

    def draw(self, wcd):
        # redraw field
        for r, row in enumerate(self.field):
            for c, cell in enumerate(row):
                wcd.setColorBy2DCoordinates(c, r, cell.color if cell is not None else self.bg_color)
        wcd.show()

    def carve(self, brick, x, y):
        for by, row in enumerate(brick.layout):
            if y + by >= 0:
                for bx, cell in enumerate(row):
                    if y + by < len(self.field) and x + bx < len(self.field[y + by]):
                        if cell:
                            self.field[y + by][x + bx] = brick

    def collision(self, brick, x, y):
        for by, row in enumerate(brick.layout):
            if y + by >= 0:
                for bx, cell in enumerate(row):
                    if y + by < len(self.field) and x + bx < len(self.field[y + by]):
                        if cell:
                            if self.field[y + by][x + bx] is not None:
                                return True
        return False

    def uncarve(self, brick, x, y):
        for by, row in enumerate(brick.layout):
            if y + by >= 0:
                for bx, cell in enumerate(row):
                    if y + by < len(self.field) and x + bx < len(self.field[y + by]):
                        if cell:
                            self.field[y + by][x + bx] = None
