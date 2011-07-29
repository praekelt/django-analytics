from django.contrib.auth.models import User

from analytics import options

class Registrations(options.Statistic):
    """
    Monitors the number of new user signups.
    """

    @classmethod
    def calculate(cls, start_datetime, end_datetime):
        return User.objects.filter(date_joined__gte=start_datetime,
            date_joined__lt=end_datetime).count()


