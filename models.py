import peewee
from flask import url_for
from peewee import SqliteDatabase
from playhouse.fields import ManyToManyField
from playhouse.shortcuts import model_to_dict

from app import db

class BaseModel(peewee.Model):
    class Meta:
        database = db

class Tag(BaseModel):
    name = peewee.CharField(unique=True, primary_key=True)

class Quote(BaseModel):
    text = peewee.TextField(unique=True)
    author = peewee.CharField()
    date = peewee.DateField()
    credit = peewee.CharField()
    credit_url = peewee.TextField()
    source_url = peewee.TextField()
    tags = ManyToManyField(Tag, related_name="quotes")

    def make_public(self):
        fields = [
            Quote.text, Quote.author, Quote.credit, Quote.credit_url,
            Quote.source_url, Quote.tags, Quote.date, Quote.id
        ]
        public_quote = model_to_dict(self, only=fields)
        public_quote["date"] = public_quote.get("date").strftime("%Y/%m/%d")
        public_quote["uri"] = url_for("get_quote", quote_id=self.id, _external=True)
        return public_quote


QuoteTag = Quote.tags.get_through_model()

def create_tables():
    models = [Tag, Quote, QuoteTag]
    db.create_tables(models, True)
