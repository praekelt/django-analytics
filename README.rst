django-analytics
================

A basic Django app facilitating tracking of certain elementary metrics and statistics -
generally just metrics which can be measured in terms of counts and cumulative counts.

This app could be useful for keeping track of registrations, page impressions, sessions,
and so on. By default, it allows for tracking of registrations. Adding more metrics
is a relatively straightforward task, as explained further on.

.. contents::
    :depth: 5    

Quick Installation
------------------
1. Save a copy of the ``django-analytics`` app in your Python path.
2. Add it to your ``INSTALLED_APPS`` list in your Django project settings.
3. Create a ``mod_analytics.py`` file for each of your apps that require some sort
   of tracking. See the `Creating a mod_analytics Script`_ section below.
4. Run the following from the command line in order to install the various metrics
   and automatically make them active:

::

    > python manage.py metrics --install

5. Run the following from the command line to update the daily, weekly and monthly
   statistics for each of the active metrics:

::

    > python manage.py metrics --calculate=ALL

By default, ``django-analytics`` comes with a ``registrations`` metric which counts
the number of users in the system based on their ``date_joined`` timestamp.

Creating a mod_analytics Script
-------------------------------
If, for example, you have an app called ``comments`` with the following ``models.py`` file:

::

    from django.db import models
    from django.contrib.auth.models import User

    class Comment(models.Model):
        user = models.ForeignKey(User, related_name='comments')
        timestamp = models.DateTimeField(auto_now_add=True)
        comment = models.CharField(max_length=300)

