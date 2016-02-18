import json
import models
from datetime import datetime
from app import db

db.connect()

models.Quote.create_table(True)
models.Tag.create_table(True)
models.QuoteTag.create_table(True)

data = {}
with open("database.json") as db:
    data = json.load(db)

for tag in data.get("tags"):
    print("Inserting Tag: {}".format(tag))

    tag_model = models.Tag.get_or_create(
        name=tag
    )


for quote in data.get("quotes"):
    print("Inserting Quote: {}".format(quote.get("text")[:30]))

    quote_model, created = models.Quote.get_or_create(
        text=quote.get("text"),
        author=quote.get("author"),
        date=datetime.strptime(quote.get("date"), "%Y/%m/%d").date(),
        credit=quote.get("source").get("credit"),
        credit_url=quote.get("source").get("credit_url"),
        source_url=quote.get("source").get("url")
    )

    if created:
        tags = models.Tag.select().where(models.Tag.name.in_(quote.get("tags")))
        quote_model.tags.add(tags)

db.close()
