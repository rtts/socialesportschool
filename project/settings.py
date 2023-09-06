import os, random, string
try:
    import uwsgi
    DEBUG = False
except ImportError:
    DEBUG = True
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
ADMINS = []
SECRET_KEY = ''.join(random.choice(string.printable) for x in range(50))
ALLOWED_HOSTS = ['*', 'localhost', 'sss.created.today', 'www.socialesportschool.nl']
ROOT_URLCONF = 'sss.urls'
WSGI_APPLICATION = 'project.wsgi.application'
LANGUAGE_CODE = 'nl'
TIME_ZONE = 'Europe/Amsterdam'
USE_I18N = True
USE_L10N = True
USE_TZ = True
STATIC_URL = '/static/'
STATIC_ROOT = '/srv/sss/static'
MEDIA_URL = '/media/'
MEDIA_ROOT = '/srv/sss/media'
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/mijnsss/'
ACCOUNT_ACTIVATION_DAYS = 7

import sss
SASS_PROCESSOR_ROOT = os.path.join(os.path.dirname(os.path.abspath(sss.__file__)), 'static')

INSTALLED_APPS = [
    'sss',
    'bootcamps',
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'ckeditor',
    'embed_video',
    'easy_thumbnails',
    'jquery',
    'jquery_ui',
]

INSTALLED_APPS += ['sass_processor']

CKEDITOR_CONFIGS = {
    'default': {
        'removePlugins': 'elementspath',
        # 'contentsCss': STATIC_URL + 'ckeditor.css',
        'width': '100%',
        'toolbar': 'Custom',
        'allowedContent': True, # this allows iframes, embeds, scripts, etc...
        'toolbar_Custom': [
            ['Bold', 'Italic', 'Underline'],
            ['NumberedList', 'BulletedList', 'Blockquote'],
            ['JustifyLeft', 'JustifyCenter', 'JustifyRight'],
            ['Link', 'Unlink'],
            ['Source'],
        ]
    }
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'USER': 'sss',
        'NAME': 'sss',
    }
}
