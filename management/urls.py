from django.urls import path 
from . import views

app_name = 'management'

urlpatterns = [
    path('', views.manager_dashboard, name='manager_dashboard'),
    path('management_detail/<int:id>/', views.manager_detail, name='management_detail'),
    path('management_detail/<int:id>/edit', views.manager_edit, name='management_edit'),
]