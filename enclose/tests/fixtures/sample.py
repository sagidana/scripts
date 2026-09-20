import os


def helper(value):
    return value + 1


class Widget:
    """a widget"""

    def __init__(self, size):
        self.size = size

    def grow(self):
        self.size = helper(self.size)
        return self.size

    @staticmethod
    def shrink(size):
        def inner(n):
            return n - 1
        return inner(size)


def use_widget():
    widget = Widget(3)
    callback = lambda x: helper(x)
    widget.grow()
    return callback(widget.size)


TOP_LEVEL = helper(41)
