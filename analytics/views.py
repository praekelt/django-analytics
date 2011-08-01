from django.views.generic import TemplateView

from analytics import maintenance

class AlreadyRegistered(Exception):
    pass


class AnalyticsView(TemplateView):
    def get_template_names(self):
        return 'analytics/dashboard.html'

    def __init__(self):
        self._registry = []

    def get_gadgets(self):
        return self._registry

    def get_active_stats(self):
        """
        Returns all of the active statistics for the gadgets currently registered.
        """
        stats = []
        for gadget in self._registry.values():
            for s in gadget.stats:
                if s not in stats:
                    stats.append(s)
        return stats

    def register(self, gadget):
        """
        Registers a gadget object.
        If a gadget is already registered, this will raise AlreadyRegistered.
        """
        if gadget in self._registry:
            raise AlreadyRegistered
        else:
            self._registry.append(gadget)

    def unregister(self, gadgets):
        """
        Unregisters the specified gadget(s) if it/they has/have already been registered.
        "gadgets" can be a single class or a tuple/list of classes to unregister.
        """
        gadgets = maintenance.ensure_list(gadgets)
        for gadget in gadgets:
            while gadget in self._registry:
                self._registry.remove(gadget)


class AnalyticsDashboardView(AnalyticsView):
    def get_context_data(self, **kwargs):
        """
        Get the context for this view.
        """
        context = {'gadgets': self._registry}
        context.update(kwargs)
        return context


dashboard = AnalyticsDashboardView()
