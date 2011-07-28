def autodiscover():
    """
    Auto-discover INSTALLED_APPS metrics.py modules and fail silently when
    not present. This forces an import on them to register any metrics they
    may want.

    After import dynamically create statistics model for each metric.
    """
    import pdb; pdb.set_trace()
    from django.conf import settings
    from django.utils.importlib import import_module
    from django.utils.module_loading import module_has_submodule

    for app in settings.INSTALLED_APPS:
        mod = import_module(app)
        # Attempt to import the app's metrics module.
        try:
            import_module('%s.metrics' % app)
        except:
            # Decide whether to bubble up this error. If the app just
            # doesn't have an metrics module, we can ignore the error
            # attempting to import it, otherwise we want it to bubble up.
            if module_has_submodule(mod, 'metrics'):
                raise

    # Dynamically create stats model for each metric.
    from analytics.sites import metrics

    for metric in metrics._registry:
        metric_name = metric.__class__.__name__
        globals()[metric_name] = type(metric_name, (Statistic,), {'__module__': 'analytics.models',})

autodiscover()
