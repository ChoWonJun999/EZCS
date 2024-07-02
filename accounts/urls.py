from django.urls import path 
from . import views
from django.conf.urls.static import static

app_name = 'accounts'

urlpatterns = [
    path('', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('searchPW/', views.searchPW, name='searchPW'),
    path('check_username/', views.check_username, name='check_username'),
    path('check_email/', views.check_email, name='check_email'),
]
