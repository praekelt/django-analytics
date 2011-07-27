from django.contrib.auth.models import User

from analytics.sites import metrics

class BaseMetric(object):
    """
    Serves as a template for external apps' metrics. All
    functions specified in this object are compulsory.
    """
    # A descriptive label, to be used as user friendly metric title during widget rendering.
    label = ''

    def calculate(self, start_datetime, end_datetime):
        """
        Must calculate the number of statistics between the two
        specified date/times. These date/times are passed from the
        calculator functions depending on the type of calculation
        being performed.

        Results must be returned for date >= start_datetime and
        date < end_datetime.
        """
        raise NotImplementedError("%s has to implement 'calculate' method" % self)

    def get_earliest_timestamp(self):
        """
        Must return a date/time object indicating when the earliest
        data available for this metric occurred.
        """
        # XXX: This should not have to happen in the metric themselves.
        raise NotImplementedError("Calc all stats from epoch or from some setting value and assume first to have a value's timestamp is the earliest.")


class Registrations(BaseMetric):
    """
    Monitors the number of new user signups.
    """
    label = 'Registrations'

    def calculate(self, start_datetime, end_datetime):
        return User.objects.filter(date_joined__gte=start_datetime,
            date_joined__lt=end_datetime).count()

    # XXX: This should not have to be here.
    #def get_earliest_timestamp(self):
    #    try:
    #        return User.objects.order_by('date_joined')[0].date_joined
    #    except IndexError:
    #        return None

metrics.register(Registrations)
