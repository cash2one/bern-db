from flask.ext.sqlalchemy import SQLAlchemy
db = SQLAlchemy()

from flask.ext.admin import Admin
admin = Admin()

from flask.ext.limiter import Limiter
limiter = Limiter()

from flask.ext.security import Security
security = Security()
