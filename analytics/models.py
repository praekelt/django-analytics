from django.contrib.auth.models import User

from analytics import options

class Registrations(options.Statistic):
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
