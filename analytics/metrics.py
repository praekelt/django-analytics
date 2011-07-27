#
# Sample mod_analytics file for django-analytics.
# Provides metric computation for some standard metrics.
#
# thane@praekelt.com
#

from django.contrib.auth.models import User
from analytics.basemetric import BaseMetric



class Registrations(BaseMetric):
    """
    Monitors the number of new user signups.
    """

    uid   = 'registrations'
    title = 'Registrations'


    def calculate(self, start_datetime, end_datetime):
        return User.objects.filter(date_joined__gte=start_datetime,
            date_joined__lt=end_datetime).count()


    def get_earliest_timestamp(self):
        try:
            return User.objects.order_by('date_joined')[0].date_joined
        except IndexError:
            return None

 

