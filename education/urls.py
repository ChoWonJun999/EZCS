from django.urls import path 
from . import views

app_name = 'education'

urlpatterns = [
    path('', views.my_view, name='list'),
]
