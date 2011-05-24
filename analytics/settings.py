#
# Settings for django-analytics.
#
# thane@praekelt.com
#

from django.utils.translation import ugettext as _


STATISTIC_FREQUENCY_DAILY   = 'd'
STATISTIC_FREQUENCY_WEEKLY  = 'w'
STATISTIC_FREQUENCY_MONTHLY = 'm'

STATISTIC_FREQUENCY_CHOICES = (
    (STATISTIC_FREQUENCY_DAILY, _('Daily')),
    (STATISTIC_FREQUENCY_WEEKLY, _('Weekly')),
    (STATISTIC_FREQUENCY_MONTHLY, _('Monthly')),
)

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

# the module for which to search when looking through the
# installed apps for analytics-related configurations
ANALYTICS_APP_MODULE = "mod_analytics"

