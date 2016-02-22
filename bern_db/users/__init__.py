from flask.ext.security import SQLAlchemyUserDatastore
from ..extensions import db
from .admin import *
from .models import User, Role

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
