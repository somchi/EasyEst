from .models import PromoteProperty
import datetime
from common.models import Profile
from Services.models import RequestServices

def featured(request):
    d = datetime.datetime.now()
    featured = PromoteProperty.objects.filter(expires__gte=d)
    context = {'featured':featured}
    return context

def active_users(request):
    active_users = Profile.objects.all()
    context_list = {'active_users':active_users}
    return context_list

def featured_jobs(request):
    jobs = RequestServices.objects.all()
    context = {'jobs':jobs}
    return context