from django import forms

class QuizForm(forms.Form):
    answers = forms.CharField(widget=forms.HiddenInput())
    quiz_ids = forms.CharField(widget=forms.HiddenInput())