from django.urls import path 
from . import views

app_name = 'main'

urlpatterns = [
    path('start/', views.start_ezcs, name='start_ezcs'),
    path('', views.user_dashboard, name='user_dashboard'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('contract/', views.contract, name='contract'),
    path('privacy/', views.privacy, name='privacy'),
    path('', views.user_dashboard, name='user_dashboard'),
    path('notice/<int:id>/', views.notice_detail, name='notice_detail'),
]
