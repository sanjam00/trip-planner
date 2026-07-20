from marshmallow import Schema, fields

class ItineraryItemSchema(Schema):
  id = fields.Int()
  activity = fields.String()
  start_time = fields.Time()
  end_time = fields.Time()
  day = fields.Date()
  # no 'trip' nested here — same reasoning as above