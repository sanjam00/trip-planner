from marshmallow import Schema, fields
from sqlalchemy.ext.hybrid import hybrid_property
from flask import Flask

from config import db, bcrypt

class Users(db.Models):
  __tablename__ = "users"

  id = db.Column(db.Integer, primary_key = True)
  username = db.Column(db.String, nullable=False, unique=True)
  email = db.Column(db.String, nullable=False, unique=True)
  _password_hash = (db.String)

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
  
class Board(db.Models):
  __tablename__ = "board"

  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String, nullable=False)
  description = db.Column(db.String)
  travellers = db.Column(db.String)
  destination = db.Column(db.String)
  start_date = db.Column(db.String)
  end_date = db.Column(db.String)
  notes = db.Column(db.String)

  user_id = db.Column(db.Integer(), db.ForeignKey('users.id'), nullable=False)
  
  def __repr__(self):
    return f'<Trip Board {self.id}: {self.title}. Description: "{self.description}". Travellers: {self.travellers}. Destination: {self.destination}. From {self.start_date} to {self.end_date}>'

class CheckList(db.Models):
  __tablename__ = "checklist"

  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String, nullable=False)
  assigned_to = db.Column(db.String)
  
  board_id = db.Column(db.Integer(), db.ForeignKey('board.id'), nullable=False)

  def __repr__(self):
    return f'Checklist {self.id}: {self.title}. Assigned to: {self.assigned_to}'

class CheckListItem(db.Models):
  __tablename__ = "checklistitem"

  id = db.Column(db.Integer, primary_key=True)
  item_name = db.Column(db.String, nullable=False)
  packed = db.Column(db.Boolean)
  assigned_to = db.Column(db.String)

  checklist_id = db.Column(db.Integer(), db.ForeignKet('checklist.id'), nullable=False)

  def __repr__(self):
    return f'Checklist Item {self.id}: {self.item_name}. Assigned to: {self.assigned_to}. Packed {self.packed}'

class Itinerary(db.Models):
  __tablename__ = "intinerary"

  id = db.Column(db.Integer, primary_key=True)
  activity = db.Column(db.String, nullable=False)
  time = db.Column(db.String)
  day = db.Column(db.String)

  board_id = db.Column(db.Integer(), db.ForeignKey('board.id'), nullable=False)

  def __repr__(self):
    return f'Itinerary {self.id}. Activity: {self.activity}. Time and day: {self.time} on {self.day}'