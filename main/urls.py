from django.urls import path 
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.user_dashboard, name='user_dashboard'),
    path('manager/', views.manager_dashboard, name='manager_dashboard'),
]
