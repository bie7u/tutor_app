from django.db.models.base import Model
from django.forms import ModelForm
from .models import Notice, ReserveTutoring
from django import forms

class NoticeForm(ModelForm):

    class Meta:
        model = Notice
        fields = '__all__'
        exclude = ['user', 'data']

class DateInput(forms.DateInput):
    input_type = 'date'
 
class TimeInput(forms.TimeInput):
    input_type = 'time'

class ReserveTutoringForm(ModelForm):

    class Meta:
        model = ReserveTutoring
        fields = '__all__'
        exclude = ['user', 'tutor']
        widgets = {
            'expiration_date': DateInput(),
            'hours': TimeInput(),
        }


class ReserveTutoringFormSecond(ModelForm):
    
    class Meta:
        model = ReserveTutoring
        fields = ('agree', 'accept')
        exclude = ['user', 'tutor', 'city', 'street', 'number', 'expiration_date', 'hours']

    def clean_website_rules(self):
        data = self.cleaned_data['agree']
        if data == False:
            print('asdf')
            raise forms.ValidationError("please accept the rules of the website")
        else:
            return data