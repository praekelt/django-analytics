#
# Constants for Panya Analytics.
#
# thane@praekelt.com
#


STATISTIC_FREQUENCY_DAILY   = 'd'
STATISTIC_FREQUENCY_WEEKLY  = 'w'
STATISTIC_FREQUENCY_MONTHLY = 'm'

STATISTIC_FREQUENCY_CHOICES = (
    (STATISTIC_FREQUENCY_DAILY, 'Daily'),
    (STATISTIC_FREQUENCY_WEEKLY, 'Weekly'),
    (STATISTIC_FREQUENCY_MONTHLY, 'Monthly'),
)

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

