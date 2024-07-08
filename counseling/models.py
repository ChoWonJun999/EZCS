from django.db import models
from django.core.serializers.json import DjangoJSONEncoder
from json import JSONDecoder
from django.contrib.auth.models import User

class CounselLog(models.Model):
    # 상담원의 상담 내역
    username = models.CharField(
        max_length=16,
        verbose_name="Account's Username",
        db_comment="Account's Username",
    )

    phone_number = models.ForeignKey(
        "CustomerInfo",
        on_delete=models.CASCADE,
        verbose_name="Customer's Korea Phone Number(from customer_info)",
        db_comment="Customer's Korea Phone Number(from customer_info)",
        db_column='phone_number'
    )

    body = models.JSONField(
        encoder=DjangoJSONEncoder,
        decoder=JSONDecoder,
        verbose_name="Counsel Body(JSON Format)",
        db_comment="Counsel Body(JSON Format)",
    )

    create_time = models.DateTimeField(
        auto_now_add=True,  # Insert된 시간이 저장
        verbose_name="Created Time",
        db_comment="Created Time",
    )

    memo = models.JSONField(
        encoder=DjangoJSONEncoder,
        decoder=JSONDecoder,
        verbose_name="Noted By Counselor",
        db_comment="Noted By Counselor",
        null=True,
    )

    class Meta:
        db_table = "counsel_log"
        verbose_name = "Counsel Log"
        verbose_name_plural = "Counsel Log"

    def __str__(self):
        return self.body

class CustomerInfo(models.Model):
    # 상담원이 응대한 고객의 정보
    phone_number = models.CharField(
        primary_key=True,
        max_length=11,
        verbose_name="Customer's Korea Phone Number",
        db_comment="Customer's Korea Phone Number",
    )

    name = models.CharField(
        max_length=24, verbose_name="Customer's Name", db_comment="Customer's Name"
    )

    birth_date = models.DateField(
        verbose_name="Customer's Birth Date", db_comment="Customer's Birth Date"
    )
    
    joined_date = models.DateField(
        verbose_name="Customer's Birth Date", db_comment="Customer's Birth Date"
    )
    
    address = models.CharField(
        max_length=255,
        verbose_name="User's Address",
        db_comment="User's Address"
    )

    class Meta:
        db_table = "customer_info"
        verbose_name = "Customer Info"
        verbose_name_plural = "Customer Info"

    def __str__(self):
        return self.name

class CounselManual(models.Model):
    # 상담원이 사용할 응대 매뉴얼
    category = models.CharField(
        max_length=24,
        verbose_name="Counsel Manual Category",
        db_comment="Counsel Manual Category"
    )
    
    body = models.JSONField(
        encoder=DjangoJSONEncoder,
        decoder=JSONDecoder,
        verbose_name="Counsel Manual body for Counselor",
        db_comment="Counsel Manual body for Counselor",
        null=True,
    )
    
    vector = models.JSONField(
        encoder=DjangoJSONEncoder,
        decoder=JSONDecoder,
        verbose_name="Counsel Manual Vector body for Counselor",
        db_comment="Counsel Manual Vector body for Counselor",
        null=True,
    )

    class Meta:
        db_table = "counsel_manual"
        verbose_name = "Counsel Manual"
        verbose_name_plural = "Counsel Manual"

    def __str__(self):
        return self.category

class CounselChatbotLog(models.Model):
    # 상담원의 챗봇 이용 기록
    user_id = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="User's ID",
        db_comment="User's ID",
        db_column='user_id'
    )
    
    body = models.JSONField(
        encoder=DjangoJSONEncoder,
        decoder=JSONDecoder,
        verbose_name="Chatbot body for Counselor",
        db_comment="Chatbot body body for Counselor",
        null=True,
    )
    
    create_time = models.DateTimeField(
        auto_now_add=True,  # Insert된 시간이 저장
        verbose_name="Created Time",
        db_comment="Created Time",
    )
    
    class Meta:
        db_table = "counsel_chatbot_log"
        verbose_name = "Counsel Chatbot Log"
        verbose_name_plural = "Counsel Chatbot Log"

    def __str__(self):
        return self.create_time
