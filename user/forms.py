from django import forms
from .models import Nakrutka


class NakrutkaForm(forms.ModelForm):
    class Meta:
        model = Nakrutka
        fields = ['username', 'password']


