from marshmallow import Schema, fields
from enum import Enum
from sqlalchemy.ext.hybrid import hybrid_property

from config import db, bcrypt

class CheckList(db.Model):
  __tablename__ = "checklists"

  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String, nullable=False)

  trip_id = db.Column(db.Integer(), db.ForeignKey('trips.id'), nullable=False)

  trip = db.relationship('Trip', back_populates='checklists')
  items = db.relationship('CheckListItem', back_populates='checklist', cascade='all, delete-orphan')

  def __repr__(self):
    return f'Checklist {self.id}: {self.title}'
