class TemporaryGenerator:

    def __init__(self):
        self.reset()

    def reset(self):
        self.counter = 1

    def new(self):
        value = f"t{self.counter}"
        self.counter += 1
        return value


class LabelGenerator:

    def __init__(self):
        self.reset()

    def reset(self):
        self.counter = 1

    def new(self):
        value = f"L{self.counter}"
        self.counter += 1
        return value
