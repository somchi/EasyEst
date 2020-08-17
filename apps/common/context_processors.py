from Services.models import ServiceType
from django.views import generic

def ListServiceType(request):
    services = ServiceType.objects.order_by('pk')
    context = {'services':services}
    return context