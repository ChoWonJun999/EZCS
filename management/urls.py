from django.urls import path 
from . import views

app_name = 'management'

urlpatterns = [
    path('', views.manager_dashboard, name='manager_dashboard'),
    path('management_detail/<int:id>/', views.manager_detail, name='management_detail'),
    path('management_detail/<int:id>/edit', views.manager_edit, name='management_edit'),
    path('allow/', views.allow, name='allow'),
    path('allow/allow_detail/<int:id>/', views.allow_detail, name='allow_detail'),
    path('approve/<int:id>/', views.approve_user, name='approve_user'),
    path('active/<int:id>/', views.active, name='active'),
    # path('user_inactive/<int:id>/', views.user_inactive, name='user_inactive'),
    # path('reject/<int:id>/', views.reject_user, name='reject_user'),

    path('quitter/', views.quitter, name='quitter'),
    path('manager_user/', views.manager_user, name='manager_user'),

    path('inactive/', views.inactive, name='inactive'),
    path('inactive/inactive_detail/<int:id>/', views.inactive_detail, name='inactive_detail'),
    path('retire/', views.retire, name='retire'),
    path('retire/retire_detail/<int:id>/', views.retire_detail, name='retire_detail'),
    path('leave/', views.leave, name='leave'),
    path('leave/leave_detail/<int:id>/', views.leave_detail, name='leave_detail'),
    path('reject/', views.reject, name='reject'),
    path('reject/reject_detail/<int:id>/', views.reject_detail, name='reject_detail'),

]