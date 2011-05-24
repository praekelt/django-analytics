#
# Geckoboard-related views for django-analytics.
#
# thane@praekelt.com
#

from datetime import datetime, timedelta
from django_geckoboard.decorators import number_widget, rag_widget, pie_chart, line_chart, geck_o_meter, funnel
from analytics.models import Metric
from analytics import settings
from django.utils.translation import ugettext as _



def get_GET_array(request, var_name, fail_silently=True):
    """
    Returns the GET array's contents for the specified variable.
    """

    vals = request.GET.getlist(var_name)
    if not vals:
        if fail_silently:
            return []
        else:
            raise Exception, _("No array called '%(varname)s' in GET variables") % {'varname': var_name}

    return vals



def get_GET_bool(request, var_name, default=True):
    """
    Tries to extract a boolean variable from the specified request.
    """

    val = request.GET.get(var_name, default)
    if isinstance(val, str) or isinstance(val, unicode):
        val = True if val[0] == 't' else False

    return val



def get_next_colour():
    """
    Gets the next colour in the Geckoboard colour list.
    """

    colour = settings.GECKOBOARD_COLOURS[get_next_colour.cur_colour]

    get_next_colour.cur_colour += 1
    if get_next_colour.cur_colour >= len(settings.GECKOBOARD_COLOURS):
        get_next_colour.cur_colour = 0

    return colour

get_next_colour.cur_colour = 0




def get_gecko_params(request, uid=None, days_back=0, cumulative=True,
    frequency=settings.STATISTIC_FREQUENCY_DAILY, min_val=0, max_val=100,
    chart_type='standard', percentage='show', sort=False):
    """
    Returns the default GET parameters for a particular Geckoboard
    view request.
    """

    return {
        'days_back'  : int(request.GET.get('daysback', days_back)),
        'uid'        : request.GET.get('uid', uid),
        'uids'       : get_GET_array(request, 'uids[]'),
        'cumulative' : get_GET_bool(request, 'cumulative', cumulative),
        'frequency'  : request.GET.get('frequency', frequency),
        'min'        : request.GET.get('min', min_val),
        'max'        : request.GET.get('max', max_val),
        'type'       : request.GET.get('type', chart_type),
        'percentage' : request.GET.get('percentage', percentage),
        'sort'       : get_GET_bool(request, 'sort', sort),
    }





@number_widget
def geckoboard_number_widget(request):
    """
    Returns a number widget for the specified metric's cumulative total.
    """

    params = get_gecko_params(request, days_back=7)
    metric = Metric.objects.get(uid=params['uid'])
    try:
        latest_stat = metric.statistics.filter(frequency=params['frequency']).order_by('-date_time')[0]
    except IndexError:
        return (0, 0)

    try:
        prev_stat = metric.statistics.filter(frequency=params['frequency'],
            date_time__lte=latest_stat.date_time-timedelta(days=params['days_back'])).order_by('-date_time')[0]
    except IndexError:
        # if there is no previous stat
        return (latest_stat.cumulative_count, 0) if params['cumulative'] else (latest_stat.count, 0)

    return (latest_stat.cumulative_count, prev_stat.cumulative_count) if params['cumulative'] else (latest_stat.count, prev_stat.count)




@rag_widget
def geckoboard_rag_widget(request):
    """
    Searches the GET variables for metric UIDs, and displays
    them in a RAG widget.
    """

    params = get_gecko_params(request)
    print params['uids']
    max_date = datetime.now()-timedelta(days=params['days_back'])

    metrics = Metric.objects.filter(uid__in=params['uids'])
    results = [(metric.latest_count(frequency=params['frequency'], count=not params['cumulative'],
        cumulative=params['cumulative'], max_date=max_date), metric.title) for metric in metrics]
    
    return tuple(results)




@pie_chart
def geckoboard_pie_chart(request):
    """
    Shows a pie chart of the metrics in the uids[] GET variable array.
    """

    params = get_gecko_params(request, cumulative=True)
    from_date = datetime.now()-timedelta(days=params['days_back'])

    metrics = Metric.objects.filter(uid__in=params['uids'])
    results = [(metric.latest_count(frequency=params['frequency'], count=not params['cumulative'],
        cumulative=params['cumulative']), metric.title, get_next_colour()) for metric in metrics]
    
    return tuple(results)



@line_chart
def geckoboard_line_chart(request):
    """
    Returns the data for a line chart for the specified metric.
    """

    params = get_gecko_params(request, cumulative=False, days_back=7)
    metric = Metric.objects.get(uid=params['uid'])

    start_date = datetime.now()-timedelta(days=params['days_back'])
    stats = [s for s in metric.statistics.filter(frequency=params['frequency'],
        date_time__gte=start_date).order_by('date_time')]

    if len(stats) == 0:
        raise Exception, _("No statistics for metric %(metric)s.") % {'metric': params['uid']}

    dates = [stats[0].date_time]

    # get up to 3 dates from the stats
    if len(stats) >= 3:
        mid = len(stats)/2
        if not mid:
            mid = 1
        dates.extend([stats[mid].date_time, stats[-1].date_time])
    elif len(stats) == 2:
        dates.extend([stats[-1].date_time])

    return (
        [s.count for s in stats],
        dates,
        metric.title,
    )



@geck_o_meter
def geckoboard_geckometer(request):
    """
    Returns a Geck-o-Meter control for the specified metric.
    """

    params = get_gecko_params(request, cumulative=True)
    metric = Metric.objects.get(uid=params['uid'])

    return (metric.latest_count(frequency=params['frequency'], count=not params['cumulative'],
        cumulative=params['cumulative']), params['min'], params['max'])




@funnel
def geckoboard_funnel(request, frequency=settings.STATISTIC_FREQUENCY_DAILY):
    """
    Returns a funnel chart for the metrics specified in the GET variables.
    """

    # get all the parameters for this function
    params = get_gecko_params(request, cumulative=True)
    metrics = Metric.objects.filter(uid__in=params['uids'])
    items = [(metric.latest_count(frequency=params['frequency'], count=not params['cumulative'],
        cumulative=params['cumulative']), metric.title) for metric in metrics]
    
    return {
        'items'     : items,
        'type'      : params['type'],
        'percentage': params['percentage'],
        'sort'      : params['sort'],
    }

