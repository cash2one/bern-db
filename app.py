import random, json
from flask import Flask, jsonify, url_for, abort

app = Flask(__name__)

database = {}
with open("database.json") as db:
    database = json.load(db)

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not Found"}), 404

def make_public_quote(quote):
    public_quote = quote.copy()
    public_quote["uri"] = url_for("get_quote", quote_id=public_quote.get("id"), _external=True)
    return public_quote

def quote_random(quotes):
    if len(quotes) == 0:
        return None
    return random.choice(quotes)

def quotes_by_tag(tag):
    return [quote for quote in database.get("quotes") if tag in quote["tags"]]

@app.route("/v0/quotes", methods=["GET"])
def get_quotes():
    return jsonify({"quotes": [make_public_quote(quote) for quote in database.get("quotes")]})

@app.route("/v0/quotes/<int:quote_id>", methods=["GET"])
def get_quote(quote_id):
    quote = [quote for quote in database.get("quotes") if quote["id"] == quote_id]
    if len(quote) == 0:
        abort(404)
    return jsonify(quote[0])

@app.route("/v0/quotes/random", methods=["GET"])
def get_quote_random():
    return jsonify(make_public_quote(quote_random(database.get("quotes"))))

@app.route("/v0/quotes/tag/<string:tag>", methods=["GET"])
def get_quotes_by_tag(tag):
    quotes = quotes_by_tag(tag)
    if len(quotes) == 0:
        abort(404)
    return jsonify({"quotes": [make_public_quote(quote) for quote in quotes]})

@app.route("/v0/quotes/tag/<string:tag>/random", methods=["GET"])
def get_quotes_by_tag_random(tag):
    quote = quote_random(quotes_by_tag(tag))
    if quote is None:
        abort(404)
    return jsonify(make_public_quote(quote))

if __name__ == "__main__":
    app.run(debug=True)
