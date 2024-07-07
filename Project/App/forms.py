from django import forms
from .models import *

class MentorForm(forms.ModelForm):
    class Meta:
        model = Mentor
        fields = ['name', 'dob', 'email', 'gender', 'mobile']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'dob': forms.DateInput(attrs={'type': 'date'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'mobile': forms.TextInput(attrs={'class': 'form-control'}),
        }