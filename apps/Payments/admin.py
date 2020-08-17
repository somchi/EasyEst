from django.contrib import admin
from .models import FundAccount, PromotionCategories, PromoteProperty, DebitsTrasactions, PayForCustomRequest, ProviderIncome

admin.site.register(FundAccount)
admin.site.register(PromotionCategories)
admin.site.register(PromoteProperty)
admin.site.register(DebitsTrasactions)
admin.site.register(PayForCustomRequest)
admin.site.register(ProviderIncome)

# Register your models here.
