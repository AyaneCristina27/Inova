import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get("SECRET_KEY")

# ---------------------------------------------------------------------
# Modo de desenvolvimento x produção
# No seu computador, o .env tem DEBUG=True.
# Na Vercel, a variável DEBUG não é cadastrada, então fica desligado.
# ---------------------------------------------------------------------
DEBUG = os.environ.get("DEBUG", "False") == "True"

ALLOWED_HOSTS = ["localhost", "127.0.0.1", ".vercel.app"]
CSRF_TRUSTED_ORIGINS = ["https://*.vercel.app"]

if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "app",
    "django_plotly_dash.apps.DjangoPlotlyDashConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_plotly_dash.middleware.BaseMiddleware",
]

# Necessário para o django-plotly-dash (dashboard em Dash)
X_FRAME_OPTIONS = "SAMEORIGIN"

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(BASE_DIR, "app/templates"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# ---------------------------------------------------------------------
# Banco de dados
# Na Vercel, o Supabase é acessado pelo Transaction pooler (porta 6543),
# que exige DISABLE_SERVER_SIDE_CURSORS. Isso é ativado automaticamente.
# ---------------------------------------------------------------------
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("DB_NAME"),
        "USER": os.environ.get("DB_USER"),
        "PASSWORD": os.environ.get("DB_PASSWORD"),
        "HOST": os.environ.get("DB_HOST"),
        "PORT": os.environ.get("DB_PORT"),
        "OPTIONS": {"sslmode": os.environ.get("DB_SSLMODE", "prefer")},
        "DISABLE_SERVER_SIDE_CURSORS": os.environ.get("DB_PORT") == "6543",
        "CONN_MAX_AGE": 0,
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Sao_Paulo"
USE_I18N = True
USE_TZ = True

# ---------------------------------------------------------------------
# Arquivos estáticos (CSS, JavaScript, imagens do layout)
# Na Vercel, o collectstatic roda sozinho e os arquivos são servidos pela CDN.
# ---------------------------------------------------------------------
STATIC_URL = "static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "app/static/"),
]

MEDIA_URL = "media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# ---------------------------------------------------------------------
# Armazenamento das imagens (uploads) no Supabase Storage
# Com USE_SUPABASE_STORAGE=True, os uploads vão para o bucket do Supabase.
# Com False (ou sem a variável), usa a pasta media local.
# ---------------------------------------------------------------------
if os.environ.get("USE_SUPABASE_STORAGE") == "True":
    SUPABASE_PROJECT_REF = os.environ.get("SUPABASE_PROJECT_REF")
    SUPABASE_BUCKET = os.environ.get("SUPABASE_BUCKET")

    STORAGES = {
        "default": {
            "BACKEND": "app.storage.SupabaseStorage",
            "OPTIONS": {
                "bucket_name": SUPABASE_BUCKET,
                "access_key": os.environ.get("SUPABASE_S3_ACCESS_KEY_ID"),
                "secret_key": os.environ.get("SUPABASE_S3_SECRET_ACCESS_KEY"),
                "endpoint_url": os.environ.get("SUPABASE_S3_ENDPOINT"),
                "region_name": os.environ.get("SUPABASE_S3_REGION"),
                "addressing_style": "path",
                "default_acl": None,
                "querystring_auth": False,
                "file_overwrite": False,
                "custom_domain": f"{SUPABASE_PROJECT_REF}.supabase.co/storage/v1/object/public/{SUPABASE_BUCKET}",
            },
        },
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
        },
    }

LOGIN_URL = "login"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ---------------------------------------------------------------------
# Configuração de e-mail (envio de link de redefinição de senha)
# ---------------------------------------------------------------------
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = f"INova Sudoeste de Minas <{EMAIL_HOST_USER}>"