from django.urls import path 
from . import views

app_name = 'management'

urlpatterns = [
    path('', views.manager_dashboard, name='manager_dashboard'),
]