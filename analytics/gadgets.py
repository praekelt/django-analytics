from django.template.loader import render_to_string
from django.utils.encoding import force_unicode

from analytics import settings
from analytics import models
from analytics.views import dashboard
from analytics.sites import gadgets

class BaseGadget(object):
    def __init__(self, title, stats, display_type, frequency, samples, width, height):
        self.title = title
        # make sure we have a list of statistics
        self.stats = list(stats) if getattr(stats, '__iter__', False) else [stats]
        self.display_type = display_type
        self.frequency = frequency
        self.samples = samples
        self.width = width
        self.height = height
        self.id = None

    def get_data(self):
        from datetime import datetime
        from random import randint
        import time

        data = []
        for stat in self.stats:
            latest = stat.get_latest(frequency=self.frequency)
            #data.append((time.mktime(latest.date_time.timetuple()), getattr(stat.get_latest(), self.display_type)))
            data.append((time.mktime(datetime.now().timetuple()) * 1000, randint(0, 10000)))

        return data
        return [(time.mktime(datetime.now().timetuple()) * 1000, randint(0, 10000)), (time.mktime(datetime.now().timetuple()) * 1000, randint(0, 10000))]
    
    def render(self, template):
        gadgets.register(self)
        context = {
            'object': self,
            'hash': self.__hash__(),
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
        return super(LineGadget, self).render('analytics/gadgets/line.html')

class NumberGadget(BaseGadget):
    def render(self):
        super(LineGadget, self).render('analytics/gadgets/number.html')

class Registrations(LineGadget):
    pass

dashboard.register(Registrations('Daily Registrations', [models.Registrations, models.Registrations], settings.COUNT_DISPLAY_TYPE, settings.STATISTIC_FREQUENCY_DAILY, 30, 4, 1))