and you would like to track the total number of comments, you could
create a ``mod_analytics.py`` script (in the same directory as your app's models)
looking like the following:

::

    from analytics.basemetric import BaseMetric
    from models import Comment

    class TotalComments(BaseMetric):
        uid   = "totalcomments"
        title = "Total comments"

        def calculate(self, start_datetime, end_datetime):
            return Comment.objects.filter(timestamp__gte=start_datetime,
                timestamp__lt=end_datetime).count()

        def get_earliest_timestamp(self):
            try:
                return Comment.objects.all().order_by('timestamp')[0].timestamp
            except IndexError:
                return None


Geckoboard Integration and CSV Dumps
------------------------------------
In order to allow for `Geckoboard <http://geckoboard.com>`_ integration to allow for
visualisation of your statistics, as well as simple CSV dumping of statistics,
in your project's ``urls.py``, add the following line:

::

    urlpatterns = patterns('',
        # ...

        (r'^analytics/', include('analytics.urls')),

        # ...
    )

Note that this project makes use of ``django-geckoboard`` (http://pypi.python.org/pypi/django-geckoboard),
so all of the default ``django-geckoboard`` settings apply.

**Geckboard Charts**

This will automatically add the following Geckoboard-related URLs to your project:

``analytics/geckoboard/numbers``
    A `numbers widget <http://support.geckoboard.com/entries/231507-custom-widget-type-definitions>`_.
    Supported GET variable parameters: ``uid``, ``daysback``, ``cumulative``, ``frequency``.
    ``daysback`` default: 7.
``analytics/geckoboard/rag``
    A `RAG widget <http://support.geckoboard.com/entries/231507-custom-widget-type-definitions>`_.
    Supported GET variable parameters: ``uids``, ``daysback``, ``cumulative``, ``frequency``.
``analytics/geckoboard/pie``
    A `pie chart widget <http://support.geckoboard.com/entries/274940-custom-chart-widget-type-definitions>`_.
    Supported GET variable parameters: ``uids``, ``daysback``, ``cumulative``, ``frequency``.
``analytics/geckoboard/line``
    A `line chart widget <http://support.geckoboard.com/entries/274940-custom-chart-widget-type-definitions>`_.
    Note that this can only plot a single metric per chart.
    Supported GET variable parameters: ``uid``, ``daysback``, ``cumulative``, ``frequency``.
    ``daysback`` default: 7.
``analytics/geckoboard/geckometer``
    A `geck-o-meter widget <http://support.geckoboard.com/entries/274940-custom-chart-widget-type-definitions>`_.
    Supported GET variable parameters: ``uid``, ``frequency``, ``cumulative``, ``min``, ``max``.
``analytics/geckoboard/funnel``
    A `funnel chart widget <http://support.geckoboard.com/entries/274940-custom-chart-widget-type-definitions>`_.
    Supported GET variable parameters: ``uids``, ``frequency``, ``cumulative``, ``type``,
    ``percentage``, ``sort``.

**Geckoboard GET Variable Parameters**

+----------------+--------------------------------------------------------------------------+
| ``uid``        | The UID of the metric to display, if a single metric is to be displayed. |
+----------------+--------------------------------------------------------------------------+
| ``uids``       | The UIDs of the metrics to display, if multiple metrics are to be        |
|                | displayed.                                                               |
+----------------+--------------------------------------------------------------------------+
| ``daysback``   | The numbers Geckoboard widget shows a single count, and the percentage   |
|                | change from a previous count. This view returns the most recent count    |
|                | or cumulative count, as well as the count or cumulative count from       |
|                | ``days_back`` days ago.                                                  |
+----------------+--------------------------------------------------------------------------+
| ``cumulative`` | A boolean value (either ``t`` or ``f``) indicating whether the period    |
|                | count is to be returned, or the cumulative count. Default: ``t``.        |
+----------------+--------------------------------------------------------------------------+
| ``frequency``  | The frequency of the statistics to be returned. Can be ``d``, ``w`` or   |
|                | ``m`` for daily, weekly or monthly, respectively. Default: ``d``.        |
+----------------+--------------------------------------------------------------------------+
| ``min``        | The minimum value of a particular metric - usually for pie charts.       |
|                | Default: 0.                                                              |
+----------------+--------------------------------------------------------------------------+
| ``max``        | The maximum value of a particular metric - usually for pie charts.       |
|                | Default: 100.                                                            |
+----------------+--------------------------------------------------------------------------+
| ``type``       | Chart type - only applicable to the funnel chart. See the Geckoboard     |
|                | API for more details. Default: ``standard``.                             |
+----------------+--------------------------------------------------------------------------+
| ``percentage`` | Whether or not to show a percentage - only applicable to the funnel      |
|                | chart. See the Geckoboard API for more details. Default: ``show``.       |
+----------------+--------------------------------------------------------------------------+
| ``sort``       | A boolean value (either ``t`` or ``f``) indicating whether or not to     |
|                | sort the statistics - only applicable to the funnel chart. See the       |
|                | Geckoboard API for more details. Default: ``f``.                         |
+----------------+--------------------------------------------------------------------------+

**CSV Dump**

It will also add the following CSV-related URLs to your project:

``analytics/csv/<uid>``
    A simple view requiring the UID of the metric as its parameter, returning
    a CSV dump of all of the statistics for the given metric. By default, this returns
    the **daily** statistics for the metric.

**CSV Dump GET Variable Parameters**

+----------------+--------------------------------------------------------------------------+
| ``frequency``  | The frequency of the statistics to be returned. Can be ``d``, ``w`` or   |
|                | ``m`` for daily, weekly or monthly, respectively. Default: ``d``.        |
|                | For example, ``analytics/csv/registrations?frequency=w`` will return all |
|                | of the weekly registrations over all time as a CSV dump.                 |
+----------------+--------------------------------------------------------------------------+


Metrics Explained
-----------------
The ``django-analytics`` module creates ``Metric`` objects for each type of metric that
needs to be tracked, such as registrations, page impressions, etc. Each metric needs to
have a globally unique identifier (**UID**) so that it can be referenced from the command line
by name, and a title to provide a little more of a description of what that metric
is.

Each metric has a number of ``Statistic`` objects associated with it, each ``Statistic``
only being a simple combination of date/time, a count for that date/time, a cumulative
count, and frequency.

The frequency can currently only be **daily**, **weekly** or
**monthly**, and by default, each metric's statistics are calculated for all of those
frequencies (so a single metric can have multiple frequencies' statistics).

In general, the cumulative count is automatically calculated for you, and is simply the
previous day's/week's/month's cumulative count, added to the current day's/week's/month's
count.

Command Line Reference
----------------------
The following options are available from the command line for the ``metrics`` management
command:

-l, --list         Lists all of the available metrics, along with some basic information about each.
-i, --install      Scans the project for available metrics and creates or updates them where necessary.
-a, --activate     Activates the metric with the specified UID, e.g. ``--activate=registrations``.
                   If you want to activate all metrics,
                   simply specify ``--activate=ALL`` on the command line. Only active metrics will
                   be included in a ``--calculate=ALL`` execution.
-d, --deactivate   Deactivates the metric with the specified UID. Again, you can specify
                   ``--deactivate=ALL`` to deactivate all metrics.
-c, --calculate    Calculates the specified metric, e.g. ``--calculate=registrations``. Can
                   specify ``--calculate=ALL`` to calculate all active metrics.
-f, --frequency    If the ``--calculate`` command is specified, this will allow one to force a particular
                   frequency's statistics to be calculated. Possible values are: ``d`` (daily), ``w`` (weekly),
                   ``m`` (monthly) and ``a`` (all). Default is *all*.
--reset            Deletes all of the ``Statistic`` objects associated with the specified metric.
                   Can specify ``--reset=ALL`` to delete all statistics for all metrics, regardless
                   of whether they are active or not.
--drop-metric      Deletes the actual ``Metric`` with the specified UID. Use ``--drop-metric=ALL``
                   to drop all metrics (and their statistics) from the database.

Inner Workings
--------------
When running the ``manage.py metrics --install`` command, the following happens:

1. The script searches through all the installed apps for your project and
   attempts to first find a ``mod_analytics`` module which it can import.
2. It then searches through all of the classes in each ``mod_analytics`` module
   it encounters, and then attempts to find classes derived from the
   ``analytics.basemetric.BaseMetric`` class (an abstract class).
3. For each valid class found which derives from the ``BaseMetric`` class, the script
   makes sure it has two functions: ``calculate``, and ``get_earliest_timestamp``.
   It also makes sure the class has two properties: ``uid`` and ``title``.
4. If the class has these two functions, the script creates a ``Metric`` instance
   whose unique identifier and title are set to the ``uid`` and ``title`` values
   of the discovered class.

The ``calculate`` function takes two parameters: ``start_datetime`` and ``end_datetime``,
and must simply return a count of the relevant metric between those two given dates. You can
perform any calculations you need in this function to get to this final count value.

To understand the reasoning here, the ``analytics`` app has three broad calculation time periods
which it attempts to calculate: **daily**, **weekly** and **monthly**. For a daily calculation,
for example, the ``start_datetime`` parameter supplied will resemble something like
``datetime(2011, 5, 1)`` and the ``end_datetime`` parameter will resemble something like
``datetime(2011, 5, 2)``. The ``calculate`` function must then return a count of the relevant
metric for the time period starting at 2011/05/01 00:00 and ending at 2011/05/02 00:00.
**NOTE**: You should always return counts starting at exactly the given ``start_datetime``
value (i.e. greater-than-equal-to), but *just before* the ``end_datetime`` value (i.e.
less-than).

The ``get_earliest_timestamp`` function must simply return a ``datetime.datetime`` object
indicating the earliest data's associated date/time, so that the analytics calculation routine
knows the date at which to start calculating. If there are no entries yet, this function must
return ``None``.

Abstract Metrics
----------------

If you want to create abstract metrics, simply create a separate Python file somewhere
which will contain your "abstract" metrics. For example, create an ``abstract_metrics.py``
file which looks as follows:

::

    from analytics import BaseMetric
    from django.contrib.auth.models import User

    class UserBaseMetric(BaseMetric):
        def calculate(self, start_datetime, end_datetime):
            return User.objects.filter(date_joined__gte=start_datetime,
                date_joined__lt=end_datetime).count()

        def get_earliest_timestamp(self):
            try:
                return User.objects.all().order_by('date_joined')[0].date_joined
            except IndexError:
                return None
            
Then, in your ``mod_analytics.py`` file, just import your ``abstract_metrics`` module.
**Note**: Do not import the ``UserBaseMetric``, just import the ``abstract_metrics`` module,
as follows:

::

    from analytics import BaseMetric
    import myapp.abstract_metrics

    class UserMetric(abstract_metrics.UserBaseMetric):
        uid   = "users"
        title = "Users"


Todo
----
The following features are planned for future versions of ``django-analytics``:

1. Custom visualisation integrated into Django admin back-end.
2. Hourly statistics.
3. More complex statistics, such as frequency plots/histograms.

Version History
---------------

+---------+------------------------------------------+
| Version | Description                              |
+=========+==========================================+
| 0.0.1   | First version                            |
+---------+------------------------------------------+

