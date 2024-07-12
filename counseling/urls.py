from django.urls import path
from . import views

app_name = "counseling"

urlpatterns = [
    path("", views.counsel, name="counsel"),

    path("update_log/", views.update_log, name="updateLog"),

    path("ai/", views.ai_model, name="aiModel"),

    path("history/", views.history, name="history"),

    path("detail/<int:id>/", views.detail, name="detail"),





    path("", views.list, name="list"),

    path("save_counseling_log/", views.save_counseling_log, name="save_counseling_log"),
    path("save_consultation/", views.save_consultation, name="save_consultation"),
    # path('evaluation_chat/', views.evaluation_chat, name='evaluation_chat'),

    # path('customer_detail/', views.customer_detail, name='customer_detail')
]
