from django.db import models
from django.core.serializers.json import DjangoJSONEncoder
from json import JSONDecoder

class CounselLog(models.Model):
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

    class Meta:
        db_table = "customer_info"
        verbose_name = "Customer Info"
        verbose_name_plural = "Customer Info"

    def __str__(self):
        return self.name