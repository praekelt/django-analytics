from django.core.exceptions import ImproperlyConfigured

def validate(metric_class):
    """
    Does basic Metric option validation. 
    """
    if not hasattr(metric_class, 'label'):
        raise ImproperlyConfigured("No 'label' attribute found for metric %s." % metric_class.__name__)
    
    if not hasattr(metric_class, 'widget'):
        raise ImproperlyConfigured("No 'widget' attribute found for metric %s." % metric_class.__name__)
