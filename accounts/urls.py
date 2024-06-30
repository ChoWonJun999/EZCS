from django.urls import path 
from django.contrib.auth import views as auth_views
from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'accounts'

urlpatterns = [

    #path('signup/', views.signup, name='signup'),
    #path('login/', views.login_view, name='login'),
    path('', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
]