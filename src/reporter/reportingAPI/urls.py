from django.urls import path
from . import views

urlpatterns = [
    path('demographic', views.demographic, name='demographic'),
    path('organization', views.organization, name='organization'),
    path('historical', views.historical, name='historical'),
    path('user-historical', views.user_historical, name='user_historical'),
]
