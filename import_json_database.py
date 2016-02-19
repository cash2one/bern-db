import json
from datetime import datetime
from app import db
from models import Quote, Tag

db.drop_all()
db.create_all()
print(db.session)

data = {}
with open("database.json") as f:
    data = json.load(f)

for tag in data.get("tags"):
    print("Inserting Tag: {}".format(tag))

    tag_model = Tag(
        name=tag
    )
    db.session.add(tag_model)


for quote in data.get("quotes"):
    print("Inserting Quote: {}".format(quote.get("text")[:30]))

    tags = Tag.query.filter(Tag.name.in_(quote.get("tags"))).all()
    quote_model = Quote(
        text=quote.get("text"),
        author=quote.get("author"),
        date=datetime.strptime(quote.get("date"), "%Y/%m/%d").date(),
        credit=quote.get("source").get("credit"),
        credit_url=quote.get("source").get("credit_url"),
        source_url=quote.get("source").get("url"),
        tags=tags
    )
    db.session.add(quote_model)

db.session.commit()
