from django.db import models
from django.contrib.auth.models import User


class UserCounselLog(models.Model):
    """
    user 테이블과 counsel_log 테이블의 조인테이블
    """
    id = models.AutoField(
        primary_key=True,
        verbose_name="Auto created ID",
        db_comment="Auto created ID"
    )
    
    user_id = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="User's ID",
        db_comment="User's ID",
        db_column='user_id'
    )
    
    counsel_log_id = models.ForeignKey(
        "counseling.CounselLog",
        on_delete=models.CASCADE,
        verbose_name="User's Counsel Log ID",
        db_comment="User's Counsel Log ID",
        db_column='counsel_log_id'
    )
    
    class Meta:
        db_table = 'user_counsel_log'
        verbose_name = 'User Counsel Log'
        verbose_name_plural = 'Users Counsel Log'
    
    
class UserCounselChatbotLog(models.Model):
    """
    User 테이블과 counsel_chatbot_log 테이블의 조인테이블
    """
    id = models.AutoField(
        primary_key=True,
        verbose_name="Auto created ID",
        db_comment="Auto created ID"
    )
    
    user_id = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="User's ID",
        db_comment="User's ID",
        db_column='user_id'
    )
    
    counsel_chatbot_log_id = models.ForeignKey(
        "counseling.CounselLog",
        on_delete=models.CASCADE,
        verbose_name="User's Counsel Chatbot Log ID",
        db_comment="User's Counsel Chatbot Log ID",
        db_column='counsel_chatbot_log_id'
    )
    
    class Meta:
        db_table = 'user_counsel_chatbot_log'
        verbose_name = 'User Counsel Chatbot Log'
        verbose_name_plural = 'Users Counsel Chatbot Log'

class UserEducationChatbotLog(models.Model):
    """
    User 테이블과 education_chatbot_log 테이블의 조인테이블
    """
    id = models.AutoField(
        primary_key=True,
        verbose_name="Auto created ID",
        db_comment="Auto created ID"
    )
    
    user_id = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="User's ID",
        db_comment="User's ID",
        db_column='user_id'
    )
    
    education_chatbot_log_id = models.ForeignKey(
        "education.Log",
        on_delete=models.CASCADE,
        verbose_name="User's Education Chatbot Log ID",
        db_comment="User's Education Chatbot Log ID",
        db_column='education_chatbot_log_id'
    )
    
    class Meta:
        db_table = 'user_education_chatbot_log'
        verbose_name = 'User Education Chatbot Log'
        verbose_name_plural = 'Users Education Chatbot Log'

class UserEducationQuiz(models.Model):
    """
    User 테이블과 education_quiz 테이블의 조인테이블
    """
    id = models.AutoField(
        primary_key=True,
        verbose_name="Auto created ID",
        db_comment="Auto created ID"
    )
    
    user_id = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="User's ID",
        db_comment="User's ID",
        db_column='user_id'
    )
    
    education_quiz_id = models.ForeignKey(
        "education.Quiz",
        on_delete=models.CASCADE,
        verbose_name="User's Education Quiz ID",
        db_comment="User's Education Quiz ID",
        db_column='education_quiz_id'
    )
    
    class Meta:
        db_table = 'user_education_quiz'
        verbose_name = 'User Education Quiz'
        verbose_name_plural = 'Users Education Quiz'