from random import randint

from django.template.loader import render_to_string
from django.utils.encoding import force_unicode

from analytics import settings
from analytics import models
from analytics.sites import gadgets

class BaseGadget(object):
    def __init__(self, title, stats, value_type, frequency, samples, width, height):
        self.title = title
        # make sure we have a list of statistics
        self.stats = list(stats) if getattr(stats, '__iter__', False) else [stats]
        self.value_type = value_type
        self.frequency = frequency
        self.samples = samples
        self.width = width
        self.height = height
    
    def render(self, template):
        context = {
            'object': self,
        }
        return render_to_string(template, context)

    def __str__(self):
        if hasattr(self, '__unicode__'):
            return force_unicode(self).encode('utf-8')
        if hasattr(self, 'title'):
            return self.title
        return '%s' % self.__class__.__name__

class BarGadget(BaseGadget):
    def render(self):
        super(BarGadget, self).render('analytics/gadgets/bar.html')

class LineGadget(BaseGadget):
    def render(self):
        super(LineGadget, self).render('analytics/gadgets/line.html')

class NumberGadget(BaseGadget):
    def render(self):
        super(LineGadget, self).render('analytics/gadgets/number.html')

class Registrations(LineGadget):
    pass


gadgets.register(Registrations('Registrations', [models.Registrations, models.Registrations], settings.COUNT, 'd', 30, 4, 1))
