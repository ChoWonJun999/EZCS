from django.urls import path 
from . import views

app_name = 'education'

urlpatterns = [
    path('', views.chat_view, name='chat_view'),
    path('edu_history/', views.edu_history, name='edu_history'),
    path('quiz/', views.quiz, name='quiz'),
    path('details/', views.details, name='details'),  
    # 일단 어떻게 연결해야할지 모르겠어서 일단 연결해뇠는데, history에서 확인 누르면 해당 기록 열려야함

    # chat 어떻게 동작되는지 보는 용도의 urls
    path('chat/', views.chat_view_test, name='chat_view_test'), 
]
