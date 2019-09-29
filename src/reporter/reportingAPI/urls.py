from django.urls import path
from . import views

urlpatterns = [
    path('demographic', views.demographic, name='demographic'),
    path('organization', views.organization, name='organization'),
    path('historical', views.historical, name='historical'),
    path('user-historical', views.user_historical, name='user_historical'),
    path('export-single-event', views.export_csv_single_event, name='export_csv_single_event'),
    path('export-events', views.export_csv_events, name='export_csv_events'),
]
