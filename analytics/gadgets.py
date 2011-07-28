from analytics import settings
from analytics import models
from analytics.sites import gadgets

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
    pass

class Registrations(NumberWidget):
    def render(self):
        return 'foo'

gadgets.register(Registrations('Registrations', [models.Registrations,], settings.COUNT, 'd', 30, 4, 1))
