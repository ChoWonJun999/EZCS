from django.urls import path 
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [

    #path('signup/', views.signup, name='signup'),
    #path('login/', views.login_view, name='login'),
    path('login2/', views.login2, name='login2'),
    path('login/', views.login, name='login'),
    #path('logout/', views.logout_view, name='logout'),
]