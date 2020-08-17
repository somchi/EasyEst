from django.contrib import admin
from .models import MessageProvider, EmailSeller
# Register your models here.
admin.site.register(MessageProvider)
admin.site.register(EmailSeller)