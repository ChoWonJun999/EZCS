from django.urls import path
from . import views

app_name = "counseling"

urlpatterns = [
    path("", views.list, name="list"),
    path("history/", views.history, name="history"),
    # path("test", views.test, name="test"),
    path("stt/", views.stt, name="stt"),
    path("stt_chat/", views.stt_chat, name="stt_chat"),
    path("save_customer_info/", views.save_customer_info, name="save_customer_info"),
    path("save_counseling_log/", views.save_counseling_log, name="save_counseling_log"),
    path("save_consultation/", views.save_consultation, name="save_consultation"),

    # path('customer_detail/', views.customer_detail, name='customer_detail')
]
