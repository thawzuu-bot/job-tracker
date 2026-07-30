from django import forms
from .models import JobApplication, Event


class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = '__all__'
        widgets = {
            'date_applied': forms.DateInput(attrs={'type': 'date'}),
        }


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['application', 'date', 'note']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }
