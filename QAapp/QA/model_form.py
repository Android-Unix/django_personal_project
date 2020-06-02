from django import forms
from .models import Question , Answer
from account.models import Account

class CreateQuestion(forms.ModelForm):
    class Meta:
        model = Question
        fields = '__all__'

class CreateAnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['answer']


