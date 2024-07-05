from django.urls import path 
from . import views
from django.conf.urls.static import static

app_name = 'accounts'

urlpatterns = [
    path('', views.login, name='login'),
    path('login_pass/', views.login_pass, name='login_pass'),
    path('logout/', views.logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('searchPW/', views.searchPW, name='searchPW'),
    path('check-username/', views.check_username, name='check_username'),
    path('check-email/', views.check_email, name='check_email'),
    path('check-phone/', views.check_phone, name='check_phone'), 
    path('reset-password/', views.reset_password, name='reset_password'),
]
