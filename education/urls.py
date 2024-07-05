from django.urls import path 
from . import views

app_name = 'education'

urlpatterns = [
    # 롤플레잉 페이지
    path('', views.chat_view, name='chat_view'),

    # 교육 이력 페이지
    path('edu_history/', views.edu_history, name='edu_history'),

    # 퀴즈 페이지 
    path('quiz/', views.quiz, name='quiz'),

    # 교육 이력 상세 페이지
    path('details/', views.details, name='details'),  
    # 일단 어떻게 연결해야할지 모르겠어서 일단 연결해뇠는데, history에서 확인 누르면 해당 기록 열려야함
]
