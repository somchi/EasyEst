from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from . import views


urlpatterns = [
    url(r'^absre4g64(?P<payee_id>\d+)4t5f/funding/$', views.fund, name='fund_account'),
    url(r'^fund-account/$', views.fundaccount, name='fundaccount'),
    url(r'^absre4g64(?P<id>\d+)5t5f/pay-summary/$', views.custompaysummary, name='custom_summary'),
    #url(r'^absre4g64(?P<id>\d+)5t5f/pay/$', views.payforcustomrequest, name='custom_payment'),
]