from django import forms
from .models import MessageProvider, EmailSeller

class MessageProviderForm(forms.ModelForm):
    class Meta:
        model = MessageProvider
        exclude = ('receiver', 'sender', 'read', )
        widgets = {
            'message_subject': forms.TextInput(attrs={'class': 'form-control','placeholder':'Your Email'}),
            'sender_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Your Message'}),
        }

    def save(self,user,sender):
        message = super(MessageProviderForm, self).save(commit=False)
        message.receiver = user
        message.sender = sender
        message.save()

class EmailSellerForm(forms.ModelForm):
    class Meta:
        model = EmailSeller
        exclude = ('property', 'receiver', )

    def save(self, property, receiver):
        email = super(EmailSellerForm, self).save(commit=False)
        email.property = property
        email.receiver = receiver
        email.save()