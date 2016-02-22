from flask import url_for
from .schema import TagSchema, QuoteSchema
from ..extensions import db

tag_schema = TagSchema()
quote_schema = QuoteSchema()

quote_tags = db.Table("quote_tags", db.Model.metadata,
    db.Column("tag_id", db.Integer, db.ForeignKey("tag.id")),
    db.Column("quote_id", db.Integer, db.ForeignKey("quote.id")),
)

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)

    @classmethod
    def get_by_name(self, tag_name):
        return self.query.filter_by(name=tag_name).first_or_404()

    def make_public_quotes(self):
        return [q.make_public() for q in self.quotes]

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
        public_quote["tags"] = [tag.name for tag in self.tags]
        public_quote["uri"] = url_for("v0.get_quote", quote_id=self.id, _external=True)

        return public_quote

    @classmethod
    def get_random(self):
        return self.query.order_by(db.func.random()).limit(1).first()

    @classmethod
    def get_by_random_tag_name(self, tag_name):
        quote = db.session.query(self)\
            .filter(self.tags.any(name=tag_name))\
            .order_by(db.func.random())\
            .limit(1).first()
        return quote

    @classmethod
    def get_by_id(self, quote_id):
        return self.query.filter_by(id=quote_id).first_or_404()

    def __str__(self):
        return self.text
