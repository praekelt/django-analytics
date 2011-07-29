from django.conf.urls.defaults import *
from analytics import views

urlpatterns = patterns('',
    # Geckoboard-related views.
    (r'^geckoboard/numbers', 'analytics.geckoboard_views.geckoboard_number_widget'),
    (r'^geckoboard/rag', 'analytics.geckoboard_views.geckoboard_rag_widget'),
    (r'^geckoboard/pie', 'analytics.geckoboard_views.geckoboard_pie_chart'),
    (r'^geckoboard/line', 'analytics.geckoboard_views.geckoboard_line_chart'),
    (r'^geckoboard/geckometer', 'analytics.geckoboard_views.geckoboard_geckometer'),
    (r'^geckoboard/funnel', 'analytics.geckoboard_views.geckoboard_funnel'),
   
    # Highcharts related views.
    url(r'^highcharts/(?P<id>\d+)/$', 'analytics.highcharts_views.data', name='highcharts_data'),
        
    # CSV related views.
    (r'^csv/(?P<uid>[a-zA-Z0-9\_]+)', 'analytics.csv_views.csv_dump'),

    # Default analytics dashboard.
    url(r'^$', views.AnalyticsDashboardView.as_view(), name='analytics_dashboard_view'),
)
