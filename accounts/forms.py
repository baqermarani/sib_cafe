from django import forms
from .models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField


class UserCreationForm(forms.ModelForm):
    """Create a Form for creation User in Admin Panel and User Client"""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['personal_id', 'email', 'full_name', 'phone_number', ]

    def clean_password2(self):
        clean_data = self.cleaned_data
        if clean_data['password1'] and clean_data['password2'] and clean_data['password1'] != clean_data['password2']:
            raise ValidationError('Password don\'t match ! ')
        return clean_data['password2']

    def save(self, commit=True):
        user = super().save(commit=True)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """Create a Form for Updating User in Admin Panel"""
    password = ReadOnlyPasswordHashField(help_text="""Raw passwords are not stored,
         so there is no way to see this user's password, but you can change the password using 
         <a href=\"../password/\">this form</a>.""")

    class Meta:
        model = User
        fields = ['personal_id', 'email', 'full_name', 'phone_number', 'password']


class UserLoginForm(forms.Form):
    personal_id = forms.CharField(label='Personal ID', max_length=8)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    def clean_id(self):
        personal_id = self.cleaned_data['personal_id']
        if not User.objects.filter(personal_id=personal_id).exists():
            raise ValidationError('User Does Not Exist')
