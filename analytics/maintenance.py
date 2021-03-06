from django.utils.translation import ugettext as _

from analytics import settings
from analytics.options import Statistic


def list_statistics():
    """
    Prints all of the available statistics.
    """
    for s in get_statistic_models():
        print s.__name__, "(%s)" % s



def ensure_list(v):
    """
    Makes sure that the given value is a list.
    """
    return list(v) if getattr(v, '__iter__', False) else [v]



def get_statistic_by_name(stat_name):
    """
    Fetches a statistics based on the given class name. Does a look-up
    in the gadgets' registered statistics to find the specified one.
    """

    if stat_name == 'ALL':
        return get_statistic_models()

    for stat in get_statistic_models():
        if stat.__name__ == stat_name:
            return stat

    raise Exception, _("%(stat)s cannot be found.") % {'stat': stat_name}


def get_statistic_models():
    from django.db.models import get_models
    import inspect
    
    stats = []
    for model in get_models():
        if Statistic in inspect.getmro(model):
            stats.append(model)

    return stats
        

def calculate_statistics(stat, frequencies):
    """
    Calculates all of the metrics associated with the registered gadgets.
    """
    stats = ensure_list(stat)
    frequencies = ensure_list(frequencies)

    for stat in stats:
        for f in frequencies:
            print "Calculating %s (%s)..." % (stat.__name__, settings.STATISTIC_FREQUENCY_DICT[f])
            stat.calculate(f)


def reset_statistics(stat, frequencies, reset_cumulative, recalculate=False):
    """
    Resets the specified statistic's data (deletes it) for the given
    frequency/ies.
    """

    stats = ensure_list(stat)
    frequencies = ensure_list(frequencies)

    for s in stats:
        for f in frequencies:
            if not s.cumulative or reset_cumulative:
                print "Resetting %s (%s)..." % (s.__name__, settings.STATISTIC_FREQUENCY_DICT[f])
                s.objects.filter(frequency=f).delete()
            elif s.cumulative and not reset_cumulative:
                print "Skipping %s because it is cumulative." % s.__name__

    if recalculate:
        print "Recalculating statistics..."
        calculate_statistics(stats, frequencies)


