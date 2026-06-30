
"""
User
  Board
    Checklist
      ChecklistItem
    Itinerary
    Notes
  Board
    ...
"""

from marshmallow import Schema, fields
from sqlalchemy.ext.hybrid import hybrid_property
from flask import Flask

from config import db, bcrypt

class Users(db.Models):
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