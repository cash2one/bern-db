from flask import url_for
from flask_sqlalchemy import SQLAlchemy

from app import db
from schema import TagSchema, QuoteSchema
tag_schema = TagSchema()
quote_schema = QuoteSchema()

quote_tags = db.Table("quote_tags", db.Model.metadata,
        db.Column("tag_id", db.Integer, db.ForeignKey("tag.id")),
        db.Column("quote_id", db.Integer, db.ForeignKey("quote.id")),
)

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)

    def __str__(self):
        return self.name

class Quote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text)
    author = db.Column(db.String)
    date = db.Column(db.Date)
    credit = db.Column(db.String)
    credit_url = db.Column(db.Text)
    source_url = db.Column(db.Text)
    tags = db.relationship("Tag", secondary=quote_tags, backref="quotes")

    def make_public(self):
        public_quote = quote_schema.dump(self).data
        public_quote["uri"] = url_for("get_quote", quote_id=self.id, _external=True)

        return public_quote

    def __str__(self):
        return self.text
