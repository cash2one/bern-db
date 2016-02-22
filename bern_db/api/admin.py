from ..admin import LoginRequiredView
from ..extensions import admin, db
from .models import Quote, Tag

admin.add_view(LoginRequiredView(Quote, db.session))
admin.add_view(LoginRequiredView(Tag, db.session))
