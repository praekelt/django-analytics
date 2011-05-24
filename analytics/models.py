#
# django-analytics
#
# thane@praekelt.com
#

from django.db import models
from django.utils.translation import ugettext as _
from analytics import settings



class Metric(models.Model):
    """
    Represents a tracked metric for this project. For example,
    this could be "unique users", or "page impressions", or
    "registrations".
    """

    uid = models.CharField(
        max_length=100,
        help_text=_("A unique name for this metric, so that it can be addressed from the code."),
        unique=True,
        db_index=True,
    )
    title = models.CharField(
        max_length=100,
        help_text=_("A short, descriptive title for this metric"),
    )
    metric_class = models.CharField(
        max_length=200,
        help_text=_("The Python class responsible for the calculation of this metric."),
    )
    active = models.BooleanField(
        default=True,
        help_text=_("Whether or not to include this metric in regular calculations."),
    )
    

    def __unicode__(self):
        return self.title


    def latest_count(self, frequency=settings.STATISTIC_FREQUENCY_DAILY,
        count=True, cumulative=True, max_date=None):
        """
        Returns the most recent counts (cumulative and not) for this metric.

        If max_date is specified, the latest count prior to or on that date will be returned.
        """
        
        try:
            if max_date is not None:
                stat = self.statistics.filter(frequency=frequency,
                    date_time__lte=max_date).order_by('-date_time')[0]
            else:
                stat = self.statistics.filter(frequency=frequency).order_by('-date_time')[0]
            if count and cumulative:
                return (stat.count, stat.cumulative_count)
            elif cumulative:
                return stat.cumulative_count
            else:
                return stat.count
        except IndexError:
            # if there is no latest statistic
            if count and cumulative:
                return (0, 0)
            else:
                return 0
        


    def latest_stat(self, frequency=settings.STATISTIC_FREQUENCY_DAILY):
        """
        Returns the latest statistic for this metric.
        """

        try:
            return self.statistics.filter(frequency=frequency).order_by('-date_time')[0]
        except IndexError:
            return None



    def update_cumulative_counts(self, earliest_datetime=None, frequency=settings.STATISTIC_FREQUENCY_DAILY):
        """
        Updates all of this metric's statistics' cumulative counts.
        """

        try:
            query = self.statistics.filter(frequency=frequency)
            # if a "from" date/time was specified, use it
            if earliest_datetime is not None:
                query = query.filter(date_time__gte=earliest_datetime)
            stat = query.order_by('date_time')[0]
            stat.update_count()
        except IndexError:
            pass




class Statistic(models.Model):
    """
    A counter (point and cumulative) for a specific metric relevant
    to a particular date/time.
    """

    metric = models.ForeignKey(
        Metric,
        db_index=True,
        related_name='statistics',
    )
    date_time = models.DateTimeField(
        db_index=True,
    )
    frequency = models.CharField(
        max_length=1,
        choices=settings.STATISTIC_FREQUENCY_CHOICES,
        db_index=True,
    )
    count = models.IntegerField(default=0)
    cumulative_count = models.BigIntegerField(default=0)


    def __unicode__(self):
        return u'%s at %s' % (self.metric, self.date_time.strftime("%Y-%m-%d %H:%M:%S"))



    def update_count(self, count=None):
        """
        Updates this particular date's count, automatically working out the
        cumulative total, updating the cumulative totals of all of the subsequent
        statistic objects.

        Not supplying the count parameter simply updates all subsequent statistics,
        making sure their cumulative counts are accurate.
        """

        if count is None:
            # use the current count value
            count = self.count if self.count else 0
        else:
            self.count = count

        try:
            last_statistic = Statistic.objects.filter(metric=self.metric,
                frequency=self.frequency,
                date_time__lt=self.date_time).order_by('-date_time')[0]
            self.cumulative_count = last_statistic.cumulative_count+count
            #print "Set cumulative count to %d" % self.cumulative_count
        except IndexError:
            # this will most likely happen if there are no
            # elements prior to this statistic's date
            self.cumulative_count = count

        self.save()

        # update all subsequent cumulative counts
        next_statistics = [s for s in Statistic.objects.filter(metric=self.metric,
            frequency=self.frequency, date_time__gt=self.date_time).order_by('date_time')]
        prev_count = self.cumulative_count
        for s in next_statistics:
            s.cumulative_count = prev_count+s.count
            #print "date=%s, count=%d, cumulative_count=%d, prev_count=%d" % (s.date_time.strftime("%Y-%m-%d"), s.count, s.cumulative_count, prev_count)
            s.save()
            prev_count = int(s.cumulative_count)



