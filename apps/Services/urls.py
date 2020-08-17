from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from . import views


urlpatterns = [
    url(r'^acfe131(?P<pk>\d+)6acbtds/manage-service/$', views.ManageService.as_view(), name='manage_service'),
    url(r'^acfe131(?P<user_id>\d+)6acbtds/create-profile/$', views.provider, name='create_profile'),
    url(r'^acfe131(?P<requester_id>\d+)6acbtds/custom-request/$', views.requestservice, name='request_service'),
    url(r'^acfe131(?P<request_id>\d+)6acbtds/request-interest/$', views.requestinterests, name='request_interest'),
    url(r'^acfe131(?P<pk>\d+)6acbtds/my-requests/$', views.MyRequest.as_view(), name='my_requests'),
    url(r'^acfe131(?P<pk>\d+)6acbtds/edit-requests/$', views.RequestServicesEdit.as_view(), name='edit_requests'),
    url(r'^(?P<request_id>\d+)/confirm_delete/$', views.deleterequest, name='delete'),
    url(r'^(?P<provider_id>\d+)/build-profile/$', views.buildprofile, name='build_profile'),
    url(r'^(?P<id>\d+)/approve-request/$', views.approverequest, name='approve_request'),
    url(r'^result/$', views.findprovider, name='search'),
]