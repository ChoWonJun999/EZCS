from django.db import models
from django.contrib.auth.models import User


class Log(models.Model):
    """
    교육 이력 HEADER
    """
    auth_user = models.ForeignKey(
        User
        , on_delete=models.CASCADE
        , verbose_name="User's ID"
        , db_comment="User's ID"
        , related_name='education_logs'
    )

    CATEGORY_CHOICES = [
        (0, 'Additional')
        , (1, 'Policies')
        , (2, 'Charges')
    ]

    category = models.IntegerField(
        default=0
        , choices=CATEGORY_CHOICES
        , verbose_name="Question Category"
        , db_comment="Question Category"
    )

    create_time = models.DateTimeField(
        auto_now_add=True
        , verbose_name="Created Time"
        , db_comment="Created Time"
    )

    class Meta:
        db_table = "edu_log"
        verbose_name = "Education Chatbot Log"
        verbose_name_plural = "Education Chatbot Log"


class LogItem(models.Model):
    """
    교육 이력 Item
    """
    log = models.ForeignKey(
        Log
        , on_delete=models.CASCADE
        , verbose_name="Log PK"
        , db_comment="Log PK"
        , related_name='education_log_items'
    )

    chatbot = models.TextField(
        verbose_name="Chatbot's message"
        , db_comment="Chatbot's message"
    )

    user = models.TextField(
        null=True
        , blank=True
        , verbose_name="User's message"
        , db_comment="User's message"
    )

    evaluate = models.TextField(
        null=True
        , blank=True
        , verbose_name="Chatbot's evaluate message"
        , db_comment="Chatbot's evaluate message"
    )

    create_time = models.DateTimeField(
        auto_now_add=True
        , verbose_name="Created Time"
        , db_comment="Created Time"
    )

    class Meta:
        db_table = "edu_log_item"
        verbose_name = "Education Chatbot Log Item"
        verbose_name_plural = "Education Chatbot Log Item"


class Quiz(models.Model):
    """
    교육 질문 문제집
    """
    flag = models.BooleanField(
        default=False
        , verbose_name="Question Method status(0:Short, 1:Multiple)"
        , db_comment="Question Method status(0:Short, 1:Multiple)"
    )

    question = models.TextField(
        verbose_name="Question"
        , db_comment="Question"
    )

    CATEGORY_CHOICES = [
        (0, 'Additional')
        , (1, 'Policies')
        , (2, 'Charges')
    ]

    category = models.IntegerField(
        default=0
        , choices=CATEGORY_CHOICES
        , verbose_name="Question Category"
        , db_comment="Question Category"
    )

    answer = models.TextField(
        verbose_name="Question Correct Answer(flag=0: TEXT, flag=1: Integer)"
        , db_comment="Question Correct Answer(flag=0: TEXT, flag=1: Integer)"
    )

    commentary = models.TextField(
        verbose_name="Question Commentary"
        , db_comment="Question Commentary"
    )

    choice1 = models.TextField(
        null=True
        , blank=True
        , verbose_name="Question Method Multiple Choice1"
        , db_comment="Question Method Multiple Choice1"
    )

    choice2 = models.TextField(
        null=True
        , blank=True
        , verbose_name="Question Method Multiple Choice2"
        , db_comment="Question Method Multiple Choice2"
    )

    choice3 = models.TextField(
        null=True
        , blank=True
        , verbose_name="Question Method Multiple Choice3"
        , db_comment="Question Method Multiple Choice3"
    )

    choice4 = models.TextField(
        null=True
        , blank=True
        , verbose_name="Question Method Multiple Choice4"
        , db_comment="Question Method Multiple Choice4"
    )

    create_time = models.DateTimeField(
        auto_now_add=True
        , verbose_name="Created Time"
        , db_comment="Created Time"
    )

    class Meta:
        db_table = "edu_quiz"
        verbose_name = "Education Quiz"
        verbose_name_plural = "Education Quiz"

    def __str__(self):
        return self.question


class QuizHistory(models.Model):
    """
    상담원의 챗봇 이용 기록
    """
    auth_user = models.ForeignKey(
        User
        , on_delete=models.CASCADE
        , verbose_name="User's ID"
        , db_comment="User's ID"
        , related_name="history_user"
    )
    
    CATEGORY_CHOICES = [
        (0, 'Additional')
        , (1, 'Policies')
        , (2, 'Charges')
    ]

    category = models.IntegerField(
        default=0
        , choices=CATEGORY_CHOICES
        , verbose_name="Question Category"
        , db_comment="Question Category"
    )
    
    create_time = models.DateTimeField(
        auto_now_add=True
        , verbose_name="Created Time"
        , db_comment="Created Time"
    )

    is_passed = models.BooleanField(
        default=False
        , verbose_name="Question is Passed(0:Fail, 1:Pass)"
        , db_comment="Question is Passed(0:Fail, 1:Pass)"
    )
    
    class Meta:
        db_table = "edu_quiz_hist"
        verbose_name = "Education Quiz History"
        verbose_name_plural = "Education Quiz History"


class QuizHistoryItem(models.Model):
    """
    상담원의 챗봇 이용 기록 상세 내역
    """
    quiz_history = models.ForeignKey(
        "QuizHistory"
        , on_delete=models.CASCADE
        , verbose_name="Quiz History Id"
        , db_comment="Quiz History Id"
    )

    quiz = models.ForeignKey(
        "Quiz"
        , on_delete=models.CASCADE
        , verbose_name="Quiz Id"
        , db_comment="Quiz Id"
    )

    answer = models.TextField(
        verbose_name="Question User Answer(Quiz.flag=0: TEXT, Quiz.flag=1: Integer)"
        , db_comment="Question User Answer(Quiz.flag=0: TEXT, Quiz.flag=1: Integer)"
    )

    class Meta:
        db_table = "edu_quiz_hist_item"
        verbose_name = 'Quiz History Detail'
        verbose_name_plural = 'Quiz History Detail'
    
    def __str__(self):
        return self.answer
    