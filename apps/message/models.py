from django.db import models
from Services.models import Providers
from common.models import Profile
from Agents.models import PropertyUpload

class MessageProvider(models.Model):
    receiver = models.ForeignKey(Providers)
    sender = models.ForeignKey(Profile)
    sender_name = models.CharField(max_length=200)
    message_subject = models.CharField(max_length=255)
    message = models.TextField()
    phone = models.CharField(max_length=11)
    date_created = models.DateTimeField(editable=False, auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return self.sender.user.username

class Chart(models.Model):
    user = models.ForeignKey(Profile)
    message = models.TextField()
    date_create = models.DateTimeField(auto_now_add=True)

class EmailSeller(models.Model):
    property = models.ForeignKey(PropertyUpload)
    receiver = models.ForeignKey(Profile)
    your_name = models.CharField(max_length=255)
    email_address = models.EmailField()
    contact_no = models.CharField(max_length=11)
    message = models.TextField()
    subject = models.CharField(max_length=255)

    def __str__(self):
        return self.your_name

