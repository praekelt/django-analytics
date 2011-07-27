from django.conf import settings

class AlreadyRegistered(Exception):
    pass

class Metrics(object):
    """
    A Metrics object providing managing various metrics.
    Models are registered with the Metrics using the register() method.
    """
    def __init__(self):
        self._registry = [] # metric class -> stats model class.

    def register(self, metric_class):
        """
        Registers the metric class.
        If a metric class is already registered, this will raise AlreadyRegistered.
        """
        # Don't validate unless required.
        if settings.DEBUG:
            from analytics.validation import validate
            validate(metric_class)

        # Instantiate the metric class to save in the registry
        if metric_class in self._registry:
            raise AlreadyRegistered
        else:
            self._registry.append(metric_class())
    
# This global metrics represents the default metrics, for the common case.
# You can instantiate Metrics in your own code to create a custom metrics object.
metrics = Metrics()
