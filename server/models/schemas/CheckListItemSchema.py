from marshmallow import Schema, fields

from models.CheckListItem import Status

class CheckListItemSchema(Schema):
  id = fields.Int()
  item_name = fields.String()
  status = fields.Enum(Status, by_value=True)
  # no 'checklist' nested here — you already have it from the parent