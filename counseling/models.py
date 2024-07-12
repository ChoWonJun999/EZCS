from django.db import models
from django.core.serializers.json import DjangoJSONEncoder
from json import JSONDecoder
from django.contrib.auth.models import User


class CustomerProfile(models.Model):
    """
    상담원이 응대한 고객의 정보
    """
    phone_number = models.CharField(
        unique=True,
        blank=True,
        null=True,
        max_length=20,
        verbose_name="Customer's Korea Phone Number",
        db_comment="Customer's Korea Phone Number",
    )

    name = models.CharField(
        max_length=24,
        verbose_name="Customer's Name",
        db_comment="Customer's Name"
    )

    birth_date = models.DateField(
        null=True,
        verbose_name="Customer's Birth Date",
        db_comment="Customer's Birth Date"
    )
    
    joined_date = models.DateField(
        verbose_name="Customer's Birth Date",
        db_comment="Customer's Birth Date"
    )
    
    address_code = models.IntegerField(
        null=True
        , blank=True
    )
    
    address = models.CharField(
        null=True
        , blank=True
        , max_length=255
    )

    address_detail = models.CharField(
        null=True
        , blank=True
        , max_length=255
    )

    create_time = models.DateTimeField(
        auto_now_add=True
        , verbose_name="Created Time"
        , db_comment="Created Time"
    )

    class Meta:
        db_table = "customer_profile"
        verbose_name = "Customer profile"
        verbose_name_plural = "Customer profile"


class Log(models.Model):
    """
    상담원의 챗봇 이용 기록
    """
    auth_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="User's ID",
        db_comment="User's ID",
        related_name='counseling_logs'
    )

    customer = models.ForeignKey(
        CustomerProfile,
        on_delete=models.CASCADE,
        verbose_name="Customer's PK",
        db_comment="Customer's PK",
    )

    inquiries = models.TextField(
        null=True
        , blank=True
        , verbose_name="Customer Inquiries"
        , db_comment="Customer Inquiries"
    )
    
    action = models.TextField(
        null=True
        , blank=True
        , verbose_name="Action for Customer Inquiries"
        , db_comment="Action for Customer Inquiries"
    )

    create_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Created Time",
        db_comment="Created Time",
    )

    update_time = models.DateTimeField(
        auto_now=True,
        verbose_name="Created Time",
        db_comment="Created Time",
    )
    
    class Meta:
        db_table = "counsel_log"
        verbose_name = "Counsel Chatbot Log"
        verbose_name_plural = "Counsel Chatbot Log"


class LogItem(models.Model):
    log = models.ForeignKey(
        Log
        , on_delete=models.CASCADE
        , verbose_name="Log PK"
        , db_comment="Log PK"
        , related_name='counseling_log_items'
    )

    CLASSIFY_CHOICES = [
        (0, 'Customer'),
        (1, 'Counselor'),
    ]

    classify = models.IntegerField(
        default=0,
        choices=CLASSIFY_CHOICES,
    )

    message = models.TextField(
        verbose_name="Customer or counselor's message"
        , db_comment="Customer or counselor's message"
    )

    translate = models.TextField(
        null=True
        , blank=True
        , verbose_name="Recommended response comments"
        , db_comment="Recommended response comments"
    )

    recommend = models.TextField(
        null=True
        , blank=True
        , verbose_name="Recommended response comments"
        , db_comment="Recommended response comments"
    )

    create_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Created Time",
        db_comment="Created Time",
    )

    class Meta:
        db_table = "counsel_log_item"
        verbose_name = "Counsel Log"
        verbose_name_plural = "Counsel Log"






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
