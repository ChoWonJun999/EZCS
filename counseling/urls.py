from django.urls import path 
from . import views

app_name = 'counseling'

urlpatterns = [
    path('', views.list, name='list'),
    path('stt/', views.stt, name='stt'),
    path('stt_chat/', views.stt_chat, name='stt_chat'),
]
