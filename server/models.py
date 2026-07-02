from marshmallow import Schema, fields
from enum import Enum
from sqlalchemy.ext.hybrid import hybrid_property
from flask import Flask

from config import db, bcrypt

# --- enum values ---
class Status(Enum):
  PACKED = 'packed'
  NOT_PACKED = 'not packed'
  PLANNED = 'planned'

# --- models ---

class User(db.Model):
  __tablename__ = "users"

  id = db.Column(db.Integer, primary_key = True)
  username = db.Column(db.String, nullable=False, unique=True)
  email = db.Column(db.String, nullable=False, unique=True)
  _password_hash = db.Column(db.String, nullable=False)

  trips = db.relationship('Trip', back_populates='user', cascade='all, delete-orphan')

  # protect password hash from being viewed
  @hybrid_property
  def password_hash(self):
    raise AttributeError("Password hashes may not be viewed")
  
  # hashes the password
  @password_hash.setter
  def password_hash(self, password):
    password_hash = bcrypt.generate_password_hash(
      password.encode('utf-8')
    )
    self._password_hash = password_hash.decode('utf-8')

  # authenticates user by comparing the stored hashed password to the newly entered hashed password
  def authenticate(self, password):
    return bcrypt.check_password_hash(
      self._password_hash, password.encode('utf-8')
    )
  
  def __repr__(self):
    return f'<Username: {self.username}, Email: {self.email}>'
  
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
  itinerarylist = db.relationship('ItineraryList', back_populates='trips', cascade='all, delete-orphan')
  
  def __repr__(self):
    return f'<Trip Trip {self.id}: {self.title}. Description: "{self.description}". Destination: {self.destination}. From {self.start_date} to {self.end_date}>'

class CheckList(db.Model):
  __tablename__ = "checklists"

  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String, nullable=False)
  
  trip_id = db.Column(db.Integer(), db.ForeignKey('trips.id'), nullable=False)

  trip = db.relationship('Trip', back_populates='checklists')
  items = db.relationship('CheckListItem', back_populates='checklist', cascade='all, delete-orphan')

  def __repr__(self):
    return f'Checklist {self.id}: {self.title}'

class CheckListItem(db.Model):
  __tablename__ = "checklistitem"

  id = db.Column(db.Integer, primary_key=True)
  item_name = db.Column(db.String, nullable=False)
  status = db.Column(db.Enum(Status), default=Status.NOT_PACKED, nullable=False)

  checklist_id = db.Column(db.Integer(), db.ForeignKey('checklists.id'), nullable=False)

  checklist = db.relationship('CheckList', back_populates='items')

  def __repr__(self):
    return f'Checklist Item {self.id}: {self.item_name}. Status {self.status}'

class ItineraryList(db.Model):
  __tablename__= "itinerarylist"

  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String, default="Itinerary")

  trip_id = db.Column(db.Integer(), db.ForeignKey('trips.id'), nullable=False)

  trip = db.relationship('Trip', back_populates='itineraries')
  items = db.relationship('ItineraryItem', back_populates='itinerarylist', cascade='all, delete-orphan')

  def __repr__(self):
    return f'Itinerary List {self.id}: {self.title}'

class ItineraryItem(db.Model):
  __tablename__ = "itineraries"

  id = db.Column(db.Integer, primary_key=True)
  activity = db.Column(db.String, nullable=False)
  start_time = db.Column(db.Time)
  end_time = db.Column(db.Time)
  day = db.Column(db.Date)

  itinerarylist_id = db.Column(db.Integer, db.ForeignKey("itinerarylist.id"))

  itinerarylist = db.relationship("ItineraryList", back_populates="items")

  def __repr__(self):
    return f'ItineraryItem {self.id}. Activity: {self.activity}. Time and day: {self.start_time} - {self.end_time} on {self.day}'
  
# --- Schemas ---

class UserSchema(Schema):
  id = fields.Int()
  username = fields.String()
  email = fields.String()

class TripSchema(Schema):
  id = fields.Int()
  title = fields.String()
  description = fields.String()
  destination = fields.String()
  start_date = fields.Date()
  end_date = fields.Date()
  notes = fields.String()

  # nested under users
  checklists = fields.Nested(CheckListSchema)
  itinerarylist = fields.Nested(ItineraryListSchema)

class CheckListSchema(Schema):
  id = fields.Int()
  title = fields.String()

  # nested under trip
  trip = fields.Nested(TripSchema)

class CheckListItemSchema(Schema):
  id = fields.Int()
  item_name = fields.String()
  status = fields.Enum(Status, by_value=True)

  # nested under CheckList
  checklist = fields.Nested(CheckListSchema)

class ItineraryListSchema(Schema):
  id = fields.Int()
  title = fields.String()

  # nested under trip
  trip = fields.Nested(TripSchema)

class ItineraryItemSchema(Schema):
  id = fields.Int()
  activity = fields.String()
  start_time = fields.Time()
  end_time = fields.Time()
  day = fields.Date()

  # nested under ItineraryList
  itinerarylist = fields.Nested(ItineraryListSchema)