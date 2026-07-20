from marshmallow import Schema, fields
from enum import Enum
from sqlalchemy.ext.hybrid import hybrid_property

from config import db, bcrypt

class ItineraryItem(db.Model):
  __tablename__ = "itinerary_items"

  id = db.Column(db.Integer, primary_key=True)
  activity = db.Column(db.String, nullable=False)
  start_time = db.Column(db.Time)
  end_time = db.Column(db.Time)
  day = db.Column(db.Date)

  trip_id = db.Column(db.Integer(), db.ForeignKey('trips.id'), nullable=False)

  trip = db.relationship('Trip', back_populates='itinerary_items')

  def __repr__(self):
    return f'ItineraryItem {self.id}. Activity: {self.activity}. Time and day: {self.start_time} - {self.end_time} on {self.day}'
