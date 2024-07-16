from django.urls import path 
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    path('signup/', views.signup, name='signup'),
    path('searchPW/', views.searchPW, name='searchPW'),
    path('check-username/', views.check_username, name='check_username'),
    path('check-email/', views.check_email, name='check_email'),
    path('check-phone/', views.check_phone, name='check_phone'), 
    path('reset_password/', views.reset_password, name='reset_password'),
    path('consent/', views.consent, name='consent'),
]
