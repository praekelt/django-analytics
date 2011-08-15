from django.views.generic import TemplateView

from analytics import maintenance

class AlreadyRegistered(Exception):
    pass


class AnalyticsView(TemplateView):
    columns = 4
    rows = 2

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
    
    def get_max_dimension(self):
        columns = 0
        rows = 0
        for gadget in self._registry:
            if gadget.columns > columns:
                columns = gadget.columns
            if gadget.rows > rows:
                rows = gadget.rows
    
        return columns, rows
    
    def get_context_data(self, **kwargs):
        """
        Get the context for this view.
        """
        #max_columns, max_rows = self.get_max_dimension()
        context = {
            'gadgets': self._registry,
            'columns': self.columns,
            'rows': self.rows,
            'column_ratio': 100 - self.columns * 2,
            'row_ratio': 100 - self.rows * 2,
        }
        context.update(kwargs)
        return context


class AnalyticsDashboardView(AnalyticsView):
    pass


dashboard = AnalyticsDashboardView()
