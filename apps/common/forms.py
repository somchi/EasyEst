from django import forms
from .models import Profile
import datetime
from django.contrib.auth.models import User, Permission
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django_registration.forms import RegistrationFormUniqueEmail
from django.forms.widgets import PasswordInput, TextInput, EmailInput
from django.contrib.auth.hashers import make_password

class AccountCreationForm(RegistrationFormUniqueEmail):
    username = forms.CharField(widget=TextInput(attrs={'class': 'form-control','placeholder': 'your username'}))
    email = forms.EmailField(widget=EmailInput(attrs={'class': 'form-control','placeholder':'your email address'}))
    password1 = forms.CharField(widget=PasswordInput(attrs={'class': 'form-control','placeholder':'*******'}))
    password2 = forms.CharField(widget=PasswordInput(attrs={'class': 'form-control', 'placeholder': '*******'}))

class AuthenticationFormWithPlaceholder(AuthenticationForm):
    username = forms.CharField(widget=TextInput(attrs={'class': 'form-control','placeholder': 'Username or Email'}))
    password = forms.CharField(widget=PasswordInput(attrs={'class': 'form-control','placeholder':'Password'}))


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ('user', )
        widgets = {
            'country': forms.Select(attrs={'class': 'form-control'}),
            'state': forms.Select(attrs={'class': 'form-control'}),
            'lga': forms.Select(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.NumberInput(attrs={'class': 'form-control'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control'}),
            'i_agree': forms.CheckboxInput(attrs={'class': 'form-control', 'required':'True'})

        }

    def save(self, user):
        profile = super(ProfileForm, self).save(commit=False)
        profile.user = user
        profile.save()
        permission = Permission.objects.get(codename='is_a_user')
        user.user_permissions.add(permission)
        profile.save()

class PasswordResetFormWithPlaceholder(PasswordResetForm):
    email = forms.CharField(widget=TextInput(attrs={'class': 'form-control','placeholder': 'Email'}))

class PasswordSetFormWithPlaceholder(SetPasswordForm):
    new_password1 = forms.CharField(widget=PasswordInput(attrs={'class': 'form-control','placeholder': 'New Password'}))
    new_password2 = forms.CharField(widget=PasswordInput(attrs={'class': 'form-control','placeholder': 'Confirm New Password'}))





