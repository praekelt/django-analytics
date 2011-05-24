#
# CSV view for django-analytics.
#
# thane@praekelt.com
#

import csv
import datetime
from django.utils.translation import ugettext as _
from django.http import HttpResponse
from analytics.models import Metric
from analytics import settings



def csv_dump(request, uid):
    """
    Returns a CSV dump of all of the specified metric's counts
    and cumulative counts.
    """

    metric = Metric.objects.get(uid=uid)
    frequency = request.GET.get('frequency', settings.STATISTIC_FREQUENCY_DAILY)

    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=%s%s.csv' % (uid, datetime.datetime.now().strftime("%Y%m%d-%H%M"))

    writer = csv.writer(response)
    writer.writerow([_('Date/time'), _('Count'), _('Cumulative count')])
    for stat in metric.statistics.filter(frequency=frequency).order_by('date_time'):
        writer.writerow([stat.date_time.strftime(settings.CSV_DATETIME_FORMAT), stat.count, stat.cumulative_count])

    return response

