from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "django-insecure-demo-key-for-dissertation-evidence-only"

DEBUG = True

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "corsheaders",
    "api",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",  # this is the protection Bug 4 bypasses via @csrf_exempt
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

AUTH_PASSWORD_VALIDATORS = []

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ---------------------------------------------------------------------------
# CORS is NOT the vulnerability under test in this demo — it stays fixed
# throughout so it doesn't interfere with the CSRF evidence.
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5501",   # the trusted frontend only
]
CORS_ALLOW_CREDENTIALS = True
# ---------------------------------------------------------------------------

# Carried over from Bug 2 (5.2) — required for the cross-origin session
# cookie to be sent at all in a micro-frontend split.
SESSION_COOKIE_SAMESITE = "None"
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SAMESITE = "None"
CSRF_COOKIE_SECURE = True

# Since Django 4.0, CsrfViewMiddleware checks the Origin header (when present)
# against CSRF_TRUSTED_ORIGINS for any unsafe request, on any scheme — not only
# HTTPS. Because this is a genuinely cross-origin micro-frontend split, the
# trusted frontend's origin must be listed explicitly, or its own legitimate
# requests would be rejected identically to the attacker's. The attacker's
# origin is deliberately NOT listed here.
CSRF_TRUSTED_ORIGINS = [
    "http://localhost:5501",
]

# Returns a JSON error body on CSRF failure instead of Django's default HTML page.
CSRF_FAILURE_VIEW = "api.views.csrf_failure_view"
