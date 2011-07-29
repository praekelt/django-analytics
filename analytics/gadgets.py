from random import randint

from django.template.loader import render_to_string
from django.utils.encoding import force_unicode

from analytics import settings
from analytics import models
from analytics.sites import gadgets

class BaseGadget(object):
    def __init__(self, title, stats, value_type, frequency, samples, width, height):
        self.title = title
        self.stats = stats
        self.value_type = value_type
        self.frequency = frequency
        self.samples = samples
        self.width = width
        self.height = height
    
    def render(self):
        context = {
            'object': self,
        }
        return render_to_string('analytics/gadgets/line.html', context)

    def __str__(self):
        if hasattr(self, '__unicode__'):
            return force_unicode(self).encode('utf-8')
        if hasattr(self, 'label'):
            return self.label
        return '%s' % self.__class__.__name__

class BarGadget(BaseGadget):
    pass

class LineGadget(BaseGadget):
    pass

class NumberGadget(BaseGadget):
    pass

class Registrations(LineGadget):
    label = 'Registrations'


gadgets.register(Registrations('Registrations', [models.Registrations, models.Registrations], settings.COUNT, 'd', 30, 4, 1))
