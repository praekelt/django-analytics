#
# URLs for django-analytics.
#
# thane@praekelt.com
#

from django.conf.urls.defaults import *
from analytics.geckoboard_views import *
from analytics.csv_views import *


urlpatterns = patterns('',
    # geckoboard-related views
    (r'^geckoboard/numbers', geckoboard_number_widget),
    (r'^geckoboard/rag', geckoboard_rag_widget),
    (r'^geckoboard/pie', geckoboard_pie_chart),
    (r'^geckoboard/line', geckoboard_line_chart),
    (r'^geckoboard/geckometer', geckoboard_geckometer),
    (r'^geckoboard/funnel', geckoboard_funnel),

    # CSV-realted views
    (r'^csv/(?P<uid>[a-zA-Z0-9\_]+)', csv_dump),
)

