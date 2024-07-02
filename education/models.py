from django.db import models
from django.core.serializers.json import DjangoJSONEncoder
from json import JSONDecoder

class EducationChatbotLog(models.Model):
    # 상담원의 챗봇 이용 기록
    user_id = models.ForeignKey(
        "accounts.User",
        on_delete=models.CASCADE,
        verbose_name="User's ID",
        db_comment="User's ID",
        db_column='user_id'
    )
    
    body = models.JSONField(
        encoder=DjangoJSONEncoder,
        decoder=JSONDecoder,
        verbose_name="Chatbot body for Education AI",
        db_comment="Chatbot body body for Education AI",
        null=True,
    )
    
    create_time = models.DateTimeField(
        auto_now_add=True,  # Insert된 시간이 저장
        verbose_name="Created Time",
        db_comment="Created Time",
    )
    
    class Meta:
        db_table = "education_chatbot_log"
        verbose_name = "Education Chatbot Log"
        verbose_name_plural = "Education Chatbot Log"

    def __str__(self):
        return self.create_time

class EducationQuiz(models.Model):
    # 상담원의 챗봇 이용 기록
    user_id = models.ForeignKey(
        "accounts.User",
        on_delete=models.CASCADE,
        verbose_name="User's ID",
        db_comment="User's ID",
        db_column='user_id'
    )
    
    body = models.JSONField(
        encoder=DjangoJSONEncoder,
        decoder=JSONDecoder,
        verbose_name="Quiz for Education",
        db_comment="Quiz for Education",
        null=True,
    )
    
    create_time = models.DateTimeField(
        auto_now_add=True,  # Insert된 시간이 저장
        verbose_name="Created Time",
        db_comment="Created Time",
    )
    
    class Meta:
        db_table = "education_quiz"
        verbose_name = "Education Quiz"
        verbose_name_plural = "Education Quiz"

    def __str__(self):
        return self.create_time