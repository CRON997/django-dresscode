import os
from pathlib import Path

from django.utils.translation import gettext_lazy as _
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', ]

INTERNAL_IPS = [
    "127.0.0.1",
]

DOMAIN_MAIN = 'http://localhost:8000/'

DJANGO_APPS = ['unfold',
               'unfold.contrib.filters',
               'unfold.contrib.forms',
               'unfold.contrib.inlines',
               'unfold.contrib.import_export',
               'unfold.contrib.guardian',
               'unfold.contrib.simple_history',
               'django.contrib.admin',
               'django.contrib.auth',
               'django.contrib.contenttypes',
               'django.contrib.sessions',
               'django.contrib.messages',
               'django.contrib.staticfiles',
               'django.contrib.sites',
               ]

THIRD_PARTY_APPS = ['django_htmx',
                    'rosetta',
                    'parler',
                    'widget_tweaks',
                    'allauth',
                    'allauth.account',
                    'allauth.socialaccount',
                    'allauth.socialaccount.providers.google',
                    'debug_toolbar',
                    'rest_framework',
                    'django_filters',
                    ]

LOCAL_APPS = [
    'apps.main',
    'apps.cart',
    'apps.users',
    'apps.comments',
    'apps.orders',
    'apps.coupons',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_htmx.middleware.HtmxMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': '601578469699-06a18eu6uthi53hq9s4pduj4da0as86g.apps.googleusercontent.com',
            'secret': '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',
            'key': "",
        },
    }
}

SITE_ID = 1
ROOT_URLCONF = 'shop.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'apps.cart.context_processors.cart'
            ],
        },
    },
]

WSGI_APPLICATION = 'shop.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': os.getenv('POSTGRES_HOST', 'localhost'),
        'PORT': os.getenv('POSTGRES_PORT', 5432),
        'USER': os.getenv('POSTGRES_USER', 'postgres'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
        'NAME': os.getenv('POSTGRES_DB', 'db_01'),
        'ATOMIC_REQUEST': True,
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {'min_length': 8, }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en'
LANGUAGES = [
    ('en', _('English')),
    ('ru', _('Russian')),
    ('uk', _('Ukrainian')),
]

LOCALE_PATHS = [
    BASE_DIR / 'locale'
]

TIME_ZONE = 'Europe/Kyiv'

USE_I18N = True

USE_TZ = True

# STATIC FILES
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# MEDIA FILES
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CART_SESSION_ID = 'cart'
AUTH_USER_MODEL = 'users.CustomUser'

LOGING_URL = 'login'
LOGOUT_URL = 'logout'
LOGIN_REDIRECT_URL = '/'
ACCOUNT_LOGOUT_REDIRECT_URL = 'login'

# EMAIL
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False

PARLER_LANGUAGES = {
    None: (
        {'code': 'en'},
        {'code': 'ru'},
        {'code': 'uk'},
    ),
    'default': {
        'fallback': 'en',
        'hide_untranslated': False,
    }
}

# STRIPE
STRIPE_TEST_PUBLIC_KEY = os.getenv('STRIPE_TEST_PUBLIC_KEY')
STRIPE_TEST_SECRET_KEY = os.getenv('STRIPE_TEST_SECRET_KEY')

# CELERY
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'

# REST API
SITE_URL = 'http://127.0.0.1:8000'
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',  # Разрешить доступ всем
    ],
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',  # Ограничение запросов для анонимных пользователей
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/hour',  # Лимит запросов для анонимных пользователей
    },
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',  # Рендеринг в JSON
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',  # Парсинг JSON-данных
    ],
}

# Настройка CORS для разработки и продакшена
if DEBUG:
    CORS_ALLOW_ALL_ORIGINS = True
else:
    CORS_ALLOWED_ORIGINS = [  # Разрешенные источники
        'http://localhost:5173',
        'http://127.0.0.1:5173',
    ]

# Настройки безопасности
SECURE_BROWSER_XSS_FILTER = True  # Защита от XSS-атак
SECURE_CONTENT_TYPE_NOSNIFF = True  # Запрет MIME-типов
X_FRAME_OPTIONS = 'DENY'  # Защита от кликджекинга

# Настройки логирования
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',  # Уровень логирования
            'class': 'logging.FileHandler',  # Логирование в файл
            'filename': BASE_DIR / 'debug.log',  # Путь к файлу логов
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],  # Используемый обработчик
            'level': 'INFO',  # Уровень логирования
            'propagate': True,  # Передача логов родительским логгерам
        },
    },
}

# settings.py
# settings.py

UNFOLD = {
    "SITE_TITLE": "DressCode Admin",
    "SITE_HEADER": "DressCode Administration",

    # Логотип

    # Светлая тема
    "THEME": "light",
    "SHOW_THEME_SWITCH": False,

    # Цветовая схема по вашему дизайну
    "COLORS": {
        "primary": {
            "50": "250 245 238",  # #faf5ee - основной фон
            "100": "248 243 236",  # светлее основного фона
            "200": "240 235 228",
            "300": "220 215 208",
            "400": "180 175 168",  # промежуточный
            "500": "29 80 58",  # #1d503a - основной зеленый
            "600": "25 70 50",  # темнее основного
            "700": "20 60 42",
            "800": "15 50 35",
            "900": "10 40 28",  # самый темный зеленый
        },

        # Дополнительные цвета
        "gray": {
            "50": "250 245 238",  # #faf5ee
            "100": "248 249 250",  # #f8f9fa
            "200": "224 224 224",  # #e0e0e0
            "300": "178 126 126",  # #827e7e
            "400": "130 126 126",  # #827e7e
            "500": "51 51 51",  # #333333
            "600": "0 0 0",  # #000000
        }
    },

    # Дополнительные настройки
    "SHOW_HISTORY": True,
    "SHOW_VIEW_ON_SITE": True,
}
