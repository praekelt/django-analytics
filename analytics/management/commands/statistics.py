#
# Central management command for django-analytics.
#
# thane@praekelt.com
#

from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from django.utils.translation import ugettext as _
from analytics.calculator import *
from analytics.maintenance import *
from analytics import settings
from analytics.sites import gadgets


def list_gadgets():
    """
    Prints all of the available gadgets and their corresponding statistics.
    """
    for gadget in gadgets.get_gadgets():
        print u"%s\t\t-\t%s" % (gadget, ', '.join(gadget.stats))



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
        make_option('--drop-metric',
            action='store',
            dest='drop_metric',
            type='string',
            default=None,
            help=_("Drops the specified metric from the database. Use --drop-metric=ALL to drop all metrics."),
        ),
        make_option('-f', '--frequency',
            action='store',
            dest='frequency',
            type='choice',
            default='a',
            choices=['d', 'w', 'm', 'a'],
            help=_("Set the frequency for the current calculation. d=daily, w=weekly, m=monthly, a=all."),
        ),
    )
    
    help = "Analytics-related functionality"

    def handle(self, *args, **kwargs):
        """
        Command handler for the "metrics" command.
        """

        frequency = kwargs['frequency']
        frequencies = ['d', 'w', 'm'] if frequency == 'a' else [frequency]

        if kwargs['list']:
            list_gadgets()

        # if we're supposed to calculate the latest statistics
        '''
        elif kwargs['calculate']:
            if kwargs['calculate'] == 'ALL':
                calculate_all_metrics(frequencies)
            else:
                calculate_metric_by_uid(kwargs['calculate'], frequencies)

        elif kwargs['reset']:
            reset_metric(kwargs['reset'], frequencies)
        '''

