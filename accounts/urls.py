# from django.urls import path 
# from . import views
# from django.contrib.auth import views as auth_views

# app_name = 'accounts'

# urlpatterns = [
#     path('login/', auth_views.LoginView.as_view(template_name='accounts/Login.html'), name='login'), 
#     #path('logout/', auth_views.LogoutView.as_view(template_name='accounts/Login.html'), name='logout'),
#     #path('signup/', auth_views.signupView.as_view(template_name='accounts/Login.html'), name='signup'),
# ]
from django.urls import path 
from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]