from django.forms import ModelForm
from .models import MatchRecord
from django import forms

class DateInput(forms.DateInput):
    input_type = 'date'

class TextAreaInput(forms.DateInput):
    input_type = 'textarea'

class SampleForm(ModelForm):
    class Meta:
        model = MatchRecord
        fields = [
                'game_name',
                'game_date',
                'my_title',
                'opp_title',
                'win_lose',
                'comment',
                'frirst_strike',
                'battle_division'
        ]
        
        widgets = {
                'game_date': DateInput(),
                'comment':forms.Textarea(attrs={'rows':4,})
        }