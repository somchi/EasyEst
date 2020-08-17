from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from state.models import Country, State, LGA
from .validator import validate_phone

SEX_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
)

I_AM = (
    ('U', 'User'),
    ('A', 'Agent'),
    ('S', 'Service Provider'),
)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='users', blank=True)
    gender = models.CharField(max_length=1, choices=SEX_CHOICES, default='F')
    phone_number = models.CharField(max_length=11, validators=[validate_phone])
    full_name = models.CharField(max_length=200, default="", blank=False)
    address = models.TextField()
    country = models.ForeignKey(Country)
    state = models.ForeignKey(State)
    lga = models.ForeignKey(LGA)
    i_agree = models.BooleanField(default=False)


    class Meta:
        permissions = (
            ('is_a_user', 'Is a User'),
        )

    def __str__(self):
        return self.user.username

    @models.permalink
    def get_absolute_url(self):
        return ('common:profile', (), {'pk':self.pk})
