from django.db import models
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.auth.signals import user_logged_in
from django.contrib.auth.models import User


class AdministratorProfile(models.Model):
    """
    관리자 계정
    """
    auth_user = models.OneToOneField(
        User
        , on_delete=models.CASCADE
        , related_name='administrator_profile'
    )

    birth_date = models.DateField(
        null=True
        , blank=True
    )
    
    phone_number = models.CharField(
        null=True
        , blank=True
        , max_length=20
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
    
    department = models.CharField(
        null=True
        , blank=True
        , max_length=255
    )

    class Meta:
        db_table = "administrator_profile"


class CounselorProfile(models.Model):
    """
    상담사 계정
    """
    auth_user = models.OneToOneField(
        User
        , on_delete=models.CASCADE
        , related_name='counselor_profile'
    )

    birth_date = models.DateField(
        null=True
        , blank=True
    )
    
    phone_number = models.CharField(
        null=True
        , blank=True
        , max_length=20
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
    
    department = models.CharField(
        null=True
        , blank=True
        , max_length=255
    )
    
    ACTIVE_STATUS_CHOICES = [
        (0, 'Inactive'),
        (1, 'Active'),
        (2, 'On Leave'),
        (3, 'Retired'),
        (4, 'Rejection')
    ]
    
    active_status = models.IntegerField(
        default=0,
        choices=ACTIVE_STATUS_CHOICES,
    )

    class Meta:
        db_table = "counselor_profile"

    
class UserSession(models.Model):
    """
    중복로그인 제어 테이블
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    session_key = models.CharField(max_length=40)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'user_session'
        verbose_name = 'User Session'
        verbose_name_plural = 'Users Session'


def block_duplicate_login(sender, request, user, **kwargs):
    login_user_list = UserSession.objects.filter(user=user)

    for user_session in login_user_list:
        session = SessionStore(user_session.session_key)
        session['blocked'] = True
        session.save()

    session_key = request.session.session_key
    UserSession.objects.create(user=user, session_key=session_key)


user_logged_in.connect(block_duplicate_login)