from django import forms


# 퀴즈 제출 폼
class QuizForm(forms.Form):
    answers = forms.JSONField()