from django.db import models

class User(models.Model):
    # 유저 정보(사용자/관리자)
    id = models.AutoField(
        primary_key=True,
        verbose_name="Auto created ID",
        db_comment="Auto created ID"
    )
    
    password = models.CharField(
        max_length=64,
        verbose_name="Password",
        db_comment="User Password"
    )
    
    last_login = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Last login time",
        db_comment="Last login time"
    )
    
    is_superuser = models.BooleanField(
        default=False,
        verbose_name="Administrator status",
        db_comment="Administrator status"
    )
    
    username = models.CharField(
        max_length=16,
        unique=True,
        verbose_name="ID to use when login",
        db_comment="ID to use when login for the user"
    )
    
    name = models.CharField(
        max_length=30,
        verbose_name="The user's real name",
        db_comment="The user's real name"
    )
    
    email = models.EmailField(
        max_length=254,
        unique=True,
        verbose_name="Email Address",
        db_comment="The user's email address"
    )
    
    is_active = models.BooleanField(
        default=True,
        verbose_name="In-service status",
        db_comment="In-service status"
    )
    
    date_joined = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Joined Date",
        db_comment="The date the user joined"
    )

    class Meta:
        db_table = 'user'
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.name