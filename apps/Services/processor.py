from .models import ServiceType

def service_type(request):
    ser_typ = ServiceType.objects.all()
    cat_context = {'ser_typ': ser_typ}
    return cat_context