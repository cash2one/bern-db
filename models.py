from flask import url_for
from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin

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

roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __str__(self):
        return self.name


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

    def __str__(self):
        return self.email
