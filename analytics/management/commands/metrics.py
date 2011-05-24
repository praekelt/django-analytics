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


class Command(BaseCommand):
    """
    The management command to handle metric-related function calls.
    """

    option_list = BaseCommand.option_list + (
        make_option('-l', '--list',
            action='store_true',
            dest='list',
            default=False,
            help=_("List all of the available metrics."),
        ),
        make_option('-i', '--install',
            action='store_true',
            dest='install',
            default=False,
            help=_("Run through project apps and install metrics."),
        ),
        make_option('-a', '--activate',
            action='store',
            dest='activate',
            default=None,
            help=_("Activate the specified metric. Use --activate=ALL to activate all metrics."),
        ),
        make_option('-d', '--deactivate',
            action='store',
            dest='deactivate',
            default=None,
            help=_("Deactivate the specified metric. Use --deactivate=ALL to deactivate all metrics."),
        ),
        make_option('-c', '--calculate',
            action='store',
            type='string',
            dest='calculate',
            default=None,
            help=_("Perform the statistical calculation for the specified metric. Use --calculate=ALL to calculate all metrics."),
        ),
        make_option('--reset',
            action='store',
            dest='reset',
            type='string',
            default=None,
            help=_("Reset the specified metric. Use --reset=ALL to reset all metrics."),
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
    
    help = "Metric-related functionality (django-analytics)"

    def handle(self, *args, **kwargs):
        """
        Command handler for the "metrics" command.
        """

        frequency = kwargs['frequency']
        frequencies = ['d', 'w', 'm'] if frequency == 'a' else [frequency]

        # if we're going to install/update the metrics
        if kwargs['install']:
            scan_apps_for_metrics()

        elif kwargs['list']:
            list_metrics()

        # if we're supposed to calculate the latest statistics
        elif kwargs['calculate']:
            if kwargs['calculate'] == 'ALL':
                calculate_all_metrics(frequencies)
            else:
                calculate_metric_by_uid(kwargs['calculate'], frequencies)

        # activate the specified metric
        elif kwargs['activate']:
            activate_metric(kwargs['activate'])
            print _("Metric(s) %(metric)s activated.") % {'metric': kwargs['activate']}

        # deactivate the specified metric
        elif kwargs['deactivate']:
            deactivate_metric(kwargs['deactivate'])
            print _("Metric(s) %(metric)s deactivated.") % {'metric': kwargs['deactivate']}

        elif kwargs['drop_metric']:
            drop_metric(kwargs['drop_metric'])
            print _("Metric(s) %(metric)s dropped.") % {'metric': kwargs['drop_metric']}

        elif kwargs['reset']:
            reset_metric(kwargs['reset'], frequencies)

