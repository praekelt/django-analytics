#
# Base metric class from which related apps' metric definitions
# must be derived in order to be detected by the maintenance functions.
#
# thane@praekelt.com
#

class BaseMetric(object):
    """
    Serves as a template for external apps' metrics. All
    functions specified in this object are compulsory.
    """

    # a unique identifier for this metric
    # must be globally unique
    uid = ''

    # the metric's descriptive title
    title = ''


    def calculate(self, start_datetime, end_datetime):
        """
        Must calculate the number of statistics between the two
        specified date/times. These date/times are passed from the
        calculator functions depending on the type of calculation
        being performed.

        Results must be returned for date >= start_datetime and
        date < end_datetime.
        """

        pass


    def get_earliest_timestamp(self):
        """
        Must return a date/time object indicating when the earliest
        data available for this metric occurred.
        """

        pass



