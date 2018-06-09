# Authored by Markus E.
# https://github.com/mrksngl


import copy


class brick:
    def __init__(self, layout, color):
        self.layout = copy.deepcopy(layout)
        self.color = color
        self.outerHeight = len(layout)
        self.outerWidth = len(layout[0])

        self.padTop = padTop(layout)
        self.padBottom = padTop(layout[::-1])
        rl = rot_left(layout)
        self.padLeft = padTop(rl)
        self.padRight = padTop(rl[::-1])

        self.innerHeight = self.outerHeight - self.padTop - self.padBottom
        self.innerWidth = self.outerWidth - self.padLeft - self.padRight

    def clone(self):
        return brick(self.layout, self.color)

    def rotate_cw(self):
        return brick(rot_left(self.layout), self.color)

    def rotate_ccw(self):
        return brick(rot_right(self.layout), self.color)


def padTop(layout):
    empty = 0
    for i in layout:
        if reduce(lambda x, y: x + y, i, 0) == 0:
            empty += 1
        else:
            break
    return empty


def rot_left(layout):
    return map(list, zip(*layout[::-1]))


def rot_right(layout):
    return map(list, zip(*layout)[::-1])


def rot_twice(layout):
    return rot_left(rot_left(layout))
