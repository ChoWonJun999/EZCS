from django.urls import path 
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.user_dashboard, name='user_dashboard'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
]
