from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from common.models import Profile
import datetime
from django.utils import timezone

SEX_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
)

class ServiceIcon(models.Model):
    name = models.CharField(max_length=50, default='service')

    def __str__(self):
        return self.name

class ServiceType(models.Model):
    service = models.CharField(max_length=200)
    icon = models.ForeignKey(ServiceIcon, null=True, on_delete=models.CASCADE)
    service_code = models.CharField(max_length=4, blank=True)
    description = models.TextField()

    def __str__(self):
        return self.service

# the model for a user to create a service profile
class Providers(models.Model):
    provider = models.OneToOneField(Profile, on_delete=models.CASCADE)
    service_provided = models.ForeignKey(ServiceType, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200)
    since = models.DateField(help_text='When did you start')
    to = models.DateField(auto_now=True, help_text='till')
    major_experience = models.TextField()
    major_jobs_done = models.TextField(help_text="The jobs you have done, separated with a 'comma' ")
    service_pic = models.ImageField(upload_to='service_profile_picture', blank=True)
    starting_at = models.DecimalField(max_digits=50, decimal_places=0)
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name

    # @models.permalink
    def get_absolute_url(self):
        return reverse('service:manage_service', {'pk':self.pk})

# the model a user can use to request a specific service


class ProviderBuild(models.Model):
    provider = models.ForeignKey(Providers, on_delete=models.CASCADE)
    certificate_name = models.CharField(max_length=50, help_text='Evidence of a training done')
    cert_evidence = models.ImageField(upload_to='photo_evidence', blank=True)
    issuer = models.CharField(max_length=200, help_text='A recent job you just did')
    date_acquired = models.DateField()
    date_created = models.DateTimeField(auto_now_add=True)

# the model a user uses to make a request
class RequestServices(models.Model):
    RUNNING, CANCELLED, GRANTED = range(3)
    STATUS = (
        (RUNNING, 'Running'),
        (CANCELLED, 'Cancelled'),
        (GRANTED, 'Granted')
    )

    requester = models.ForeignKey(Profile, on_delete=models.CASCADE)
    type_of_service = models.ForeignKey(ServiceType, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS, default=RUNNING, editable=False)
    job_title = models.CharField(max_length=255)
    duration = models.CharField(max_length=20, help_text='How long the job will run', blank=True)
    location = models.CharField(max_length=300, default='Nigeria')
    price_from = models.DecimalField(max_digits=10, decimal_places=0)
    price_to = models.DecimalField(max_digits=10, decimal_places=0)
    date_created = models.DateField(auto_now_add=True, editable=False)
    date_approved = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.job_title

    def get_absolute_url(self):
        return reverse('service:my_requests', kwargs={'pk': self.requester.pk})



# the model a provider uses to bid for a request
class RequestInterest(models.Model):
    request = models.ForeignKey(RequestServices, on_delete=models.CASCADE)
    interested_person = models.ForeignKey(Providers, on_delete=models.CASCADE)
    my_offer = models.CharField(max_length=255)
    price_offer = models.DecimalField(max_digits=10, decimal_places=0)
    date_created = models.DateField(auto_now_add=True)
    duration = models.IntegerField(default=1)
    status = models.CharField(max_length=10, blank=True, default='Pending')
    due_date = models.DateTimeField(null=True)

    def __str__(self):
        return self.my_offer










