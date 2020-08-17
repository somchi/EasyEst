from django.contrib import admin
from .models import Providers, ServiceType, ProviderBuild, RequestServices, RequestInterest, ServiceIcon

admin.site.register(Providers)
admin.site.register(ServiceType)
admin.site.register(ProviderBuild)
admin.site.register(RequestServices)
admin.site.register(ServiceIcon)
admin.site.register(RequestInterest)

# Register your models here.
