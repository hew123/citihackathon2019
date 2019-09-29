from django.urls import path, re_path, include
from . import views

urlpatterns = [
    path('', views.accounts_details, name ='accounts_details'),
    path('reset-password/',views.reset_password, name ='reset-password'),
    # path('account-type/',views.account_type, name='account_type'),

    # path('', views.UserList.as_view(),name='user-list'),
    # path('<int:pk>/', views.UserDetail.as_view(), name='user-detail'),
    # path('', views.api_root),
]
