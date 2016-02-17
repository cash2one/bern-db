import peewee
from peewee import SqliteDatabase
from playhouse.fields import ManyToManyField

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

QuoteTag = Quote.tags.get_through_model()
