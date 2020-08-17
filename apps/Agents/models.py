from django.db import models
from common.models import Profile
import datetime
from django.urls import reverse
from state.models import State, LGA
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import User


SEX_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
)

HOW = (
    ('FF', 'From a Friend'),
    ('SM', 'Social Media'),
    ('OF', 'From our Orientation Meeting'),
    ('FG', 'From Google'),
    ('FE', 'From Email'),
)

STATUS = (
    ('Running', 'Running'),
    ('Expired', 'Expired'),
)


class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.name

class Available(models.Model):
    property_type = models.CharField(max_length=50, default='Rent')

    def __str__(self):
        return self.property_type

class PriceRange(models.Model):
    price = models.DecimalField(max_digits=15, decimal_places=0)


class PropertyUpload(models.Model):
    STATUS = (
        ('Running', 'Running'),
        ('Expired', 'Expired'),
        ('Pending', 'Pending'),
        ('Rejected', 'Rejected'),
        ('Approved', 'Approved'),
    )

    created_by = models.ForeignKey(Profile, on_delete=models.CASCADE)
    property_type = models.ForeignKey(Category, null=True, on_delete=models.CASCADE)
    availability_type = models.ForeignKey(Available, null=True, on_delete=models.CASCADE)
    main_view = models.ImageField(upload_to='Agents')
    right_view = models.ImageField(upload_to='Agents', blank=True)
    back_view = models.ImageField(upload_to='Agents', blank=True)
    left_view = models.ImageField(upload_to='Agents', blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=15, decimal_places=0)
    number_of_room = models.CharField(max_length=10, blank=True)
    number_of_toilet = models.CharField(max_length=10, blank=True)
    number_of_baths = models.CharField(max_length=10, blank=True)
    property_state = models.ForeignKey(State, on_delete=models.CASCADE)
    property_lga = models.ForeignKey(LGA, on_delete=models.CASCADE)
    water = models.CharField(max_length=100, blank=True)
    power = models.CharField(max_length=100, blank=True)
    date_created = models.DateField(editable=False, auto_now_add=True)
    date_expire = models.DateTimeField()
    is_expired = models.BooleanField()
    status = models.CharField(max_length=50, choices=STATUS, default='Pending')
    running = models.CharField(max_length=10, choices=STATUS, default='Running')

    class Meta:
        ordering = ['-date_created']

    def save(self):
        date = datetime.timedelta(days=30)
        if not self.id:
            self.date_expire = datetime.datetime.now() + date
        super(PropertyUpload, self).save()

    def __str__(self):
        return self.property_type.name

    def get_absolute_url(self):
        return reverse('agents:user_properties', kwargs={'pk': self.created_by.pk})








