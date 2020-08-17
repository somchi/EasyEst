from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    url(r'^accounts/direct/$', views.direct, name='direct'),
    url(r'^acbtds34(?P<user_id>\d+)6acbtds/create-profile/$', views.profile, name='create_profile'),
    url(r'^acfe131(?P<pk>\d+)6acbtds/profile/$', views.UserProfile.as_view(), name='profile'),
    url(r'^acfe131(?P<profile_id>\d+)6acbtds/jobs/$', views.availablejobs, name='available_jobs'),
    url(r'^accounts/common/$', views.common, name='common'),
    url(r'^acfe135(?P<pk>\d+)6acbtds/welcome/$', views.ProfileSetUp.as_view(), name='initial'),
    url(r'^acfe135(?P<pk>\d+)9acbtds/services-professionals/$', views.ListServiceType.as_view(), name='service'),
    url(r'^acfe131(?P<pk>\d+)6acbtds/provider-detail/$', views.ServiceProviderDetail.as_view(), name='provider_detail'),
    url(r'^send-msg/$', views.send_msg, name='send_msg'),
    url(r'^about/$', views.about, name='about_us'),
]