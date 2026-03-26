from pathlib import Path
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = 'django-insecure-_t9m6tmh-!pec$5*y991uiz4n-ziw*f5=#q-)28_ib@@!9isy&'

DEBUG = True

ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
    "yukiko-nonconvertible-meanspiritedly.ngrok-free.dev"
]


SITE_ID = 1

CSRF_TRUSTED_ORIGINS = [
    "https://yukiko-nonconvertible-meanspiritedly.ngrok-free.dev",
    "http://127.0.0.1:8000"
]

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


# APPLICATIONS
INSTALLED_APPS = [
    'daphne',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    # ALLAUTH
    'allauth',
    'allauth.account',
    'allauth.socialaccount',

    # PROVIDERS
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.github',
    'allauth.socialaccount.providers.openid_connect',

    'users',
    'posts',
    'notifications',
    'channels',
]

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("127.0.0.1", 6379)],
        },
    },
}


# MIDDLEWARE
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]


# AUTHENTICATION
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]


ROOT_URLCONF = 'blogsite.urls'


# TEMPLATES
TEMPLATES = [
{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [BASE_DIR / "blogsite/templates"],
    'APP_DIRS': True,

    'OPTIONS': {
        'context_processors': [
            "django.template.context_processors.debug",
            'django.template.context_processors.request',
            'django.contrib.auth.context_processors.auth',
            'django.contrib.messages.context_processors.messages',
        ],
    },
}
]


WSGI_APPLICATION = 'blogsite.wsgi.application'

ASGI_APPLICATION = 'blogsite.asgi.application'


# DATABASE
DATABASES = {
'default': {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': BASE_DIR / 'db.sqlite3',
}
}


# PASSWORD VALIDATION
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


# INTERNATIONALIZATION
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'

USE_I18N = True
USE_TZ = True


# STATIC FILES
STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

STATIC_ROOT = BASE_DIR / "staticfiles"


# CUSTOM USER
AUTH_USER_MODEL = 'users.CustomUser'


# LOGIN REDIRECTS
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/posts/read/'
LOGOUT_REDIRECT_URL = '/accounts/login/'


# EMAIL CONFIG
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

EMAIL_HOST_USER = 'zf51283@gmail.com'
EMAIL_HOST_PASSWORD = 'ppovicudfrepiosy'

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER


# DJANGO ALLAUTH SETTINGS
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_EMAIL_VERIFICATION = "none"

SOCIALACCOUNT_LOGIN_ON_GET = True
SOCIALACCOUNT_AUTO_SIGNUP = True

ACCOUNT_UNIQUE_EMAIL = True

SOCIALACCOUNT_EMAIL_AUTHENTICATION = True
SOCIALACCOUNT_EMAIL_AUTHENTICATION_AUTO_CONNECT = True

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'allauth': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}


# CONSENT SCREEN + SOCIAL LOGIN CONFIG
SOCIALACCOUNT_PROVIDERS = {

    'google': {

        'SCOPE': [
            'profile',
            'email',
        ],

        'AUTH_PARAMS': {

            'access_type': 'online',

            'prompt': 'select_account consent'

        }

    },

    'facebook': {

        'METHOD': 'oauth2',

        'SCOPE': [
            'email',
            'public_profile'
        ],

        'FIELDS': [
            'id',
            'email',
            'name'
        ],

        'VERSION': 'v17.0'

    },

    'github': {

        'SCOPE': [
            'user',
            'user:email'
        ],

        'AUTH_PARAMS': {

            'prompt': 'login',

        }

    },

    'openid_connect': {
        'APPS': [
            {
                'provider_id': 'linkedin',
                'name': 'LinkedIn',
                'client_id': config('LINKEDIN_CLIENT_ID'),
                'secret': config('LINKEDIN_CLIENT_SECRET'),

                'settings': {
                    # 'server_url': 'https://www.linkedin.com',
                    'server_url': 'https://www.linkedin.com/oauth/.well-known/openid-configuration',
                    'scope': ['openid', 'profile', 'email'],
                    # 'redirect_uri': 'http://127.0.0.1:8000/accounts/oidc/linkedin/login/callback/',
                }
            }
        ],
    }

}


# CUSTOM ADAPTERS

SOCIALACCOUNT_ADAPTER = "users.adapters.SocialAccountAdapter"