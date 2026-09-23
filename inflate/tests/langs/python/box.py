class Box:

    def __init__(self):
        self.size = 1

    def helper(self, value):
        return value + self.size

    def greet(self, value):
        return self.helper(value) * 2

    def runner(self):
        return self.greet(3)
