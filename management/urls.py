from django.urls import path 
from . import views

app_name = 'management'

urlpatterns = [
    path('', views.manager_dashboard, name='manager_dashboard'),
    path('management_detail/<int:id>/', views.manager_detail, name='management_detail'),
    path('management_detail/<int:id>/edit', views.manager_edit, name='management_edit'),
    path('allow/', views.allow, name='allow'),
    path('approve/<int:id>/', views.approve_user, name='approve_user'),
    # path('reject/<int:id>/', views.reject_user, name='reject_user'),
    path('quitter/', views.quitter, name='quitter'),
]