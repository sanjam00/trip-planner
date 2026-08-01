from marshmallow import Schema, fields

from .CheckListItemSchema import CheckListItemSchema

class CheckListSchema(Schema):
  id = fields.Int()
  title = fields.String()
  items = fields.Nested(CheckListItemSchema, many=True)