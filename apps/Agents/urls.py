from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from . import views


urlpatterns = [
    url(r'^absre4g64(?P<user_id>\d+)4t5f/property-upload/$', views.propertyupload, name='property_upload'),
    url(r'^ausre4g64(?P<pk>\d+)4t5f/properties/$', views.UserProperties.as_view(), name='user_properties'),
    url(r'^(?P<request_id>\d+)/confirm_property_delete/$', views.deleteproperty, name='delete'),
    url(r'^acfe131(?P<pk>\d+)6acbtds/edit-property/$', views.PropertyUpdate.as_view(), name='edit_property'),
    url(r'^(?P<property_id>\d+)/promote-property/$', views.promoteproperty, name='promote_property'),
    url(r'^lga-search/$', views.ajax_lga_search, name='lga-search'),
    url(r'^state-search/$', views.ajax_state_search, name='state-search'),
    url(r'^search-result/$', views.findproperty, name='search'),
    url(r'^(?P<pk>\d+)/property-detail/$', views.PropertyDetail.as_view(), name='property_detail'),
    url(r'^ausre4g64(?P<pk>\d+)4t5f/ads/$', views.UserAds.as_view(), name='user_ads'),
]