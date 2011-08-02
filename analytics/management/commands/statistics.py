#
# Central management command for django-analytics.
#

from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from django.utils.translation import ugettext as _
from analytics import maintenance
from analytics import settings



class Command(BaseCommand):
    """
    The management command to handle statistic-related function calls.
    """

    option_list = BaseCommand.option_list + (
        make_option('-l', '--list',
            action='store_true',
            dest='list',
            default=False,
            help=_("List all of the available statistics."),
        ),
        make_option('-c', '--calculate',
            action='store',
            type='string',
            dest='calculate',
            default=None,
            help=_("Perform the calculation for the specified statistic. Use --calculate=ALL to calculate all statistics."),
        ),
        make_option('--reset',
            action='store',
            dest='reset',
            type='string',
            default=None,
            help=_("Reset the specified statistic. Use --reset=ALL to reset all statistics."),
        ),
        make_option('--recalculate',
            action='store',
            dest='recalculate',
            type='string',
            default=None,
            help=_("Recalculates the specified statistic. Use --recalculate=ALL to recalculate all statistics."),
        ),
        make_option('--reset-cumulative',
            action='store_true',
            dest='reset_cumulative',
            default=False,
            help=_("Should the cumulative statistics also be reset (if --reset is used)? Default: False"),
        ),
        make_option('-f', '--frequency',
            action='store',
            dest='frequency',
            type='string',
            default='a',
            help=_("Set the frequency for the current calculation. h=hourly, d=daily, w=weekly, m=monthly, a=all. Separate multiple frequencies by commas, e.g. d,w,m"),
        ),
    )
    
    help = "Analytics-related functionality"

    def handle(self, *args, **kwargs):
        """
        Command handler for the "metrics" command.
        """

        frequency = kwargs['frequency']
        frequencies = settings.STATISTIC_FREQUENCY_ALL if frequency == 'a' else (frequency.split(',') if ',' in frequency else [frequency])

        if kwargs['list']:
            maintenance.list_statistics()

        # if we're supposed to calculate the latest statistics
        elif kwargs['calculate']:
            maintenance.calculate_statistics(maintenance.get_statistic_by_name(kwargs['calculate']), frequencies)

        # pure reset of statistic(s)
        elif kwargs['reset']:
            maintenance.reset_statistics(maintenance.get_statistic_by_name(kwargs['reset']), frequencies, kwargs['reset_cumulative'])

        # recalculation of statistic(s)
        elif kwargs['recalculate']:
            maintenance.reset_statistics(maintenance.get_statistic_by_name(kwargs['recalculate']), frequencies, kwargs['reset_cumulative'], True)

