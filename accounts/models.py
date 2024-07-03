from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.sessions.backends.db import SessionStore
from django.conf import settings
from django.contrib.auth.signals import user_logged_in

class UserManager(BaseUserManager):
    """_summary_

    Args:
        BaseUserManager (_type_): _description_
    """
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, email, password, **extra_fields)

    def get_by_natural_key(self, username):
        return self.get(username=username)

class User(AbstractBaseUser, PermissionsMixin):
    """
    유저 정보(사용자/관리자)
    """
    id = models.AutoField(
        primary_key=True,
        verbose_name="Auto created ID",
        db_comment="Auto created ID"
    )
    
    username = models.CharField(
        max_length=16,
        unique=True,
        verbose_name="ID to use when login",
        db_comment="ID to use when login for the user"
    )
    
    password = models.CharField(
        max_length=128,
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
        verbose_name="Administrator status(0:General User, 1:Administrator User)",
        db_comment="Administrator status(0:General User, 1:Administrator User)"
    )
    
    birth_date = models.DateField(
        verbose_name="User's Birth Date",
        db_comment="User's Birth Date"
    )
    
    phone_number = models.CharField(
        verbose_name="User's Phone Number",
        db_comment="User's Phone Number"
    )
    
    address = models.CharField(
        verbose_name="User's Address",
        db_comment="User's Address"
    )
    
    department = models.CharField(
        verbose_name="User's Department",
        db_comment="User's Department"
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
        verbose_name="User Active Flag",
        db_comment="User Active Flag"
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
        verbose_name="In-service status(0:inactive, 1:active, 2:on leave, 3:retired, 4:rejection)",
        db_comment="In-service status(0:inactive, 1:active, 2:on leave, 3:retired, 4:rejection)"
    )
    
    date_joined = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Joined Date",
        db_comment="The date the user joined"
    )
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    objects = UserManager()

    class Meta:
        db_table = 'user'
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.name
    
class UserSession(models.Model):
    """
    중복로그인 제어 테이블
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
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
        # session.delete()
        session['blocked'] = True
        session.save()

    session_key = request.session.session_key
    UserSession.objects.create(user=user, session_key=session_key)


user_logged_in.connect(block_duplicate_login)