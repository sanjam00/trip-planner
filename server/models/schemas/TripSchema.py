from marshmallow import Schema, fields

from .CheckListSchema import CheckListSchema
from .ItineraryItemSchema import ItineraryItemSchema

class TripSchema(Schema):
  id = fields.Int()
  title = fields.String()
  description = fields.String()
  destination = fields.String()
  start_date = fields.Date()
  end_date = fields.Date()
  notes = fields.String()

  checklists = fields.Nested(CheckListSchema, many=True)
  itinerary_items = fields.Nested(ItineraryItemSchema, many=True)