from django.urls import path
from . import views

urlpatterns = [
    path('demographic/', views.index, name='index')
]
