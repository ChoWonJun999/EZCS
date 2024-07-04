from django.urls import path 
from . import views

app_name = 'management'

urlpatterns = [

    path('', views.manager_dashboard, name='dashboard'), #대쉬보드 화면
    path('management_detail/<int:id>/', views.manager_detail, name='management_detail'), # 직원상세정보화면
    path('detail/<int:id>/', views.detail, name='detail'), # 직원상세정보화면
    path('management_detail/<int:id>/edit', views.manager_edit, name='edit'), # 직원상세정보수정
    path('allow/', views.allow, name='allow'), #가입승인화면
    # path('allow/allow_detail/<int:id>/', views.allow_detail, name='allow_detail'), #가입승인상세화면
    path('approve/<int:id>/', views.approve_user, name='approve_user'), #승인해주는 로직
    # path('inactive_active/<int:id>/', views.inactive_active, name='inactive_active'), #퇴사 및 휴직 관리 활성화로직
    # path('leave_active/<int:id>/', views.leave_active, name='leave_active'), # 휴직자 활성화 로직
    # path('retire_active/<int:id>/', views.retire_active, name='retire_active'), # 퇴사자 활성화 로직
    # path('reject_active/<int:id>/', views.reject_active, name='reject_active'), # 보류자 활성화 로직
    path('inactive/', views.inactive, name='inactive'), #퇴사 및 휴직 관리 화면
    # path('inactive/inactive_detail/<int:id>/', views.inactive_detail, name='inactive_detail'),
    # path('retire/', views.retire, name='retire'), # 퇴사자 화면
    # path('retire/retire_detail/<int:id>/', views.retire_detail, name='retire_detail'),
    # path('leave/', views.leave, name='leave'), # 휴직자 화면
    # path('leave/leave_detail/<int:id>/', views.leave_detail, name='leave_detail'),
    # path('reject/', views.reject, name='reject'),# 보류자 화면
    # path('reject/reject_detail/<int:id>/', views.reject_detail, name='reject_detail'), #보류자 상세화면
    # path('search/', views.search, name='search'), #검색 로직
    # # path('all/', views.all, name='all'), #all 전체선택 로직
]