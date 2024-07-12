from django import forms
from .models import Questions

class QuestionsForm(forms.ModelForm):
    class Meta:
        model = Questions
        fields = ['pregunta', 'respuesta', 'token']