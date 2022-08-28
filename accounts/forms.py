from django import forms
from .models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField


class UserCreationForm(forms.ModelForm):
    """Create a Form for creation User in Admin Panel"""
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


class UserRegistrationForm(forms.Form):

    email = forms.EmailField()
    personal_id = forms.CharField(max_length=8, label='Personal ID')
    full_name = forms.CharField(label='Full Name')
    phone_number = forms.CharField(label='Phone Number', max_length=11)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError('Email Already Exists')
        return email

    def clean_phone(self):
        phone = self.cleaned_data['phone_number']
        if User.objects.filter(phone_number=phone).exists():
            raise ValidationError('Phone Number Already Exists')
        return phone

    def clean_id(self):
        personal_id = self.cleaned_data['personal_id']
        if User.objects.filter(personal_id=personal_id).exists():
            raise ValidationError('User Already Exist')
        return personal_id


class UserLoginForm(forms.Form):
    personal_id = forms.CharField(label='Personal ID', max_length=8)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    def clean_id(self):
        personal_id = self.cleaned_data['personal_id']
        if not User.objects.filter(personal_id=personal_id).exists():
            raise ValidationError('User Does Not Exist')
