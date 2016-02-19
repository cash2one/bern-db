from marshmallow import Schema, fields

class TagSchema(Schema):
    name = fields.String()

class QuoteSchema(Schema):
    id = fields.Integer()
    text = fields.String()
    author = fields.String()
    date = fields.Date()
    credit = fields.String()
    credit_url = fields.String()
    source_url = fields.String()
    tags = fields.Nested(TagSchema, many=True)
