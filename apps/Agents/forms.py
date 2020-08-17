from django import forms
from .models import PropertyUpload
from django.forms.widgets import PasswordInput, TextInput
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User, Permission
from django.contrib.auth.hashers import make_password

class PropertyUploadForm(forms.ModelForm):
    class Meta:
        model = PropertyUpload
        exclude = ('created_by', 'date_expire', 'running', 'status',)
        widgets = {
            "main_view": forms.FileInput(attrs={'class': 'form-control'}),
            "right_view": forms.FileInput(attrs={'class': 'form-control'}),
            "left_view": forms.FileInput(attrs={'class': 'form-control'}),
            "back_view": forms.FileInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder':'property price'}),
            'number_of_room': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Rooms'}),
            'number_of_toilet': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Toilets'}),
            'number_of_baths': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Baths'}),
            'water': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Water Availability'}),
            'power': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Power Availability'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'property_type': forms.Select(attrs={'class': 'form-control'}),
            'availability_type': forms.Select(attrs={'class': 'form-control'}),
            'property_state': forms.Select(attrs={'class': 'form-control'}),
            'property_lga': forms.Select(attrs={'class': 'form-control'}),
        }

    def save(self, user):
        created_by = super(PropertyUploadForm, self).save(commit=False)
        created_by.created_by = user
        created_by.save()

class PropertyUpdateForm(forms.ModelForm):
    class Meta:
        model = PropertyUpload
        fields = ('property_type', 'availability_type', 'main_view', 'right_view', 'back_view', 'left_view', 'description',
                  'price', 'number_of_room', 'number_of_toilet', 'number_of_baths', 'property_state', 'property_lga','water'
                  , 'power')
        widgets = {
            "main_view": forms.FileInput(attrs={'class': 'form-control'}),
            "right_view": forms.FileInput(attrs={'class': 'form-control'}),
            "left_view": forms.FileInput(attrs={'class': 'form-control'}),
            "back_view": forms.FileInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder':'property price'}),
            'number_of_room': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Rooms'}),
            'number_of_toilet': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Toilets'}),
            'number_of_baths': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Baths'}),
            'water': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Water Availability'}),
            'power': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Power Availability'}),
            'description': forms.Textarea(attrs={'class': 'form-control',}),
        }