from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^art5e3(?P<user_id>\d+)e4th5/message-provider/$', views.messageprovider, name='message_provider'),
    url(r'^ars5e3(?P<pk>\d+)e4th5/messages/$', views.MessageProviderDetail.as_view(), name='messages'),
    url(r'^ars5e3(?P<user_id>\d+)e4th5/chart/$', views.chat, name='chart'),
    url(r'^(?P<sender_id>\d+)/suggestion/$', views.mail_suggestion, name='suggestion'),
    url(r'^(?P<property_id>\d+)/email-seller/$', views.emailseller, name='create'),
]
