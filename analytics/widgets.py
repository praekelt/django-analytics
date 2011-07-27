class BaseWidget(object):
    def __init__(self, title, metrics, value_type, frequency, samples, width, height):
        self.title = title
        self.metrics = metrics
        self.value_type = value_type
        self.frequency = frequency
        self.samples = samples
        self.width = width
        self.height = height

class BarWidget(BaseWidget):
    pass

class NumberWidget(BaseWidget):

    def render(self):
        return 'foo'
