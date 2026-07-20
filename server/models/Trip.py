from marshmallow import Schema, fields
from enum import Enum
from sqlalchemy.ext.hybrid import hybrid_property

from config import db, bcrypt

class Trip(db.Model):
  __tablename__ = "trips"

  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String, nullable=False)
  description = db.Column(db.String)
  destination = db.Column(db.String)
  start_date = db.Column(db.Date)
  end_date = db.Column(db.Date)
  notes = db.Column(db.Text)

  user_id = db.Column(db.Integer(), db.ForeignKey('users.id'), nullable=False)

  user = db.relationship('User', back_populates='trips')
  checklists = db.relationship('CheckList', back_populates='trip', cascade='all, delete-orphan')
  # one itinerary per trip now — itinerary items hang directly off the trip
  itinerary_items = db.relationship('ItineraryItem', back_populates='trip', cascade='all, delete-orphan')

  def __repr__(self):
    return f'<Trip Trip {self.id}: {self.title}. Description: "{self.description}". Destination: {self.destination}. From {self.start_date} to {self.end_date}>'
