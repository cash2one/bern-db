import random
import config

from flask import Flask, jsonify, url_for, abort
from flask_admin import Admin
from flask_admin.contrib import sqla
from flask_sqlalchemy import SQLAlchemy
from flask_limiter import Limiter
from flask_security import Security, SQLAlchemyUserDatastore, login_required, current_user

app = Flask(__name__)
app.config.from_object("config")

db = SQLAlchemy(app)
limiter = Limiter(app)

import models


user_datastore = SQLAlchemyUserDatastore(db, models.User, models.Role)
security = Security(app, user_datastore)


class MyModelView(sqla.ModelView):

    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False

        if current_user.has_role('superuser'):
            return True

        return False

    def _handle_view(self, name, **kwargs):
        """
        Override builtin _handle_view in order to redirect users when a view is not accessible.
        """
        if not self.is_accessible():
            if current_user.is_authenticated:
                # permission denied
                abort(403)
            else:
                # login
                return redirect(url_for('security.login', next=request.url))

class TagAdmin(MyModelView):
    def __init__(self, session):
        super(TagAdmin, self).__init__(models.Tag, session)

class QuoteAdmin(MyModelView):
    form_ajax_refs = {
        "tags": {
            "fields": (models.Tag.name,)
        }
    }
    def __init__(self, session):
        super(QuoteAdmin, self).__init__(models.Quote, session)
admin = Admin(app, name="ASDASD")
admin.add_view(QuoteAdmin(db.session))
admin.add_view(TagAdmin(db.session))
admin.add_view(MyModelView(models.Role, db.session))
admin.add_view(MyModelView(models.User, db.session))

for view in admin._views:
    limiter.exempt(view.blueprint)

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not Found"}), 404

@app.errorhandler(429)
def not_found(error):
    return jsonify({
        "error": "Too Many Requests",
        "description": error.description
    }), 429

def quotes_by_tag(tag):
    return [quote for quote in database.get("quotes") if tag in quote["tags"]]

@app.route("/v0/quotes", methods=["GET"])
def get_quotes():
    public_quotes = []
    quotes = models.Quote.query.all()
    for quote in quotes:
        public_quotes.append(quote.make_public())

    return jsonify({"quotes": public_quotes})

@app.route("/v0/quotes/<int:quote_id>", methods=["GET"])
def get_quote(quote_id):
    quote = models.Quote.query.get_or_404(quote_id)
    public_quote = quote.make_public()

    return jsonify(public_quote)

@app.route("/v0/quotes/random", methods=["GET"])
def get_quote_random():
    quote = models.Quote.query.order_by(db.func.random()).limit(1).first()
    public_quote = quote.make_public()

    return jsonify(public_quote)

@app.route("/v0/quotes/tags", methods=["GET"])
def get_quote_tags():
    tags = models.Tag.query.all()
    public_tags = [tag.name for tag in tags]
    return jsonify({"tags": public_tags})

@app.route("/v0/quotes/tags/<string:tag_slug>", methods=["GET"])
def get_quotes_by_tag(tag_slug):
    tag = models.Tag.query.filter_by(name=tag_slug).first_or_404()
    public_quotes = []
    for quote in tag.quotes:
        public_quotes.append(quote.make_public())

    return jsonify({"quotes": public_quotes})

@app.route("/v0/quotes/tags/<string:tag_slug>/random", methods=["GET"])
def get_quotes_by_tag_random(tag_slug):
    quote = db.session.query(models.Quote)\
        .filter(models.Quote.tags.any(name=tag_slug))\
        .order_by(db.func.random())\
        .limit(1).first()
    public_quote = quote.make_public()

    return jsonify(public_quote)
