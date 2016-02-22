from ..admin import LoginRequiredView
from ..extensions import admin, db
from .models import User, Role

admin.add_view(LoginRequiredView(User, db.session))
admin.add_view(LoginRequiredView(Role, db.session))
