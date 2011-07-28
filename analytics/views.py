from django.views.generic import TemplateView

from analytics.sites import gadgets

class AnalyticsView(TemplateView):
    def get_template_names(self):
        return 'analytics/dashboard.html'
    
class AnalyticsDashboardView(AnalyticsView):
    def get_context_data(self, **kwargs):
        """
        Get the context for this view.
        """
        context = {'gadgets': gadgets._registry}
        context.update(kwargs)
        return context
