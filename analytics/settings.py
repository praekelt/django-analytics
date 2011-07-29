from django.utils.translation import ugettext as _
from django.conf import settings
from datetime import datetime

STATISTIC_FREQUENCY_DAILY   = 'd'
STATISTIC_FREQUENCY_WEEKLY  = 'w'
STATISTIC_FREQUENCY_MONTHLY = 'm'

STATISTIC_FREQUENCY_CHOICES = (
    (STATISTIC_FREQUENCY_DAILY, _('Daily')),
    (STATISTIC_FREQUENCY_WEEKLY, _('Weekly')),
    (STATISTIC_FREQUENCY_MONTHLY, _('Monthly')),
)

STATISTIC_DEFAULT_START_DATETIME = getattr(settings, 'ANALYTICS_DEFAULT_START_DATETIME', datetime(2011, 1, 1))

# should output be printed during statistic calculation?
STATISTIC_CALCULATION_VERBOSE = True

STATISTIC_FREQUENCY_DICT = dict(STATISTIC_FREQUENCY_CHOICES)

GECKOBOARD_COLOURS = [
    '666666',
    'ffcc00',
    'ff3300',
    '99cc00',
    '003300',
    '3399ff',
    '003366',
    '330066',
    '9900cc',
]

CSV_DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"

COUNT = 'count'
