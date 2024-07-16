from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator

# Create your models here.

class Board(models.Model):
    """
    관리자 공지사항
    """
    auth_user = models.ForeignKey(
        User
        , on_delete=models.CASCADE
        , related_name='management_board'
    )
    
    title = models.TextField(
        verbose_name="board title"
        , db_comment="board title"
    )
    
    body = models.TextField(
        verbose_name="board body"
        , db_comment="board body"
    )
    
    file = models.FileField(
        upload_to='uploads/%Y/%m/%d/',
        null=True,
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])]
    )
    
    FLAG_CHOICES = [
        (0, 'activate'),
        (1, 'deactivate'),
    ]
    
    flag = models.IntegerField(
        default=0,
        choices=FLAG_CHOICES,
    )
    
    create_time = models.DateTimeField(
        auto_now_add=True
        , verbose_name="Created Time"
        , db_comment="Created Time"
    )
    
    update_time = models.DateTimeField(
        auto_now=True
        , verbose_name="Created Time"
        , db_comment="Created Time"
    )