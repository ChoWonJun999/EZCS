from django.urls import path 
from . import views

app_name = 'counseling'

urlpatterns = [
    path('', views.list, name='list'),
    path('test', views.test, name='test'),
    path('stt/', views.stt, name='stt'),
    path('stt_chat/', views.stt_chat, name='stt_chat'),
    # path('customer_detail/', views.customer_detail, name='customer_detail')
]
