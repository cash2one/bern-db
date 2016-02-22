from flask import Blueprint, jsonify
from ..models import Quote, Tag

v0 = Blueprint("v0", __name__, url_prefix="/v0")

@v0.route("/quotes", methods=["GET"])
def get_quotes():
    public_quotes = []
    quotes = Quote.query.all()
    for quote in quotes:
        public_quotes.append(quote.make_public())

    return jsonify({"quotes": public_quotes})

@v0.route("/quotes/<int:quote_id>", methods=["GET"])
def get_quote(quote_id):
    public_quote = Quote.get_by_id(quote_id).make_public()
    return jsonify(public_quote)

@v0.route("/quotes/random", methods=["GET"])
def get_quote_random():
    public_quote = Quote.get_random().make_public()
    return jsonify(public_quote)

@v0.route("/quotes/tags", methods=["GET"])
def get_quote_tags():
    tags = Tag.query.all()
    public_tags = [tag.name for tag in tags]
    return jsonify({"tags": public_tags})

@v0.route("/quotes/tags/<string:tag_name>", methods=["GET"])
def get_quotes_by_tag(tag_name):
    public_quotes = Tag.get_by_name(tag_name).make_public_quotes()
    return jsonify({"quotes": public_quotes})

@v0.route("/quotes/tags/<string:tag_name>/random", methods=["GET"])
def get_quote_by_tag_random(tag_name):
    public_quote = Quote.get_by_random_tag_name(tag_name).make_public()
    return jsonify(public_quote)
