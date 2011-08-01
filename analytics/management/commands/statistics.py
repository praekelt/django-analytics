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
            help=_("List all of the available gadgets and their corresponding statistics."),
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
        make_option('--reset-cumulative',
            action='store_true',
            dest='reset_cumulative',
            default=False,
            help=_("Should the cumulative statistics also be reset (if --reset is used)? Default: False"),
        ),
        make_option('-f', '--frequency',
            action='store',
            dest='frequency',
            type='choice',
            default='a',
            choices=settings.STATISTIC_FREQUENCY_ALL+['a'],
            help=_("Set the frequency for the current calculation. d=daily, w=weekly, m=monthly, a=all."),
        ),
    )
    
    help = "Analytics-related functionality"

    def handle(self, *args, **kwargs):
        """
        Command handler for the "metrics" command.
        """

        frequency = kwargs['frequency']
        frequencies = settings.STATISTIC_FREQUENCY_ALL if frequency == 'a' else [frequency]

        if kwargs['list']:
            maintenance.list_gadgets()

        # if we're supposed to calculate the latest statistics
        elif kwargs['calculate']:
            maintenance.calculate_statistics(maintenance.get_statistic_by_name(kwargs['calculate']), frequencies)

        elif kwargs['reset']:
            maintenance.reset_statistics(maintenance.get_statistic_by_name(kwargs['reset']), frequencies, kwargs['reset_cumulative'])

