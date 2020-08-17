"""
Django settings for EasyEstate project.

Generated by 'django-admin startproject' using Django 1.10.1.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_DIR = os.path.join(BASE_DIR, 'EasyEstate')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '!9!07(g^bnhq$*rd$v55ga&_h(t3ope+fh=rdo8w&ea(86@$h('

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sites',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'django_comments',
    'mptt',
    'tagging',
    'zinnia',
    'registration',
    'Agents',
    'Blog',
    'message',
    'ControlPanel',
    'Customers',
    'FAQ',
    'Order',
    'Payments',
    'Promotion',
    'Services',
    'SocialMedia',
    'state',
    'common',
]

SITE_ID = 5

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'EasyEstate.middleware.LoginRequiredMiddleware',
]

ROOT_URLCONF = 'EasyEstate.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(PROJECT_DIR, "templates"),

        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'common.context_processors.ListServiceType',
                'Agents.processor.PropertyCategory',
                'Agents.processor.PropertyMaxPrice',
                'Agents.processor.listed_pro',
                'Agents.processor.Properties',
                'Agents.processor.PromotedProperties',
                'Agents.processor.state',
                'Services.processor.service_type',
                'Payments.processor.featured',
                'Payments.processor.active_users',
                'Payments.processor.featured_jobs',
                'zinnia.context_processors.version',
            ],
        },
    },
]

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'mailing.easyestate@gmail.com'
EMAIL_HOST_PASSWORD = 'chisom@easy11'
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'EasyEstate.com.ng <noreply@easyestate.com.ng>'

WSGI_APPLICATION = 'EasyEstate.wsgi.application'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}    # Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'EasyEstate',
        'USER': 'EasyEstate',
        'PASSWORD': 'easyestate',
        'HOST': '',
        'PORT': '',
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = False

ADMINS = (
    ('Ike Chisom', 'accomodopro@googlemail.com'),
)

MANAGERS = ADMINS


LOGIN_REDIRECT_URL = '/common/accounts/direct/'
LOGIN_URL = '/accounts/login/'
LOGIN_EXEMPT_URLS = ('', 'api/auth/token/', 'api/.*', 'account/password-reset/', 'account/password-rest/done/')

ACCOUNT_ACTIVATION_DAYS = 1
REGISTRATION_OPEN = True
ACCOUNT_AUTHENTICATED_REGISTRATION_REDIRECTS = False
INCLUDE_AUTH_URLS =True
INCLUDE_REGISTER_URL =True
REGISTRATION_USE_SITE_EMAIL =True
REGISTRATION_SITE_USER_EMAIL = 'Admins'
REGISTRATION_EMAIL_HTML = False
REGISTRATION_FORM = 'common.forms.AccountCreationForm'
ACTIVATION_EMAIL_SUBJECT = 'registration/activation_email_subject.txt'
ACTIVATION_EMAIL_BODY = 'registration/activation_email.txt'
ACTIVATION_EMAIL_HTML = 'registration/activate.html'
REGISTRATION_DEFAULT_FROM_EMAIL = 'EasyEstate'


AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'EasyEstate.backends.EmailOrUsernameModelBackend',
]

FIXTURE_DIRS =(
    os.path.join(BASE_DIR, 'fixtures'),
)
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(PROJECT_DIR, "static"),
]

STATIC_ROOT = os.path.join(BASE_DIR, "static")

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, "media")