from django.contrib import admin
from analytics import models


class MetricAdmin(admin.ModelAdmin):
    list_display = ['uid', 'title']

admin.site.register(models.Metric, MetricAdmin)



class StatisticAdmin(admin.ModelAdmin):
    list_display = ['metric', 'date_time', 'frequency', 'count', 'cumulative_count']
    list_filter = ['frequency', 'metric', 'date_time']

admin.site.register(models.Statistic, StatisticAdmin)


