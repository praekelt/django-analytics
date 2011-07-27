from django.views.generic import TemplateView
from analytics.sites import metrics

class AnalyticsView(TemplateView):
    def get_template_names(self):
        return 'analytics/dashboard.html'
    
    def get_context_data(self, **kwargs):
        """
        Get the context for this view.
        """
        widgets = []
        for metric in metrics._registry:
            widgets.append(metric.widget)

        context = {'widgets': widgets}
        context.update(kwargs)
        return context

class DefaultAnalyticsView(AnalyticsView):
    pass
