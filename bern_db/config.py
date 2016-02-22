DEBUG=True
PROJECT_NAME = "Bern DB"
SECRET_KEY = "H77CQut7L0Wn1NOblPE/z+zQ+NPMN1D6WFn+QL5Y2Rk="

DATABASE_NAME = ""
DATABASE_USERNAME = ""
DATABASE_PASSWORD = ""
DATABASE_HOSTNAME = "localhost"

SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_DATABASE_URI = "postgres://{}:{}@{}/{}".format(
    DATABASE_USERNAME,
    DATABASE_PASSWORD,
    DATABASE_HOSTNAME,
    DATABASE_NAME
)

RATELIMIT_GLOBAL = "10/minute,100/day"
RATELIMIT_STORAGE_URL = "redis://127.0.0.1:6379"
RATELIMIT_HEADERS_ENABLED = True

SECURITY_URL_PREFIX = "/admin"
SECURITY_PASSWORD_HASH = "pbkdf2_sha512"
SECURITY_PASSWORD_SALT = "StpeaPxpPPHxltwO3hNcnSuYlqzFMwtPuawHhVdg25E="
SECURITY_POST_LOGIN_VIEW = "/admin/"
SECURITY_POST_LOGOUT_VIEW = "/admin/"
SECURITY_POST_REGISTER_VIEW = "/admin/"
SECURITY_SEND_REGISTER_EMAIL = False
SECURITY_REGISTERABLE = False

try:
    from .config_local import *
except ImportError:
    pass

try:
    from .config_production import *
except ImportError:
    pass