from datetime import datetime, timedelta

from django.db import models
from django.utils.translation import ugettext as _

from analytics import settings



class Statistic(models.Model):
    """
    A counter (point and cumulative) for a specific metric relevant
    to a particular date/time.
    
    A 'label' member is required to be provided by inheriting classes, to be used as user friendly metric title during widget rendering.
    A 'widget' member is required to be provided by inheriting classes, to be used as for rendering the metric.
    """

    class Meta:
        abstract = True

    date_time = models.DateTimeField(
        db_index=True,
    )
    frequency = models.CharField(
        max_length=1,
        choices=settings.STATISTIC_FREQUENCY_CHOICES,
        db_index=True,
    )
    count = models.IntegerField(
        default=0,
    )
    cumulative_count = models.BigIntegerField(
        default=0,
    )


    def __unicode__(self):
        return self.__class__.__name__

    @classmethod
    def calculate(cls, frequency=settings.STATISTIC_FREQUENCY_DAILY, verbose=settings.STATISTIC_CALCULATION_VERBOSE):
        """
        Runs the calculator for this type of statistic.
        """

        if verbose:
            print _("Calculating statistics for %(class)s...") % {'class': cls.__name__}

        start_datetime = None
        end_datetime = None

        # get the latest statistic
        latest_stat = cls.latest(frequency)

        # if there's a cumulative function defined
        cumulative_calc = getattr(cls, 'get_cumulative', None) is not None

        # work out today's date, truncated to midnight
        today = datetime.strptime(datetime.now().strftime("%Y %m %d"), "%Y %m %d") 

        # if this statistic only has cumulative stats available
        if cumulative_calc:
            if frequency == settings.STATISTIC_FREQUENCY_DAILY:
                start_datetime = today
            elif frequency == settings.STATISTIC_FREQUENCY_WEEKLY:
                # truncate today to the start of this week
                start_datetime = datetime.strptime(today.strftime("%Y %W 0"), "%Y %w %w")
            elif frequency == settings.STATISTIC_FREQUENCY_MONTHLY:
                # truncate today to the start of this month
                start_datetime = datetime.strptime(today.strftime("%Y %m 1"), "%Y %m %d")

            stat, created = cls.objects.get_or_create(date_time=start_datetime, frequency=frequency)
            stat.cumulative_count = cls.get_cumulative()
            stat.count = (stat.cumulative_count-latest_stat.cumulative_count) if latest_stat else stat.cumulative_count
        else:
            # get the date/time at which we should start calculating
            start_datetime = cls.get_start_datetime() if latest_stat is None else latest_stat.date_time
            # truncate the start date/time to the appropriate frequency
            if frequency == settings.STATISTIC_FREQUENCY_DAILY:
                start_datetime = datetime.strptime(start_datetime.strftime("%Y %m %d"), "%Y %m %d")
                end_datetime = start_datetime+timedelta(days=1)
            elif frequency == settings.STATISTIC_FREQUENCY_WEEKLY:
                # start at the beginning of the week of the latest stat
                start_datetime = datetime.strptime(start_datetime.strftime("%Y %W 0"), "%Y %W %w")-timedelta(days=7)
                end_datetime = start_datetime+timedelta(days=7)
            elif frequency == settings.STATISTIC_FREQUENCY_MONTHLY:
                # start at the beginning of the month of the latest stat
                start_datetime = datetime.strptime(start_datetime.strftime("%Y %m 1"), "%Y %m %d")
                end_datetime = datetime.strptime((start_datetime+timedelta(days=33)).strftime("%Y %m 1"), "%Y %m %d")

            # if we're doing the normal count
            while start_datetime < today:
                count = cls.get_count(start_datetime, end_datetime)
                cumulative_count = 0
                if isinstance(count, tuple):
                    cumulative_count = count[1]
                    count = count[0]
                else:
                    cumulative_count = (latest_stat.cumulative_count+count) if latest_stat else count

                stat, created = cls.objects.get_or_create(date_time=start_datetime, frequency=frequency)
                stat.count = count
                stat.cumulative_count = cumulative_count

                latest_stat = stat

                # update the dates/times
                start_datetime = end_datetime
                if frequency == settings.STATISTIC_FREQUENCY_DAILY:
                    end_datetime += timedelta(days=1)
                elif frequency == settings.STATISTIC_FREQUENCY_WEEKLY:
                    end_datetime += timedelta(days=7)
                elif frequency == settings.STATISTIC_FREQUENCY_MONTHLY:
                    end_datetime = datetime.strptime((start_datetime+timedelta(days=33)).strftime("%Y %m 1"), "%Y %m %d")



    @classmethod
    def get_count(cls, start_datetime, end_datetime):
        """
        Must calculate the number of statistics between the two
        specified date/times. These date/times are passed from the
        calculator functions depending on the type of calculation
        being performed.

        Results must be returned for date >= start_datetime and
        date < end_datetime.
        """
        raise NotImplementedError("%s has to implement 'get_count' method" % cls.__name__)



    @classmethod
    def get_start_datetime(cls):
        """
        Must return a date/time object indicating when the earliest
        data available for this metric occurred.
        """
        return settings.STATISTIC_DEFAULT_START_DATETIME



    @classmethod
    def latest(cls, frequency=settings.STATISTIC_FREQUENCY_DAILY):
        """
        Returns the latest instance of this statistic.
        """
        try:
            return cls.objects.filter(frequency=frequency).order_by('-date_time')[0]
        except IndexError:
            return None



    @classmethod
    def earliest(cls, frequency=settings.STATISTIC_FREQUENCY_DAILY):
        """
        Returns the earliest instance of this statistic.
        """
        try:
            return cls.objects.filter(frequency=frequency).order_by('date_time')[0]
        except IndexError:
            return None



    @classmethod
    def latest_count(cls, frequency=settings.STATISTIC_FREQUENCY_DAILY, cumulative=True, count=False):
        """
        Returns the latest count for the given frequency.
        """
        latest_stat = cls.latest(frequency=frequency)
        if latest_stat:
            if count and cumulative:
                return (latest_stat.count, latest_stat.cumulative_count)
            elif count:
                return latest_stat.count
            else:
                return latest_stat.cumulative_count
        else:
            if count and cumulative:
                return (0, 0)
            else:
                return 0


