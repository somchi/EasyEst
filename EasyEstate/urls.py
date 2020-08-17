"""EasyEstate URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from django.core.urlresolvers import reverse_lazy
from common.forms import PasswordResetFormWithPlaceholder
from common.forms import PasswordSetFormWithPlaceholder
from django.contrib.sitemaps.views import index
from django.contrib.sitemaps.views import sitemap
from zinnia.sitemaps import AuthorSitemap
from zinnia.sitemaps import CategorySitemap
from zinnia.sitemaps import EntrySitemap
from zinnia.sitemaps import TagSitemap


blog_urls = ([
    url(r'^', include('zinnia.urls.capabilities')),
    url(r'^search/', include('zinnia.urls.search')),
    url(r'^sitemap/', include('zinnia.urls.sitemap')),
    url(r'^trackback/', include('zinnia.urls.trackback')),
    url(r'^blog/tags/', include('zinnia.urls.tags')),
    url(r'^blog/feeds/', include('zinnia.urls.feeds')),
    url(r'^blog/random/', include('zinnia.urls.random')),
    url(r'^blog/authors/', include('zinnia.urls.authors')),
    url(r'^blog/categories/', include('zinnia.urls.categories')),
    url(r'^blog/comments/', include('zinnia.urls.comments')),
    url(r'^blog/entries/', include('zinnia.urls.entries')),
    url(r'^blog/archives/', include('zinnia.urls.archives')),
    url(r'^blog/shortlink', include('zinnia.urls.shortlink')),
    url(r'^blog/quick_entry/', include('zinnia.urls.quick_entry'))
])

sitemaps = {
    'tags': TagSitemap,
    'blog': EntrySitemap,
    'authors': AuthorSitemap,
    'categories': CategorySitemap
}

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', TemplateView.as_view(template_name='index.html'), name='index'),
    url(r'^accounts/', include('registration.backends.default.urls', namespace='accounts')),
    url(r'^account/logout/$', auth_views.logout, {'next_page': reverse_lazy('index')}, name='logout'),
    url(r'^accounts/register/complete/$', TemplateView.as_view(template_name='registration/registration_complete.html'),name='registration_complete'),
    url(r'^accounts/activate/complete/$', TemplateView.as_view(template_name='registration/activation_complete.html'),name='registration_activation_complete'),
    url(r'^account/password-reset/$', auth_views.password_reset, {'password_reset_form': PasswordResetFormWithPlaceholder}, name='password_reset'),
    url(r'^account/password-rest/done/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^account/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', auth_views.password_reset_confirm, {'set_password_form': PasswordSetFormWithPlaceholder}, name='password_reset_confirm'),
    url(r'^account/reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),
    url(r'^', include(blog_urls)),
    url(r'^blog/', include('zinnia.urls')),
    url(r'^comments/', include('django_comments.urls')),
    url(r'^agents/', include('Agents.urls', namespace='agents')),
    #url(r'^blog/', include('Blog.urls', namespace='blog')),
    url(r'^message/', include('message.urls', namespace='message')),
    url(r'^controlpanel/', include('ControlPanel.urls', namespace='control')),
    url(r'^customers/', include('Customers.urls', namespace='customers')),
    url(r'^faq/', include('FAQ.urls', namespace='faq')),
    url(r'^order/', include('Order.urls', namespace='order')),
    url(r'^payments/', include('Payments.urls', namespace='payments')),
    url(r'^promotion/', include('Promotion.urls', namespace='promotion')),
    url(r'^service/', include('Services.urls', namespace='service')),
    url(r'^socialmedia/', include('SocialMedia.urls', namespace='social')),
    url(r'^common/', include('common.urls', namespace='common')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [
    url(r'^sitemap.xml$', index, {'sitemaps': sitemaps}),
    url(r'^sitemap-(?P<section>.+)\.xml$', sitemap, {'sitemaps': sitemaps},name='django.contrib.sitemaps.views.sitemap'),
]
