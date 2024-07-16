from django.urls import path 
from . import views

app_name = 'management'

urlpatterns = [
    path('list/<str:flag>/', views.list, name='list'),
    path('detail/<int:id>/<str:flag>/', views.detail, name='detail'),
    path('update_auth/<int:id>/<int:status>', views.update_auth, name='update_auth'),
    path('edit/<int:id>/<str:flag>/', views.edit, name='edit'),
    path('adminsignup', views.adminsignup, name='adminsignup'),
    path('admincheck-username/', views.admincheck_username, name='admincheck-username'),
    path('admincheck-email/', views.admincheck_email, name='admincheck-email'),
    path('admincheck-phone/', views.admincheck_phone, name='admincheck-phone'), 
    path('adminreset_password/', views.adminreset_password, name='adminreset-password'),



    path('detail/<int:id>/edit', views.manager_edit, name='manager_edit'),

    path('allow/', views.allow, name='allow'), #가입승인화면
    path('approve/<int:id>/', views.approve_user, name='approve_user'), #승인해주는 로직
    path('inactive/', views.inactive, name='inactive'), #퇴사 및 휴직 관리 화면
    path('disable/<int:id>/', views.disable, name='disable'), #비활성화 시킴
    path('active/<int:id>/', views.active, name='active'), #활성화 시킴
    path('leave_active/<int:id>/', views.leave_active, name='leave_active'), #휴직자로 변경
    path('retire_active/<int:id>/', views.retire_active, name='retire_active'), #퇴직자로 변경
    path('reject_active/<int:id>/', views.reject_active, name='reject_active'), #보류자로 변경
    path('test/', views.test, name='test'), #테스트
    path('search/', views.search, name='search'), #검색기능
    path('allow_search/', views.allow_search, name='allow_search'), #검색기능
    path('inactive_search/', views.inactive_search, name='inactive_search'), #검색기능


    path('list/board/', views.list, {'flag': 'board'}, name='board_list'),  # 공지사항 목록
    path('list/board/create/', views.board_create, name='board_create'),  # 공지사항 작성
    path('list/board/<int:id>/', views.board_detail, name='board_detail'),  # 공지사항 상세보기
]