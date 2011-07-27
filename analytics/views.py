from django.views.generic import TemplateView

class AnalyticsView(TemplateView):
    def get_template_names(self):
        return 'analytics/dashboard.html'

class DefaultAnalyticsView(AnalyticsView):
    pass
