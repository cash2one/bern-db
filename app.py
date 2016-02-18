import random
import config
from flask import Flask, jsonify, url_for, abort
from peewee import SqliteDatabase, fn
from playhouse.flask_utils import get_object_or_404

app = Flask(__name__)
app.config.from_object("config")

db = SqliteDatabase(app.config.get("DATABASE_NAME"))

import models

@app.before_request
def _db_connect():
    db.connect()

@app.teardown_request
def _db_close(req):
    if not db.is_closed():
        db.close()

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not Found"}), 404

def quotes_by_tag(tag):
    return [quote for quote in database.get("quotes") if tag in quote["tags"]]

@app.route("/v0/quotes", methods=["GET"])
def get_quotes():
    public_quotes = []
    quotes = models.Quote.select()
    for quote in quotes.iterator():
        public_quotes.append(quote.make_public())

    return jsonify({"quotes": public_quotes})

@app.route("/v0/quotes/<int:quote_id>", methods=["GET"])
def get_quote(quote_id):
    quotes = models.Quote.select()
    quote = get_object_or_404(quotes, (models.Quote.id == quote_id))
    public_quote = quote.make_public()

    return jsonify(public_quote)

@app.route("/v0/quotes/random", methods=["GET"])
def get_quote_random():
    quote = models.Quote.select().order_by(fn.Random()).limit(1)[0]
    public_quote = quote.make_public()

    return jsonify(public_quote)

@app.route("/v0/quotes/tags/<string:tag_slug>", methods=["GET"])
def get_quotes_by_tag(tag_slug):
    tag = get_object_or_404(models.Tag.select(), (models.Tag.name == tag_slug))
    public_quotes = []
    for quote in tag.quotes.iterator():
        public_quotes.append(quote.make_public())

    return jsonify({"quotes": public_quotes})

@app.route("/v0/quotes/tags/<string:tag_slug>/random", methods=["GET"])
def get_quotes_by_tag_random(tag_slug):
    tag = get_object_or_404(models.Tag.select(), (models.Tag.name == tag_slug))
    quote = tag.quotes.order_by(fn.Random(), models.Quote.id).limit(1).get()
    public_quote = quote.make_public()

    return jsonify(public_quote)
